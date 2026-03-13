"""
Data Model Analyzer — Consolidates tables and relationships across all extracted reports.

Identifies:
- All unique tables and their columns across all reports
- Duplicate/fragmented tables (same data from different Excel sources)
- Relationship graph between tables
- Tables that can be consolidated when migrating to SQL
"""

import json
import os
from collections import defaultdict
from pathlib import Path

import networkx as nx
from tabulate import tabulate


def _load_extracted(extracted_dir):
    """Load all extracted JSON files from the extraction step."""
    extracted_path = Path(extracted_dir)
    results = []
    for json_file in sorted(extracted_path.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            results.append(json.load(f))
    return results


def _build_table_inventory(extractions):
    """Build a consolidated inventory of all tables across all reports."""
    tables = {}  # table_name -> {columns, sources, reports}

    for extraction in extractions:
        report_name = extraction.get("file", "unknown")

        # From schema (column-level detail)
        # pbixray columns: TableName, ColumnName, PandasDataType
        for row in extraction.get("schema", []):
            table_name = row.get("TableName", "")
            col_name = row.get("ColumnName", "")
            data_type = row.get("PandasDataType", "")
            if not table_name:
                continue

            if table_name not in tables:
                tables[table_name] = {
                    "columns": {},
                    "reports": set(),
                    "row_counts": {},
                    "power_query": {},
                }
            tables[table_name]["reports"].add(report_name)
            if col_name:
                tables[table_name]["columns"][col_name] = data_type

        # From tables list (list of table name strings from pbixray)
        table_list = extraction.get("tables", [])
        for table_name in table_list:
            if isinstance(table_name, str):
                if table_name not in tables:
                    tables[table_name] = {
                        "columns": {},
                        "reports": set(),
                        "row_counts": {},
                        "power_query": {},
                    }
                tables[table_name]["reports"].add(report_name)

        # Row counts from statistics
        # pbixray statistics columns: TableName, ColumnName, RowCount, etc.
        seen_tables = set()
        for row in extraction.get("statistics", []):
            table_name = row.get("TableName", "")
            row_count = row.get("RowCount", 0)
            if table_name and table_name in tables and table_name not in seen_tables:
                tables[table_name]["row_counts"][report_name] = row_count
                seen_tables.add(table_name)

        # From power query (M expressions showing data sources)
        # pbixray columns: TableName, Expression
        for row in extraction.get("power_query", []):
            table_name = row.get("TableName", "")
            expression = row.get("Expression", "")
            if table_name and table_name in tables:
                tables[table_name]["power_query"][report_name] = expression

    # Convert sets to lists for JSON serialization
    for t in tables.values():
        t["reports"] = sorted(t["reports"])

    return tables


def _detect_source_type(m_expression):
    """Analyze a Power Query M expression to determine the data source type."""
    if not m_expression:
        return "unknown"
    m_lower = m_expression.lower()
    if "excel.workbook" in m_lower or "excel.currentworkbook" in m_lower:
        return "excel"
    if "sql.database" in m_lower or "sql.databases" in m_lower:
        return "sql_server"
    if "odbc.datasource" in m_lower or "odbc.query" in m_lower:
        return "odbc"
    if "odata.feed" in m_lower:
        return "odata"
    if "web.contents" in m_lower or "web.page" in m_lower:
        return "web"
    if "csv.document" in m_lower or "file.contents" in m_lower:
        return "csv/file"
    if "sharepoint" in m_lower:
        return "sharepoint"
    if "activedirectory" in m_lower:
        return "active_directory"
    if "mysql.database" in m_lower:
        return "mysql"
    if "postgresql.database" in m_lower:
        return "postgresql"
    if "oracle.database" in m_lower:
        return "oracle"
    # DAX calculated tables
    if m_expression.strip().startswith("="):
        return "dax_calculated"
    return "other"


def _classify_tables(tables):
    """Classify tables by their data source type."""
    classified = defaultdict(list)
    for table_name, info in tables.items():
        source_types = set()
        for report, m_expr in info.get("power_query", {}).items():
            source_types.add(_detect_source_type(m_expr))
        if not source_types:
            source_types = {"unknown"}
        for st in source_types:
            classified[st].append(table_name)
    return dict(classified)


def _build_relationship_graph(extractions):
    """Build a NetworkX graph of table relationships across all reports."""
    G = nx.DiGraph()

    for extraction in extractions:
        report_name = extraction.get("file", "unknown")
        for rel in extraction.get("relationships", []):
            # pbixray columns: FromTableName, FromColumnName, ToTableName, ToColumnName,
            #                   Cardinality, CrossFilteringBehavior, IsActive
            from_table = rel.get("FromTableName", "")
            to_table = rel.get("ToTableName", "")
            from_col = rel.get("FromColumnName", "")
            to_col = rel.get("ToColumnName", "")
            cardinality = rel.get("Cardinality", "")
            cross_filter = rel.get("CrossFilteringBehavior", "")

            if from_table and to_table:
                G.add_node(from_table)
                G.add_node(to_table)
                G.add_edge(
                    from_table,
                    to_table,
                    from_column=from_col,
                    to_column=to_col,
                    cardinality=str(cardinality),
                    cross_filter=str(cross_filter),
                    report=report_name,
                )

    return G


def _find_duplicate_candidates(tables):
    """Find tables that might be duplicates (same columns, different names)."""
    col_signatures = defaultdict(list)
    for table_name, info in tables.items():
        col_set = frozenset(info["columns"].keys())
        if len(col_set) > 0:
            col_signatures[col_set].append(table_name)

    duplicates = {}
    for cols, table_names in col_signatures.items():
        if len(table_names) > 1:
            duplicates[", ".join(sorted(table_names))] = {
                "tables": sorted(table_names),
                "shared_columns": sorted(cols),
                "column_count": len(cols),
            }

    return duplicates


def analyze_model(extracted_dir, output_dir):
    """Run the full data model analysis."""
    extractions = _load_extracted(extracted_dir)
    if not extractions:
        print("  No extracted data found. Run extract_pbix first.")
        return None

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build table inventory
    tables = _build_table_inventory(extractions)
    classified = _classify_tables(tables)
    duplicates = _find_duplicate_candidates(tables)
    rel_graph = _build_relationship_graph(extractions)

    # Build consolidated model
    model = {
        "summary": {
            "total_tables": len(tables),
            "total_reports": len(extractions),
            "source_types": {k: len(v) for k, v in classified.items()},
            "total_relationships": rel_graph.number_of_edges(),
            "potential_duplicates": len(duplicates),
        },
        "tables": {},
        "source_classification": classified,
        "potential_duplicates": duplicates,
        "relationships": [],
    }

    # Serialize table info
    for table_name, info in sorted(tables.items()):
        source_types = set()
        for m_expr in info.get("power_query", {}).values():
            source_types.add(_detect_source_type(m_expr))
        model["tables"][table_name] = {
            "columns": info["columns"],
            "column_count": len(info["columns"]),
            "used_in_reports": info["reports"],
            "report_count": len(info["reports"]),
            "row_counts": info["row_counts"],
            "source_types": sorted(source_types) if source_types else ["unknown"],
            "power_query_expressions": info["power_query"],
        }

    # Serialize relationships
    for u, v, data in rel_graph.edges(data=True):
        model["relationships"].append({
            "from_table": u,
            "to_table": v,
            "from_column": data.get("from_column", ""),
            "to_column": data.get("to_column", ""),
            "cardinality": data.get("cardinality", ""),
            "cross_filter": data.get("cross_filter", ""),
            "report": data.get("report", ""),
        })

    # Save the consolidated model
    out_file = output_path / "consolidated_model.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2, default=str)

    # Print summary
    print(f"\n  Model Analysis Complete:")
    print(f"    Tables: {model['summary']['total_tables']}")
    print(f"    Reports analyzed: {model['summary']['total_reports']}")
    print(f"    Relationships: {model['summary']['total_relationships']}")
    print(f"    Potential duplicates: {model['summary']['potential_duplicates']}")
    print(f"\n  Source types:")
    for src, count in model["summary"]["source_types"].items():
        print(f"    {src}: {count} tables")

    if duplicates:
        print(f"\n  Potential duplicate table groups:")
        for group_name, info in duplicates.items():
            print(f"    {group_name} ({info['column_count']} shared columns)")

    print(f"\n    -> {out_file}")
    return model


if __name__ == "__main__":
    analyze_model("output/extracted", "output/model")
