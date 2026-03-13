"""
SQL Migration Generator — Produces SQL DDL from the consolidated Power BI data model.

Generates:
- CREATE TABLE statements for each table
- Suggested star/snowflake schema
- SQL views for calculated columns and simple measures
- Power Query M → SQL transformation notes
- Migration priority matrix
"""

import json
import re
from pathlib import Path


# Mapping from Power BI / VertiPaq data types to SQL Server types
PBI_TO_SQL_TYPES = {
    "String": "NVARCHAR(255)",
    "Int64": "BIGINT",
    "Double": "FLOAT",
    "Decimal": "DECIMAL(18, 4)",
    "Currency": "DECIMAL(18, 4)",
    "Boolean": "BIT",
    "DateTime": "DATETIME2",
    "Date": "DATE",
    "Time": "TIME",
    "Binary": "VARBINARY(MAX)",
    "Int32": "INT",
    "Int16": "SMALLINT",
    "Byte": "TINYINT",
    "Percentage": "FLOAT",
    # Fallbacks
    "string": "NVARCHAR(255)",
    "int64": "BIGINT",
    "double": "FLOAT",
    "decimal": "DECIMAL(18, 4)",
    "boolean": "BIT",
    "dateTime": "DATETIME2",
    "date": "DATE",
}


def _sanitize_sql_name(name):
    """Sanitize a name for use as a SQL identifier."""
    name = str(name) if name is not None else ""
    # Remove or replace characters not valid in SQL identifiers
    sanitized = re.sub(r"[^\w]", "_", name)
    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = "_" + sanitized
    return sanitized


def _map_data_type(pbi_type):
    """Map a Power BI data type to SQL Server data type."""
    return PBI_TO_SQL_TYPES.get(pbi_type, "NVARCHAR(255)")


def _classify_table_role(table_name, columns, relationships_as_from, relationships_as_to):
    """Classify a table's role in a star/snowflake schema."""
    has_date_cols = any(
        "date" in c.lower() or "time" in c.lower() or "year" in c.lower()
        for c in columns
    )
    has_numeric_cols = any(
        "amount" in c.lower() or "total" in c.lower() or "quantity" in c.lower()
        or "price" in c.lower() or "cost" in c.lower() or "revenue" in c.lower()
        or "sales" in c.lower() or "count" in c.lower()
        for c in columns
    )

    # Heuristics for star schema classification
    if has_date_cols and len(columns) <= 10 and "date" in table_name.lower():
        return "dimension_date"
    if len(relationships_as_to) > 2 and has_numeric_cols:
        return "fact"
    if len(relationships_as_from) > 0 and len(relationships_as_to) <= 1:
        return "dimension"
    if has_numeric_cols and len(columns) > 8:
        return "fact"

    return "dimension"


def _generate_ddl(table_name, columns, role):
    """Generate a CREATE TABLE DDL statement."""
    sql_name = _sanitize_sql_name(table_name)
    schema = "fact" if role == "fact" else "dim"

    lines = [f"CREATE TABLE [{schema}].[{sql_name}] ("]

    # Add a surrogate key
    lines.append(f"    [{sql_name}_SK] INT IDENTITY(1,1) PRIMARY KEY,")

    for col_name, col_type in sorted(columns.items()):
        sql_col = _sanitize_sql_name(col_name)
        sql_type = _map_data_type(col_type)
        lines.append(f"    [{sql_col}] {sql_type} NULL,")

    # Add audit columns
    lines.append(f"    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),")
    lines.append(f"    [_SourceFile] NVARCHAR(500) NULL")
    lines.append(f");")

    return "\n".join(lines)


def _generate_view_for_measure(measure_name, table_name, expression, convertibility):
    """Attempt to generate a SQL view for simple DAX measures."""
    sql_table = _sanitize_sql_name(table_name)
    sql_measure = _sanitize_sql_name(measure_name)

    if convertibility == "hard":
        return (
            f"-- [{sql_measure}]: Complex DAX measure — manual conversion required\n"
            f"-- Original DAX: {expression[:200]}{'...' if len(expression) > 200 else ''}\n"
        )

    # Simple conversion attempts
    expr_upper = expression.upper().strip()

    # SUM(Table[Column])
    sum_match = re.match(r"SUM\s*\(\s*'?(\w+)'?\[(\w+)\]\s*\)", expr_upper)
    if sum_match:
        ref_table = _sanitize_sql_name(sum_match.group(1))
        ref_col = _sanitize_sql_name(sum_match.group(2))
        return (
            f"-- Measure: {measure_name}\n"
            f"-- SELECT SUM([{ref_col}]) FROM [{ref_table}]\n"
        )

    # COUNT/COUNTROWS
    count_match = re.match(r"COUNTROWS\s*\(\s*'?(\w+)'?\s*\)", expr_upper)
    if count_match:
        ref_table = _sanitize_sql_name(count_match.group(1))
        return (
            f"-- Measure: {measure_name}\n"
            f"-- SELECT COUNT(*) FROM [{ref_table}]\n"
        )

    # DISTINCTCOUNT
    dc_match = re.match(r"DISTINCTCOUNT\s*\(\s*'?(\w+)'?\[(\w+)\]\s*\)", expr_upper)
    if dc_match:
        ref_table = _sanitize_sql_name(dc_match.group(1))
        ref_col = _sanitize_sql_name(dc_match.group(2))
        return (
            f"-- Measure: {measure_name}\n"
            f"-- SELECT COUNT(DISTINCT [{ref_col}]) FROM [{ref_table}]\n"
        )

    # AVERAGE
    avg_match = re.match(r"AVERAGE\s*\(\s*'?(\w+)'?\[(\w+)\]\s*\)", expr_upper)
    if avg_match:
        ref_table = _sanitize_sql_name(avg_match.group(1))
        ref_col = _sanitize_sql_name(avg_match.group(2))
        return (
            f"-- Measure: {measure_name}\n"
            f"-- SELECT AVG([{ref_col}]) FROM [{ref_table}]\n"
        )

    return (
        f"-- [{sql_measure}]: Needs manual conversion ({convertibility})\n"
        f"-- Original DAX: {expression[:200]}{'...' if len(expression) > 200 else ''}\n"
    )


def _extract_m_source_info(m_expression):
    """Extract connection details from Power Query M expression."""
    if not m_expression:
        return {}

    info = {}

    # Excel source
    excel_match = re.search(
        r'Excel\.Workbook\s*\(\s*File\.Contents\s*\(\s*"([^"]+)"', m_expression
    )
    if excel_match:
        info["type"] = "excel"
        info["file_path"] = excel_match.group(1)

    # SQL Server source
    sql_match = re.search(
        r'Sql\.Database\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"', m_expression
    )
    if sql_match:
        info["type"] = "sql_server"
        info["server"] = sql_match.group(1)
        info["database"] = sql_match.group(2)

    # Table/sheet reference
    table_match = re.search(r'\{[^}]*\[Name\s*=\s*"([^"]+)"', m_expression)
    if table_match:
        info["source_table"] = table_match.group(1)

    return info


def generate_sql_model(model_dir, measures_dir, output_dir):
    """Generate SQL DDL and migration artifacts from the consolidated model."""
    model_path = Path(model_dir) / "consolidated_model.json"
    measures_path = Path(measures_dir) / "dax_catalog.json"
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not model_path.exists():
        print("  No consolidated model found. Run analyze_model first.")
        return None

    with open(model_path, "r", encoding="utf-8") as f:
        model = json.load(f)

    # Load measures if available
    measures = {}
    if measures_path.exists():
        with open(measures_path, "r", encoding="utf-8") as f:
            measures = json.load(f)

    # Build relationship lookup
    rel_from = {}  # table -> [relationships where it's the 'from']
    rel_to = {}    # table -> [relationships where it's the 'to']
    for rel in model.get("relationships", []):
        ft = rel.get("from_table", "")
        tt = rel.get("to_table", "")
        rel_from.setdefault(ft, []).append(rel)
        rel_to.setdefault(tt, []).append(rel)

    # Classify tables and generate DDL
    ddl_statements = []
    table_classifications = {}
    source_mapping = {}

    ddl_statements.append("-- =============================================")
    ddl_statements.append("-- Power BI to SQL Migration — Auto-Generated DDL")
    ddl_statements.append("-- =============================================")
    ddl_statements.append("")
    ddl_statements.append("-- Create schemas")
    ddl_statements.append("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dim')")
    ddl_statements.append("    EXEC('CREATE SCHEMA dim');")
    ddl_statements.append("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'fact')")
    ddl_statements.append("    EXEC('CREATE SCHEMA fact');")
    ddl_statements.append("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'staging')")
    ddl_statements.append("    EXEC('CREATE SCHEMA staging');")
    ddl_statements.append("")

    for table_name, table_info in sorted(model.get("tables", {}).items()):
        columns = table_info.get("columns", {})
        role = _classify_table_role(
            table_name,
            columns,
            rel_from.get(table_name, []),
            rel_to.get(table_name, []),
        )
        table_classifications[table_name] = role

        ddl = _generate_ddl(table_name, columns, role)
        ddl_statements.append(ddl)
        ddl_statements.append("")

        # Extract source info from M expressions
        for report, m_expr in table_info.get("power_query_expressions", {}).items():
            source_info = _extract_m_source_info(m_expr)
            if source_info:
                source_mapping[table_name] = source_info

    # Generate FK constraints
    ddl_statements.append("-- =============================================")
    ddl_statements.append("-- Foreign Key Relationships")
    ddl_statements.append("-- =============================================")
    ddl_statements.append("")

    for rel in model.get("relationships", []):
        ft = rel.get("from_table", "")
        tt = rel.get("to_table", "")
        fc = rel.get("from_column", "")
        tc = rel.get("to_column", "")
        if ft and tt and fc and tc:
            from_schema = "fact" if table_classifications.get(ft) == "fact" else "dim"
            to_schema = "fact" if table_classifications.get(tt) == "fact" else "dim"
            fk_name = f"FK_{_sanitize_sql_name(ft)}_{_sanitize_sql_name(tt)}"
            ddl_statements.append(
                f"-- ALTER TABLE [{from_schema}].[{_sanitize_sql_name(ft)}]"
                f" ADD CONSTRAINT [{fk_name}]"
                f" FOREIGN KEY ([{_sanitize_sql_name(fc)}])"
                f" REFERENCES [{to_schema}].[{_sanitize_sql_name(tt)}]"
                f" ([{_sanitize_sql_name(tc)}]);"
            )
    ddl_statements.append("")

    # Generate measure SQL comments/views
    measure_sql = []
    measure_sql.append("-- =============================================")
    measure_sql.append("-- DAX Measures → SQL Conversion Notes")
    measure_sql.append("-- =============================================")
    measure_sql.append("")

    for m in measures.get("measures", []):
        sql_note = _generate_view_for_measure(
            m.get("name", ""),
            m.get("table", ""),
            m.get("expression", ""),
            m.get("sql_convertibility", "medium"),
        )
        measure_sql.append(sql_note)

    # Save DDL
    ddl_file = output_path / "migration_ddl.sql"
    with open(ddl_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ddl_statements))

    # Save measure SQL
    measures_file = output_path / "measure_conversions.sql"
    with open(measures_file, "w", encoding="utf-8") as f:
        f.write("\n".join(measure_sql))

    # Save migration metadata
    migration_meta = {
        "table_classifications": table_classifications,
        "source_mapping": source_mapping,
        "schema_summary": {
            "fact_tables": [t for t, r in table_classifications.items() if r == "fact"],
            "dimension_tables": [
                t for t, r in table_classifications.items()
                if r.startswith("dimension")
            ],
            "date_dimensions": [
                t for t, r in table_classifications.items()
                if r == "dimension_date"
            ],
        },
        "excel_sources": {
            t: info for t, info in source_mapping.items()
            if info.get("type") == "excel"
        },
    }

    meta_file = output_path / "migration_metadata.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(migration_meta, f, indent=2, default=str)

    # Print summary
    fact_count = len(migration_meta["schema_summary"]["fact_tables"])
    dim_count = len(migration_meta["schema_summary"]["dimension_tables"])
    date_count = len(migration_meta["schema_summary"]["date_dimensions"])
    excel_count = len(migration_meta["excel_sources"])

    print(f"\n  SQL Model Generation Complete:")
    print(f"    Fact tables: {fact_count}")
    print(f"    Dimension tables: {dim_count}")
    print(f"    Date dimensions: {date_count}")
    print(f"    Excel sources identified: {excel_count}")
    print(f"\n    -> {ddl_file}")
    print(f"    -> {measures_file}")
    print(f"    -> {meta_file}")

    return migration_meta


if __name__ == "__main__":
    generate_sql_model("output/model", "output/measures", "output/sql")
