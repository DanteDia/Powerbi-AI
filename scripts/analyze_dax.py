"""
DAX & Measure Analyzer — Catalogs all DAX measures and calculated columns.

Produces:
- Complete measure inventory with DAX expressions
- Dependency mapping (which tables/columns each measure references)
- Calculated column inventory
- Complexity scoring for migration prioritization
"""

import json
import re
from collections import defaultdict
from pathlib import Path


# Common DAX functions for complexity scoring
DAX_AGGREGATIONS = {
    "SUM", "AVERAGE", "COUNT", "COUNTA", "COUNTBLANK", "COUNTROWS",
    "MIN", "MAX", "DISTINCTCOUNT",
}
DAX_TABLE_FUNCTIONS = {
    "FILTER", "ALL", "ALLEXCEPT", "VALUES", "DISTINCT", "SUMMARIZE",
    "ADDCOLUMNS", "SELECTCOLUMNS", "CALCULATETABLE", "TOPN",
    "GENERATE", "GENERATEALL", "CROSSJOIN", "UNION", "INTERSECT", "EXCEPT",
    "NATURALINNERJOIN", "NATURALLEFTOUTERJOIN", "DATATABLE", "TREATAS",
}
DAX_CONTEXT_MODIFIERS = {
    "CALCULATE", "CALCULATETABLE", "EARLIER", "EARLIEST",
    "USERELATIONSHIP", "CROSSFILTER", "KEEPFILTERS", "REMOVEFILTERS",
}
DAX_TIME_INTELLIGENCE = {
    "TOTALYTD", "TOTALQTD", "TOTALMTD",
    "SAMEPERIODLASTYEAR", "PREVIOUSYEAR", "PREVIOUSQUARTER", "PREVIOUSMONTH",
    "PREVIOUSDAY", "NEXTYEAR", "NEXTQUARTER", "NEXTMONTH", "NEXTDAY",
    "DATESYTD", "DATESQTD", "DATESMTD",
    "DATEADD", "DATESBETWEEN", "DATESINPERIOD",
    "STARTOFYEAR", "STARTOFQUARTER", "STARTOFMONTH",
    "ENDOFYEAR", "ENDOFQUARTER", "ENDOFMONTH",
    "PARALLELPERIOD", "OPENINGBALANCEMONTH", "CLOSINGBALANCEMONTH",
}


def _extract_table_references(dax_expression):
    """Extract table and column references from a DAX expression."""
    if not dax_expression:
        return [], []

    # Match 'TableName'[ColumnName] or TableName[ColumnName]
    col_refs = re.findall(r"'?([^'\[\]]+)'?\[([^\]]+)\]", dax_expression)
    tables = sorted(set(t.strip() for t, c in col_refs))
    columns = sorted(set(f"{t.strip()}[{c}]" for t, c in col_refs))

    return tables, columns


def _extract_dax_functions(dax_expression):
    """Extract DAX function names used in an expression."""
    if not dax_expression:
        return []
    # Match function calls: FUNCTIONNAME(
    functions = re.findall(r"\b([A-Z][A-Z0-9_.]+)\s*\(", dax_expression.upper())
    return sorted(set(functions))


def _score_complexity(dax_expression, functions_used):
    """Score the complexity of a DAX expression for migration difficulty."""
    if not dax_expression:
        return 0

    score = 0
    func_set = set(functions_used)

    # Base complexity by expression length
    score += min(len(dax_expression) // 100, 3)

    # Nesting depth (count parentheses nesting)
    max_depth = 0
    depth = 0
    for ch in dax_expression:
        if ch == "(":
            depth += 1
            max_depth = max(max_depth, depth)
        elif ch == ")":
            depth -= 1
    score += min(max_depth, 5)

    # Function categories add complexity
    if func_set & DAX_CONTEXT_MODIFIERS:
        score += 3  # CALCULATE etc. are hard to translate to SQL
    if func_set & DAX_TIME_INTELLIGENCE:
        score += 2  # Time intelligence needs SQL window functions
    if func_set & DAX_TABLE_FUNCTIONS:
        score += 2
    if "VAR" in dax_expression.upper():
        score += 1
    if "SWITCH" in func_set or "IF" in func_set:
        score += 1

    return min(score, 10)  # Cap at 10


def _classify_sql_convertibility(functions_used, complexity_score):
    """Classify how easily a measure can be converted to SQL."""
    func_set = set(functions_used)

    # Pure aggregations are easy
    if func_set <= DAX_AGGREGATIONS | {"DIVIDE", "IF", "SWITCH", "BLANK"}:
        return "easy"

    # Time intelligence and context modifiers are hard
    if func_set & DAX_TIME_INTELLIGENCE or func_set & DAX_CONTEXT_MODIFIERS:
        if complexity_score >= 6:
            return "hard"
        return "medium"

    if complexity_score >= 7:
        return "hard"
    if complexity_score >= 4:
        return "medium"

    return "easy"


def _load_extracted(extracted_dir):
    """Load all extracted JSON files."""
    results = []
    for json_file in sorted(Path(extracted_dir).glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            results.append(json.load(f))
    return results


def analyze_dax(extracted_dir, output_dir):
    """Analyze all DAX measures and calculated columns."""
    extractions = _load_extracted(extracted_dir)
    if not extractions:
        print("  No extracted data found. Run extract_pbix first.")
        return None

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    all_measures = []
    all_calc_columns = []
    all_calc_tables = []
    table_dependencies = defaultdict(set)  # measure -> set of tables referenced
    conversion_summary = {"easy": 0, "medium": 0, "hard": 0}

    for extraction in extractions:
        report_name = extraction.get("file", "unknown")

        # Process DAX measures
        # pbixray columns: TableName, Name, Expression, DisplayFolder, Description
        for measure in extraction.get("dax_measures", []):
            name = measure.get("Name", "")
            table = measure.get("TableName", "")
            expression = measure.get("Expression", "")

            tables_ref, columns_ref = _extract_table_references(expression)
            functions = _extract_dax_functions(expression)
            complexity = _score_complexity(expression, functions)
            convertibility = _classify_sql_convertibility(functions, complexity)
            conversion_summary[convertibility] += 1

            entry = {
                "name": name,
                "table": table,
                "expression": expression,
                "report": report_name,
                "referenced_tables": tables_ref,
                "referenced_columns": columns_ref,
                "dax_functions": functions,
                "complexity_score": complexity,
                "sql_convertibility": convertibility,
            }
            all_measures.append(entry)

            for t in tables_ref:
                table_dependencies[f"{table}[{name}]"].add(t)

        # Process calculated columns
        # pbixray columns: TableName, ColumnName, Expression
        for col in extraction.get("dax_columns", []):
            name = col.get("ColumnName", "")
            table = col.get("TableName", "")
            expression = col.get("Expression", "")

            tables_ref, columns_ref = _extract_table_references(expression)
            functions = _extract_dax_functions(expression)
            complexity = _score_complexity(expression, functions)

            entry = {
                "name": name,
                "table": table,
                "expression": expression,
                "report": report_name,
                "referenced_tables": tables_ref,
                "referenced_columns": columns_ref,
                "dax_functions": functions,
                "complexity_score": complexity,
            }
            all_calc_columns.append(entry)

        # Process calculated tables
        # pbixray columns: TableName, Expression
        for tbl in extraction.get("dax_tables", []):
            name = tbl.get("TableName", "")
            expression = tbl.get("Expression", "")

            tables_ref, columns_ref = _extract_table_references(expression)
            functions = _extract_dax_functions(expression)

            entry = {
                "name": name,
                "expression": expression,
                "report": report_name,
                "referenced_tables": tables_ref,
                "dax_functions": functions,
            }
            all_calc_tables.append(entry)

    # Deduplicate measures (same measure name + expression across reports)
    unique_measures = {}
    for m in all_measures:
        key = (m["table"], m["name"], m["expression"])
        if key not in unique_measures:
            unique_measures[key] = m
            unique_measures[key]["found_in_reports"] = [m["report"]]
        else:
            unique_measures[key]["found_in_reports"].append(m["report"])

    # Build output
    result = {
        "summary": {
            "total_measures": len(all_measures),
            "unique_measures": len(unique_measures),
            "calculated_columns": len(all_calc_columns),
            "calculated_tables": len(all_calc_tables),
            "sql_conversion_difficulty": conversion_summary,
        },
        "measures": sorted(
            unique_measures.values(),
            key=lambda x: (-x["complexity_score"], x["table"], x["name"]),
        ),
        "calculated_columns": sorted(
            all_calc_columns,
            key=lambda x: (-x["complexity_score"], x["table"], x["name"]),
        ),
        "calculated_tables": all_calc_tables,
        "dependency_map": {
            k: sorted(v) for k, v in table_dependencies.items()
        },
    }

    # Save
    out_file = output_path / "dax_catalog.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)

    # Print summary
    summary = result["summary"]
    print(f"\n  DAX Analysis Complete:")
    print(f"    Total measures: {summary['total_measures']}")
    print(f"    Unique measures: {summary['unique_measures']}")
    print(f"    Calculated columns: {summary['calculated_columns']}")
    print(f"    Calculated tables: {summary['calculated_tables']}")
    print(f"\n  SQL Conversion Difficulty:")
    for level, count in summary["sql_conversion_difficulty"].items():
        print(f"    {level}: {count} measures")

    # Show top complex measures
    complex_measures = [m for m in result["measures"] if m["complexity_score"] >= 5]
    if complex_measures:
        print(f"\n  Most complex measures (score >= 5):")
        for m in complex_measures[:10]:
            print(f"    [{m['complexity_score']}/10] {m['table']}[{m['name']}]"
                  f" ({m['sql_convertibility']})")

    print(f"\n    -> {out_file}")
    return result


if __name__ == "__main__":
    analyze_dax("output/extracted", "output/measures")
