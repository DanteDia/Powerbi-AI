"""
SQL Readiness Builder — Generates pre-SQL-access planning artifacts from the
existing PBIX and Excel analysis outputs.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

import click


DOMAIN_RULES = [
    ("technical", ["LocalDateTable", "DateTableTemplate"]),
    ("calendar", ["Calendario", "Date"]),
    ("iam", ["IAM", "Fondos", "Cuotapartista"]),
    ("ivsa", ["IVSA", "Bolsa", "CPD", "cheques", "Comitente", "Saldo"]),
    ("commercial", [
        "Banca", "Oficial", "Trader", "Region", "Producto", "PEA",
        "Presupuesto", "Seguimiento", "Embajadores", "Clusters", "Empresas",
        "Referidos", "Canal", "Celula"
    ]),
]


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _lower_join(*values):
    return " ".join(str(v) for v in values if v).lower()


def _infer_domain(table_name, table_info, source_info):
    haystack = _lower_join(
        table_name,
        " ".join(table_info.get("columns", {}).keys()),
        source_info.get("file_path", "") if source_info else "",
    )

    for domain, markers in DOMAIN_RULES:
        if any(marker.lower() in haystack for marker in markers):
            return domain
    return "shared_or_unknown"


def _infer_action(table_name, table_info, source_info, domain):
    name = table_name.lower()
    source_path = (source_info or {}).get("file_path", "").lower()

    if "localdatatable" in table_name.lower() or "datetabletemplate" in table_name.lower():
        return "drop_powerbi_auto_date"
    if table_name.lower().startswith("calendario"):
        return "replace_with_shared_date_dimension"
    if any(token in name for token in ["operaciones", "boletos", "saldos", "cpd", "resumen op"]):
        return "replace_with_sql_fact"
    if any(token in name for token in ["banca", "oficial", "trader", "region", "producto", "empresa", "clientes", "modelo"]):
        return "replace_with_sql_dimension"
    if any(token in name for token in ["pea", "presupuesto", "seguimiento", "embajadores", "inflación", "inflacion", "referidos", "ajustes", "cluster"]):
        return "keep_as_business_overlay"
    if source_path.endswith((".xlsx", ".xlsm")) and table_info.get("source_types") == ["excel"]:
        return "review_after_sql_access"
    if table_info.get("source_types") == ["other"]:
        return "keep_as_small_manual_mapping"
    return "review_after_sql_access"


def _infer_priority(action, domain):
    if action == "replace_with_sql_fact":
        return "high"
    if action in {"replace_with_sql_dimension", "keep_as_business_overlay", "replace_with_shared_date_dimension"}:
        return "medium"
    if domain == "technical" or action == "drop_powerbi_auto_date":
        return "low"
    return "medium"


def _build_table_plan(model, migration_meta):
    tables = model.get("tables", {})
    source_mapping = migration_meta.get("source_mapping", {})
    plan = []

    for table_name, table_info in sorted(tables.items()):
        source_info = source_mapping.get(table_name, {})
        domain = _infer_domain(table_name, table_info, source_info)
        action = _infer_action(table_name, table_info, source_info, domain)
        priority = _infer_priority(action, domain)
        plan.append({
            "table": table_name,
            "domain": domain,
            "priority": priority,
            "recommended_action": action,
            "source_path": source_info.get("file_path", ""),
            "column_count": table_info.get("column_count", 0),
            "report_count": table_info.get("report_count", 0),
            "source_types": table_info.get("source_types", []),
        })

    return plan


def _top_complex_measures(dax_catalog, limit=15):
    measures = dax_catalog.get("measures", [])
    return [
        {
            "table": m.get("table", ""),
            "name": m.get("name", ""),
            "complexity_score": m.get("complexity_score", 0),
            "sql_convertibility": m.get("sql_convertibility", "unknown"),
        }
        for m in measures[:limit]
    ]


def _readiness_summary(table_plan, model, dax_catalog, report_inventory):
    actions = Counter(item["recommended_action"] for item in table_plan)
    domains = Counter(item["domain"] for item in table_plan)
    return {
        "table_count": len(table_plan),
        "relationship_count": model.get("summary", {}).get("total_relationships", 0),
        "measure_count": dax_catalog.get("summary", {}).get("unique_measures", 0),
        "report_page_count": report_inventory.get("summary", {}).get("total_pages", 0),
        "visual_count": report_inventory.get("summary", {}).get("total_visuals", 0),
        "domains": dict(domains),
        "actions": dict(actions),
    }


def _render_markdown(summary, table_plan, top_measures):
    by_action = defaultdict(list)
    for item in table_plan:
        by_action[item["recommended_action"]].append(item)

    lines = [
        "# SQL Access Readiness Plan",
        "",
        "This document captures everything that can be prepared before the real SQL schema is available.",
        "",
        "## Current state",
        "",
        f"- Tables inventoried: {summary['table_count']}",
        f"- Relationships inventoried: {summary['relationship_count']}",
        f"- Measures inventoried: {summary['measure_count']}",
        f"- Report pages inventoried: {summary['report_page_count']}",
        f"- Visuals inventoried: {summary['visual_count']}",
        "",
        "## Working rule",
        "",
        "Do not recreate the legacy Excel layer table-by-table unless the table represents a real business entity, real operational fact, or a business-owned overlay that still has no upstream owner.",
        "",
        "## Domain split",
        "",
    ]

    for domain, count in sorted(summary["domains"].items()):
        lines.append(f"- {domain}: {count}")

    lines.extend([
        "",
        "## Recommended actions summary",
        "",
    ])
    for action, count in sorted(summary["actions"].items()):
        lines.append(f"- {action}: {count}")

    lines.extend([
        "",
        "## High-priority tables to replace with SQL facts",
        "",
        "| Table | Domain | Priority | Source |",
        "|---|---|---|---|",
    ])
    for item in sorted(by_action.get("replace_with_sql_fact", []), key=lambda x: x["table"]):
        lines.append(f"| {item['table']} | {item['domain']} | {item['priority']} | {item['source_path'] or '-'} |")

    lines.extend([
        "",
        "## Dimension candidates to preserve conceptually",
        "",
        "| Table | Domain | Action | Source |",
        "|---|---|---|---|",
    ])
    for item in sorted(by_action.get("replace_with_sql_dimension", []), key=lambda x: x["table"]):
        lines.append(f"| {item['table']} | {item['domain']} | {item['recommended_action']} | {item['source_path'] or '-'} |")

    lines.extend([
        "",
        "## Business overlays likely to remain curated",
        "",
        "| Table | Domain | Source |",
        "|---|---|---|",
    ])
    for item in sorted(by_action.get("keep_as_business_overlay", []), key=lambda x: x["table"]):
        lines.append(f"| {item['table']} | {item['domain']} | {item['source_path'] or '-'} |")

    lines.extend([
        "",
        "## Low-value technical artifacts",
        "",
        "| Table | Recommended action |",
        "|---|---|",
    ])
    low_value = by_action.get("drop_powerbi_auto_date", []) + by_action.get("replace_with_shared_date_dimension", [])
    for item in sorted(low_value, key=lambda x: x["table"]):
        lines.append(f"| {item['table']} | {item['recommended_action']} |")

    lines.extend([
        "",
        "## Complex measures to protect during rebuild",
        "",
        "| Measure | Complexity | SQL difficulty |",
        "|---|---:|---|",
    ])
    for measure in top_measures:
        lines.append(f"| {measure['table']}[{measure['name']}] | {measure['complexity_score']} | {measure['sql_convertibility']} |")

    lines.extend([
        "",
        "## Questions to answer once SQL access arrives",
        "",
        "1. Which SQL tables are the true operational sources for IAM facts?",
        "2. Which SQL tables are the true operational sources for IVSA facts?",
        "3. What are the durable business keys for client, investor, comitente, product, officer, and channel?",
        "4. Which workbook overlays still need manual stewardship after SQL access?",
        "5. Which current PBIX calculations should move into SQL views versus stay in the semantic layer?",
        "6. Which report outputs depend on business rules that are not present in the upstream transactional schema?",
        "",
        "## Recommended next implementation steps",
        "",
        "1. Build a source-to-domain map for IAM vs IVSA entities.",
        "2. Trace the highest-value dashboards to the minimum canonical facts and dimensions they need.",
        "3. Review the complex measures first, because they are the biggest rebuild risk.",
        "4. Replace duplicate workbook families with a single canonical fact design once SQL tables are known.",
        "",
    ])

    return "\n".join(lines)


@click.command()
@click.option("--output-dir", default="output", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--docs-dir", default="docs", type=click.Path(file_okay=False, path_type=Path))
def main(output_dir, docs_dir):
    """Generate readiness artifacts from existing PBIX analysis outputs."""
    docs_dir.mkdir(parents=True, exist_ok=True)

    model = _load_json(output_dir / "model" / "consolidated_model.json")
    dax_catalog = _load_json(output_dir / "measures" / "dax_catalog.json")
    report_inventory = _load_json(output_dir / "reports" / "report_inventory.json")
    migration_meta = _load_json(output_dir / "sql" / "migration_metadata.json")

    table_plan = _build_table_plan(model, migration_meta)
    summary = _readiness_summary(table_plan, model, dax_catalog, report_inventory)
    top_measures = _top_complex_measures(dax_catalog)

    readiness_json = {
        "summary": summary,
        "table_plan": table_plan,
        "top_complex_measures": top_measures,
    }

    json_path = docs_dir / "sql_readiness.json"
    md_path = docs_dir / "sql_readiness_plan.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(readiness_json, f, indent=2, ensure_ascii=False)

    md_path.write_text(_render_markdown(summary, table_plan, top_measures), encoding="utf-8")

    print(f"Readiness JSON: {json_path}")
    print(f"Readiness Markdown: {md_path}")


if __name__ == "__main__":
    main()
