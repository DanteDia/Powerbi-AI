"""
Report & Dashboard Analyzer — Maps all visuals, pages, filters, and data lineage.

Produces:
- Complete dashboard inventory (pages, visuals per page)
- Visual type distribution
- Data field usage (which tables/measures power which visuals)
- Filter inventory (report, page, visual level)
- Migration checklist per dashboard
"""

import json
from collections import Counter, defaultdict
from pathlib import Path


def _load_extracted(extracted_dir):
    """Load all extracted JSON files."""
    results = []
    for json_file in sorted(Path(extracted_dir).glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            results.append(json.load(f))
    return results


def _analyze_single_report(extraction):
    """Analyze a single report's layout data."""
    report_name = extraction.get("file", "unknown")
    pages = extraction.get("report_pages", [])
    report_filters = extraction.get("report_filters", [])
    bookmarks = extraction.get("bookmarks", [])

    visual_types = Counter()
    total_visuals = 0
    all_data_fields = defaultdict(set)  # table -> set of columns used
    all_measures_used = set()
    page_summaries = []

    for page in pages:
        page_visual_types = Counter()
        page_data_fields = defaultdict(set)
        page_measures = set()

        for visual in page.get("visuals", []):
            vtype = visual.get("visualType", "unknown")
            visual_types[vtype] += 1
            page_visual_types[vtype] += 1
            total_visuals += 1

            # Track data field usage
            for role, fields in visual.get("dataFields", {}).items():
                for field_ref in fields:
                    # Parse "Table.Column" or "Table.Measure" references
                    if "." in field_ref:
                        parts = field_ref.split(".", 1)
                        table = parts[0]
                        col = parts[1]
                        page_data_fields[table].add(col)
                        all_data_fields[table].add(col)
                    else:
                        all_measures_used.add(field_ref)
                        page_measures.add(field_ref)

        page_summary = {
            "name": page.get("displayName", page.get("name", "")),
            "ordinal": page.get("ordinal", 0),
            "visual_count": len(page.get("visuals", [])),
            "visual_types": dict(page_visual_types),
            "filter_count": len(page.get("filters", [])),
            "tables_referenced": sorted(page_data_fields.keys()),
            "fields_used": {
                t: sorted(cols) for t, cols in page_data_fields.items()
            },
        }
        page_summaries.append(page_summary)

    return {
        "report": report_name,
        "page_count": len(pages),
        "total_visuals": total_visuals,
        "visual_types": dict(visual_types),
        "report_filter_count": len(report_filters),
        "bookmark_count": len(bookmarks) if isinstance(bookmarks, list) else 0,
        "tables_referenced": sorted(all_data_fields.keys()),
        "fields_used": {
            t: sorted(cols) for t, cols in all_data_fields.items()
        },
        "pages": page_summaries,
    }


def _generate_migration_checklist(report_analysis, dax_catalog=None):
    """Generate a migration checklist for a single report."""
    checklist = []
    report = report_analysis["report"]

    # Data source migration
    for table in report_analysis.get("tables_referenced", []):
        checklist.append({
            "task": f"Migrate data source for table '{table}' from Excel to SQL",
            "category": "data_source",
            "priority": "high",
            "status": "pending",
        })

    # Page recreation
    for page in report_analysis.get("pages", []):
        page_name = page.get("name", "Unnamed")
        visual_count = page.get("visual_count", 0)
        checklist.append({
            "task": f"Recreate page '{page_name}' ({visual_count} visuals)",
            "category": "report_page",
            "priority": "medium",
            "status": "pending",
        })

    # Complex visuals
    complex_types = {"map", "decompositionTree", "scriptVisual", "pythonVisual"}
    for vtype, count in report_analysis.get("visual_types", {}).items():
        if vtype in complex_types:
            checklist.append({
                "task": f"Handle {count} '{vtype}' visual(s) — may need special attention",
                "category": "complex_visual",
                "priority": "high",
                "status": "pending",
            })

    # Filters
    if report_analysis.get("report_filter_count", 0) > 0:
        checklist.append({
            "task": f"Recreate {report_analysis['report_filter_count']} report-level filters",
            "category": "filter",
            "priority": "medium",
            "status": "pending",
        })

    # Bookmarks
    if report_analysis.get("bookmark_count", 0) > 0:
        checklist.append({
            "task": f"Recreate {report_analysis['bookmark_count']} bookmarks",
            "category": "bookmark",
            "priority": "low",
            "status": "pending",
        })

    return checklist


def analyze_reports(extracted_dir, output_dir):
    """Analyze all report layouts and generate migration checklists."""
    extractions = _load_extracted(extracted_dir)
    if not extractions:
        print("  No extracted data found. Run extract_pbix first.")
        return None

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report_analyses = []
    global_visual_types = Counter()
    global_tables_used = defaultdict(int)  # table -> number of reports using it
    total_pages = 0
    total_visuals = 0

    for extraction in extractions:
        analysis = _analyze_single_report(extraction)
        analysis["migration_checklist"] = _generate_migration_checklist(analysis)
        report_analyses.append(analysis)

        # Aggregate globals
        total_pages += analysis["page_count"]
        total_visuals += analysis["total_visuals"]
        for vtype, count in analysis["visual_types"].items():
            global_visual_types[vtype] += count
        for table in analysis["tables_referenced"]:
            global_tables_used[table] += 1

    # Build output
    result = {
        "summary": {
            "total_reports": len(report_analyses),
            "total_pages": total_pages,
            "total_visuals": total_visuals,
            "visual_type_distribution": dict(
                global_visual_types.most_common()
            ),
            "most_used_tables": dict(
                sorted(global_tables_used.items(),
                       key=lambda x: -x[1])[:20]
            ),
        },
        "reports": sorted(
            report_analyses,
            key=lambda x: -x["total_visuals"],
        ),
    }

    # Build combined migration checklist
    all_checklist_items = []
    for r in report_analyses:
        for item in r.get("migration_checklist", []):
            item["report"] = r["report"]
            all_checklist_items.append(item)

    result["migration_checklist"] = sorted(
        all_checklist_items,
        key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(
            x.get("priority", "low"), 3
        ),
    )

    # Save
    out_file = output_path / "report_inventory.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)

    # Print summary
    s = result["summary"]
    print(f"\n  Report Analysis Complete:")
    print(f"    Reports: {s['total_reports']}")
    print(f"    Total pages: {s['total_pages']}")
    print(f"    Total visuals: {s['total_visuals']}")
    print(f"\n  Visual types:")
    for vtype, count in list(s["visual_type_distribution"].items())[:10]:
        print(f"    {vtype}: {count}")
    print(f"\n  Migration checklist items: {len(result['migration_checklist'])}")
    print(f"    -> {out_file}")

    return result


if __name__ == "__main__":
    analyze_reports("output/extracted", "output/reports")
