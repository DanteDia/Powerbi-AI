"""
Excel Source Profiler — Reads the Excel workbooks referenced by the PBIX model
and generates workbook/sheet documentation plus data quality profiling.
"""

import json
import re
import warnings
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import click
import pandas as pd


EXCEL_FILE_RE = re.compile(
    r'Excel\.Workbook\s*\(\s*File\.Contents\s*\(\s*"([^"]+)"'
)
EXCEL_ITEM_RE = re.compile(
    r'\{\[Item\s*=\s*"([^"]+)"\s*,\s*Kind\s*=\s*"([^"]+)"\]\}\[Data\]'
)
EXCEL_NAME_RE = re.compile(
    r'\{\[[^\]]*Name\s*=\s*"([^"]+)"[^\]]*\]\}\[Data\]'
)


def _load_extracted(extracted_dir):
    results = []
    for json_file in sorted(Path(extracted_dir).glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            results.append(json.load(f))
    return results


def _normalize_name(value):
    if value is None:
        return ""
    return str(value).strip()


def _parse_excel_source(expression):
    expression = expression or ""
    file_match = EXCEL_FILE_RE.search(expression)
    if not file_match:
        return None

    item_match = EXCEL_ITEM_RE.search(expression)
    name_match = EXCEL_NAME_RE.search(expression)

    return {
        "file_path": file_match.group(1),
        "item_name": item_match.group(1) if item_match else (name_match.group(1) if name_match else None),
        "item_kind": item_match.group(2) if item_match else ("NamedRangeOrTable" if name_match else None),
        "expression": expression,
    }


def _collect_excel_sources(extracted_dir):
    sources = defaultdict(lambda: {"pbix_tables": []})

    for extraction in _load_extracted(extracted_dir):
        report_name = extraction.get("file", "unknown")
        for row in extraction.get("power_query", []):
            table_name = row.get("TableName", "")
            expression = row.get("Expression", "")
            parsed = _parse_excel_source(expression)
            if not parsed:
                continue

            file_path = parsed["file_path"]
            record = {
                "report": report_name,
                "pbix_table": table_name,
                "item_name": parsed.get("item_name"),
                "item_kind": parsed.get("item_kind"),
                "expression": expression,
            }
            sources[file_path]["pbix_tables"].append(record)

    normalized = {}
    for file_path, info in sources.items():
        unique_tables = []
        seen = set()
        for record in info["pbix_tables"]:
            key = (
                record["report"],
                record["pbix_table"],
                record.get("item_name"),
                record.get("item_kind"),
            )
            if key in seen:
                continue
            seen.add(key)
            unique_tables.append(record)
        normalized[file_path] = {"pbix_tables": unique_tables}

    return normalized


def _infer_series_type(series):
    non_null = series.dropna()
    if non_null.empty:
        return "empty"

    if pd.api.types.is_bool_dtype(non_null):
        return "boolean"
    if pd.api.types.is_numeric_dtype(non_null):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(non_null):
        return "datetime"

    parsed_numeric = pd.to_numeric(non_null, errors="coerce")
    if parsed_numeric.notna().mean() >= 0.95:
        return "numeric"

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed_datetime = pd.to_datetime(non_null, errors="coerce")
    if parsed_datetime.notna().mean() >= 0.95:
        return "datetime"

    lowered = non_null.astype(str).str.strip().str.lower()
    if lowered.isin({"true", "false", "si", "sí", "no", "0", "1"}).mean() >= 0.95:
        return "boolean-like text"

    return "text"


def _profile_column(series):
    row_count = len(series)
    text_values = series.astype(str)
    blank_string_mask = series.notna() & text_values.str.strip().eq("")
    blank_string_count = int(blank_string_mask.sum())
    null_count = int(series.isna().sum()) + blank_string_count
    non_empty = series[~series.isna() & ~blank_string_mask]
    unique_non_null = int(non_empty.nunique(dropna=True)) if not non_empty.empty else 0

    return {
        "name": _normalize_name(series.name),
        "inferred_type": _infer_series_type(non_empty),
        "null_count": null_count,
        "null_pct": round((null_count / row_count) * 100, 2) if row_count else 0.0,
        "unique_non_null": unique_non_null,
        "is_unique_non_null": bool(
            len(non_empty) > 0 and unique_non_null == len(non_empty)
        ),
        "non_empty_count": int(len(non_empty)),
    }


def _profile_sheet(file_path, sheet_name):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=object)
    df.columns = [_normalize_name(col) or f"Unnamed_{idx + 1}" for idx, col in enumerate(df.columns)]

    column_profiles = [_profile_column(df[col]) for col in df.columns]
    duplicate_rows = int(df.duplicated().sum()) if not df.empty else 0

    candidate_keys = [
        col["name"]
        for col in column_profiles
        if col["is_unique_non_null"] and col["non_empty_count"] >= max(1, int(len(df) * 0.8))
    ][:8]

    quality_flags = []
    if df.empty:
        quality_flags.append("empty_sheet")
    if duplicate_rows > 0:
        quality_flags.append("duplicate_rows")
    if any(col["name"].lower().startswith("column") for col in column_profiles):
        quality_flags.append("generic_column_names")
    if any(col["name"].lower().startswith("unnamed_") for col in column_profiles):
        quality_flags.append("unnamed_columns")
    if any(col["null_pct"] >= 50 for col in column_profiles):
        quality_flags.append("high_missingness")

    return {
        "sheet_name": _normalize_name(sheet_name),
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "duplicate_row_count": duplicate_rows,
        "candidate_keys": candidate_keys,
        "quality_flags": quality_flags,
        "columns": column_profiles,
    }


def _build_workbook_profile(file_path, source_info):
    path = Path(file_path)
    workbook = {
        "file_path": file_path,
        "file_name": path.name,
        "exists": path.exists(),
        "pbix_tables": sorted(
            source_info["pbix_tables"],
            key=lambda x: (_normalize_name(x.get("pbix_table")), _normalize_name(x.get("item_name"))),
        ),
    }

    if not path.exists():
        workbook["error"] = "File not accessible"
        return workbook

    stat = path.stat()
    workbook["file_size_mb"] = round(stat.st_size / (1024 * 1024), 2)
    workbook["modified_at"] = datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        xls = pd.ExcelFile(file_path)
    workbook["sheet_names"] = [str(name) for name in xls.sheet_names]
    workbook["sheet_count"] = len(workbook["sheet_names"])

    referenced_items = defaultdict(list)
    for record in workbook["pbix_tables"]:
        item_name = _normalize_name(record.get("item_name"))
        if item_name:
            referenced_items[item_name].append(record["pbix_table"])

    sheets = []
    for sheet_name in workbook["sheet_names"]:
        sheet_profile = _profile_sheet(file_path, sheet_name)
        sheet_profile["referenced_by_pbix"] = sheet_name in referenced_items
        sheet_profile["pbix_tables"] = sorted(referenced_items.get(sheet_name, []))
        sheets.append(sheet_profile)

    workbook["sheets"] = sheets
    workbook["referenced_sheet_count"] = sum(1 for s in sheets if s["referenced_by_pbix"])
    workbook["unreferenced_sheets"] = [
        s["sheet_name"] for s in sheets if not s["referenced_by_pbix"]
    ]

    return workbook


def _build_summary(workbooks):
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_workbooks": len(workbooks),
        "accessible_workbooks": sum(1 for w in workbooks if w.get("exists")),
        "total_sheets": sum(len(w.get("sheets", [])) for w in workbooks),
        "total_referenced_pbix_tables": sum(len(w.get("pbix_tables", [])) for w in workbooks),
        "files_with_quality_flags": sum(
            1 for w in workbooks if any(s.get("quality_flags") for s in w.get("sheets", []))
        ),
    }


def _render_markdown(profile):
    lines = []
    summary = profile["summary"]
    lines.append("# Excel Source Documentation")
    lines.append("")
    lines.append(f"Generated: {summary['generated_at']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Workbooks analyzed: {summary['total_workbooks']}")
    lines.append(f"- Accessible workbooks: {summary['accessible_workbooks']}")
    lines.append(f"- Sheets profiled: {summary['total_sheets']}")
    lines.append(f"- PBIX tables mapped to Excel: {summary['total_referenced_pbix_tables']}")
    lines.append(f"- Workbooks with data quality flags: {summary['files_with_quality_flags']}")
    lines.append("")
    lines.append("## Workbook Inventory")
    lines.append("")
    lines.append("| Workbook | Size MB | Sheets | PBIX Tables | |")
    lines.append("|---|---:|---:|---:|---|")
    for workbook in profile["workbooks"]:
        lines.append(
            "| {name} | {size} | {sheets} | {tables} | {path} |".format(
                name=workbook["file_name"],
                size=workbook.get("file_size_mb", "n/a"),
                sheets=workbook.get("sheet_count", 0),
                tables=len(workbook.get("pbix_tables", [])),
                path=workbook["file_path"],
            )
        )

    for workbook in profile["workbooks"]:
        lines.append("")
        lines.append(f"## {workbook['file_name']}")
        lines.append("")
        lines.append(f"- Path: {workbook['file_path']}")
        if workbook.get("exists"):
            lines.append(f"- Size: {workbook.get('file_size_mb', 'n/a')} MB")
            lines.append(f"- Modified: {workbook.get('modified_at', 'n/a')}")
            lines.append(f"- Sheets: {workbook.get('sheet_count', 0)}")
            lines.append(f"- Referenced sheets: {workbook.get('referenced_sheet_count', 0)}")
        else:
            lines.append("- Status: not accessible")
            continue

        lines.append("")
        lines.append("### PBIX tables fed by this workbook")
        lines.append("")
        for record in workbook.get("pbix_tables", []):
            item_name = record.get("item_name") or "(not parsed)"
            item_kind = record.get("item_kind") or "unknown"
            lines.append(f"- `{record['pbix_table']}` ← {item_name} [{item_kind}]")

        lines.append("")
        lines.append("### Sheet profiling")
        lines.append("")
        lines.append("| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |")
        lines.append("|---|---|---:|---:|---:|---|---|")
        for sheet in workbook.get("sheets", []):
            lines.append(
                "| {name} | {ref} | {rows} | {cols} | {dupes} | {keys} | {flags} |".format(
                    name=sheet["sheet_name"],
                    ref="yes" if sheet.get("referenced_by_pbix") else "no",
                    rows=sheet.get("row_count", 0),
                    cols=sheet.get("column_count", 0),
                    dupes=sheet.get("duplicate_row_count", 0),
                    keys=", ".join(sheet.get("candidate_keys", [])[:3]) or "-",
                    flags=", ".join(sheet.get("quality_flags", [])) or "-",
                )
            )

        referenced_sheets = [s for s in workbook.get("sheets", []) if s.get("referenced_by_pbix")]
        if referenced_sheets:
            lines.append("")
            lines.append("### Referenced sheet column details")
            lines.append("")
            for sheet in referenced_sheets:
                lines.append(f"#### {sheet['sheet_name']}")
                lines.append("")
                if sheet.get("pbix_tables"):
                    lines.append(f"PBIX tables: {', '.join(sheet['pbix_tables'])}")
                    lines.append("")
                lines.append("| Column | Type | Null % | Unique Non-Null | |")
                lines.append("|---|---|---:|---:|---|")
                for column in sheet.get("columns", []):
                    lines.append(
                        "| {name} | {dtype} | {null_pct} | {unique_count} | {unique_flag} |".format(
                            name=column["name"],
                            dtype=column.get("inferred_type", "unknown"),
                            null_pct=column.get("null_pct", 0),
                            unique_count=column.get("unique_non_null", 0),
                            unique_flag="candidate key" if column.get("is_unique_non_null") else "",
                        )
                    )
                lines.append("")

    lines.append("")
    return "\n".join(lines)


@click.command()
@click.option("--extracted-dir", default="output/extracted", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--docs-dir", default="docs", type=click.Path(file_okay=False, path_type=Path))
@click.option("--json-name", default="excel_source_profile.json")
@click.option("--md-name", default="excel_source_documentation.md")
def main(extracted_dir, docs_dir, json_name, md_name):
    """Profile Excel workbooks referenced by the extracted PBIX metadata."""
    docs_dir.mkdir(parents=True, exist_ok=True)

    source_map = _collect_excel_sources(extracted_dir)
    workbooks = [
        _build_workbook_profile(file_path, info)
        for file_path, info in sorted(source_map.items(), key=lambda x: x[0].lower())
    ]
    profile = {
        "summary": _build_summary(workbooks),
        "workbooks": workbooks,
    }

    json_path = docs_dir / json_name
    md_path = docs_dir / md_name

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    md_path.write_text(_render_markdown(profile), encoding="utf-8")

    print("Excel profiling complete:")
    print(f"  Workbooks: {profile['summary']['total_workbooks']}")
    print(f"  Sheets: {profile['summary']['total_sheets']}")
    print(f"  JSON: {json_path}")
    print(f"  Markdown: {md_path}")


if __name__ == "__main__":
    main()
