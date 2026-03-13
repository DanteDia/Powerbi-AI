"""
PBIX Extractor — Parses .pbix files using pbixray and extracts report layouts.

Outputs structured JSON per report containing:
- Tables, columns, data types
- Relationships
- DAX measures and calculated columns
- Power Query (M) expressions
- Report layout (pages, visuals, filters)
"""

import json
import os
import zipfile
from pathlib import Path

import pandas as pd
from pbixray.core import PBIXRay


def _df_to_serializable(df):
    """Convert a pandas DataFrame to a JSON-serializable list of dicts."""
    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        return []
    if isinstance(df, pd.DataFrame):
        # Convert timestamps and other non-serializable types
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
        return df.to_dict(orient="records")
    return []


def _extract_report_layout(pbix_path):
    """Extract report layout JSON directly from the .pbix ZIP archive."""
    try:
        with zipfile.ZipFile(pbix_path, "r") as z:
            namelist = z.namelist()
            layout_data = {}

            # Report/Layout contains the main report definition
            if "Report/Layout" in namelist:
                with z.open("Report/Layout") as f:
                    raw = f.read()
                    # Layout is UTF-16-LE encoded JSON
                    try:
                        layout_json = json.loads(raw.decode("utf-16-le").lstrip("\ufeff"))
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        try:
                            layout_json = json.loads(raw.decode("utf-8"))
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            layout_json = {"raw_error": "Could not decode Report/Layout"}
                    layout_data["layout"] = layout_json

            # List all files in the archive for reference
            layout_data["archive_contents"] = namelist

            return layout_data
    except zipfile.BadZipFile:
        return {"error": "Not a valid ZIP/PBIX file"}
    except Exception as e:
        return {"error": str(e)}


def _parse_report_pages(layout_data):
    """Parse the report layout into structured pages and visuals."""
    if "layout" not in layout_data:
        return []

    layout = layout_data["layout"]
    sections = layout.get("sections", [])
    pages = []

    for section in sections:
        page = {
            "name": section.get("name", ""),
            "displayName": section.get("displayName", ""),
            "ordinal": section.get("ordinal", 0),
            "width": section.get("width", 0),
            "height": section.get("height", 0),
            "displayOption": section.get("displayOption", 0),
            "visuals": [],
            "filters": [],
        }

        # Parse page-level filters
        filters_json = section.get("filters", "[]")
        if isinstance(filters_json, str):
            try:
                page["filters"] = json.loads(filters_json)
            except json.JSONDecodeError:
                page["filters"] = []
        else:
            page["filters"] = filters_json if filters_json else []

        # Parse visuals
        visual_containers = section.get("visualContainers", [])
        for vc in visual_containers:
            visual = {
                "x": vc.get("x", 0),
                "y": vc.get("y", 0),
                "width": vc.get("width", 0),
                "height": vc.get("height", 0),
                "z": vc.get("z", 0),
            }

            # Parse the visual config
            config_str = vc.get("config", "{}")
            if isinstance(config_str, str):
                try:
                    config = json.loads(config_str)
                except json.JSONDecodeError:
                    config = {}
            else:
                config = config_str or {}

            single_visual = config.get("singleVisual", {})
            visual["visualType"] = single_visual.get("visualType", "unknown")
            visual["title"] = ""

            # Try to extract title
            objects = single_visual.get("objects", {})
            title_obj = objects.get("title", [{}])
            if title_obj and isinstance(title_obj, list) and len(title_obj) > 0:
                props = title_obj[0].get("properties", {})
                text = props.get("text", {})
                if isinstance(text, dict):
                    expr = text.get("expr", {})
                    literal = expr.get("Literal", {})
                    visual["title"] = literal.get("Value", "").strip("'")

            # Extract data field references (projections)
            projections = single_visual.get("projections", {})
            visual["dataFields"] = {}
            for role, fields in projections.items():
                visual["dataFields"][role] = []
                for field in fields:
                    query_ref = field.get("queryRef", "")
                    if query_ref:
                        visual["dataFields"][role].append(query_ref)

            # Parse visual-level filters
            filters_str = vc.get("filters", "[]")
            if isinstance(filters_str, str):
                try:
                    visual["filters"] = json.loads(filters_str)
                except json.JSONDecodeError:
                    visual["filters"] = []
            else:
                visual["filters"] = filters_str if filters_str else []

            page["visuals"].append(visual)

        pages.append(page)

    return pages


def extract_single_pbix(pbix_path):
    """Extract all information from a single .pbix file.

    Returns a dict with all extracted data ready for JSON serialization.
    """
    pbix_path = str(pbix_path)
    result = {
        "file": os.path.basename(pbix_path),
        "file_path": pbix_path,
    }

    # --- Data Model extraction via pbixray ---
    try:
        model = PBIXRay(pbix_path)

        # tables is a StringArray of table names, not a DataFrame
        result["tables"] = list(model.tables) if model.tables is not None else []

        # schema has columns: TableName, ColumnName, PandasDataType
        result["schema"] = _df_to_serializable(model.schema)

        # statistics has columns per table/column with row counts etc.
        result["statistics"] = _df_to_serializable(model.statistics)

        # relationships: FromTableName, FromColumnName, ToTableName, ToColumnName, etc.
        result["relationships"] = _df_to_serializable(model.relationships)

        # dax_measures: TableName, Name, Expression, DisplayFolder, Description
        result["dax_measures"] = _df_to_serializable(model.dax_measures)

        # dax_columns: TableName, ColumnName, Expression
        result["dax_columns"] = _df_to_serializable(model.dax_columns)

        # dax_tables: TableName, Expression (calculated tables)
        result["dax_tables"] = _df_to_serializable(model.dax_tables)

        # power_query: TableName, Expression (M code)
        result["power_query"] = _df_to_serializable(model.power_query)

        result["m_parameters"] = _df_to_serializable(model.m_parameters)
        result["rls"] = _df_to_serializable(model.rls)

        # size is an integer (bytes), not a DataFrame
        result["size"] = model.size if isinstance(model.size, (int, float)) else 0

        # metadata: Name, Value pairs
        result["metadata"] = _df_to_serializable(model.metadata)

    except Exception as e:
        result["data_model_error"] = str(e)

    # --- Report Layout extraction ---
    layout_data = _extract_report_layout(pbix_path)
    result["report_pages"] = _parse_report_pages(layout_data)
    result["archive_contents"] = layout_data.get("archive_contents", [])

    # Report-level filters and bookmarks
    if "layout" in layout_data:
        layout = layout_data["layout"]
        config = layout.get("config", "{}")
        if isinstance(config, str):
            try:
                config = json.loads(config)
            except json.JSONDecodeError:
                config = {}
        result["report_config"] = {
            "theme": config.get("theme", {}),
            "activeSectionIndex": config.get("activeSectionIndex", 0),
        }

        # Bookmarks
        bookmarks = layout.get("config", {})
        if isinstance(bookmarks, str):
            try:
                bookmarks = json.loads(bookmarks)
            except json.JSONDecodeError:
                bookmarks = {}
        result["bookmarks"] = bookmarks.get("bookmarks", [])

        # Report-level filters
        report_filters = layout.get("filters", "[]")
        if isinstance(report_filters, str):
            try:
                result["report_filters"] = json.loads(report_filters)
            except json.JSONDecodeError:
                result["report_filters"] = []
        else:
            result["report_filters"] = report_filters or []

    return result


def extract_all(input_dir, output_dir):
    """Extract all .pbix files from input_dir and save JSON to output_dir."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pbix_files = sorted(input_path.glob("*.pbix"))
    if not pbix_files:
        print(f"No .pbix files found in {input_dir}")
        return []

    results = []
    for pbix_file in pbix_files:
        print(f"  Extracting: {pbix_file.name}")
        try:
            data = extract_single_pbix(pbix_file)
            out_file = output_path / f"{pbix_file.stem}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            print(f"    -> {out_file}")
            results.append(data)
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append({"file": pbix_file.name, "error": str(e)})

    return results


if __name__ == "__main__":
    extract_all("input", "output/extracted")
