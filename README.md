# Powerbi-AI

Legacy Power BI migration workspace for understanding a large manual-reporting model before the bank receives direct SQL access.

## Repository purpose

This repo is not trying to reproduce every Excel source as a permanent SQL table.

The current goal is to:
- understand what the legacy PBIX actually does
- identify which parts come from the two real upstream platforms
- separate true business entities from temporary spreadsheet workarounds
- prepare a cleaner SQL-backed semantic model and dashboard rebuild plan

## Current business context

The existing Power BI file was built over several years by a non-technical team.

Because the team did not have direct SQL access to the upstream operational systems, they created many manually refreshed Excel files that act as ad hoc replicas of operational data. The Power BI model therefore contains many redundant and fragmented tables.

The two real upstream source domains are:
- **VFondos / IAM**: internal naming for the funds side
- **VBOLSA / IVSA**: internal naming for the brokerage / capital markets side

In practical repo language:
- `IAM` tables usually map to the **Fondos** domain
- `IVSA` tables usually map to the **Bolsa** domain

## Source system interpretation

Based on public product information and the model itself:
- **VFondos** likely corresponds to the legacy `VisualFondos` / current `esco fondos` product family
- **VBOLSA** likely corresponds to the legacy `VisualBolsa` / current `esco bolsa` product family

That implies:
- **IAM** is the fund-management side of the business
- **IVSA** is the securities / broker side of the business

This matters because many Excel workbooks appear to be temporary exports from those systems rather than the true target data model.

## Working migration principle

The likely best path is:
1. understand the report outputs and business logic
2. understand which tables are canonical business entities versus manual reporting extracts
3. wait for SQL access to the real operational databases
4. design a smaller canonical model around IAM and IVSA domains
5. rebuild dashboards from the canonical model instead of recreating every spreadsheet table

In short: **understand first, rationalize second, rebuild third**.

## Current repo outputs

### PBIX analysis
Generated from the legacy report:
- [output/extracted/SEGUIMIENTO COMERCIAL BIND INVERSIONES 3.json](output/extracted/SEGUIMIENTO%20COMERCIAL%20BIND%20INVERSIONES%203.json)
- [output/model/consolidated_model.json](output/model/consolidated_model.json)
- [output/measures/dax_catalog.json](output/measures/dax_catalog.json)
- [output/reports/report_inventory.json](output/reports/report_inventory.json)
- [output/sql/migration_metadata.json](output/sql/migration_metadata.json)

Current high-level findings:
- 62 PBIX tables
- 69 relationships
- 82 measures
- 134 calculated columns
- 22 calculated tables
- 98 pages
- 479 visuals
- 37 Excel-backed tables identified in the PBIX

### Excel source documentation
Generated from the actual Excel files referenced by Power Query:
- [docs/excel_source_documentation.md](docs/excel_source_documentation.md)
- [docs/excel_source_profile.json](docs/excel_source_profile.json)

Current high-level findings:
- 22 accessible workbooks
- 83 profiled sheets
- 38 PBIX tables mapped to Excel sheets
- 20 workbooks with data-quality flags

### SQL readiness planning
Generated to prepare for SQL access before the actual source schema is available:
- [docs/sql_readiness_plan.md](docs/sql_readiness_plan.md)
- [docs/sql_readiness.json](docs/sql_readiness.json)
- [docs/source_rationalization.md](docs/source_rationalization.md)

## Important interpretation notes

Not all PBIX tables deserve a one-to-one SQL recreation.

Likely categories are:
- **true master/business entities**: clients, accounts, officers, traders, products, structures, regions
- **true operational facts**: tickets / boletos, balances, fund operations, CPD / cheques, channels
- **manual overlays**: budgets, targets, follow-up tables, inflation, small mapping tables
- **technical clutter**: duplicate append tables, local date tables, convenience tables created only for the PBIX

The target architecture should prefer the first two categories and sharply reduce the latter two.

## Key docs to read first

- [docs/repo_context.md](docs/repo_context.md)
- [docs/excel_source_documentation.md](docs/excel_source_documentation.md)
- [docs/sql_readiness_plan.md](docs/sql_readiness_plan.md)
- [output/model/consolidated_model.json](output/model/consolidated_model.json)
- [output/measures/dax_catalog.json](output/measures/dax_catalog.json)
- [output/reports/report_inventory.json](output/reports/report_inventory.json)

## Scripts

Core pipeline:
- [run_analysis.py](run_analysis.py)
- [scripts/extract_pbix.py](scripts/extract_pbix.py)
- [scripts/analyze_model.py](scripts/analyze_model.py)
- [scripts/analyze_dax.py](scripts/analyze_dax.py)
- [scripts/analyze_reports.py](scripts/analyze_reports.py)
- [scripts/generate_sql_model.py](scripts/generate_sql_model.py)

Excel profiling:
- [scripts/profile_excel_sources.py](scripts/profile_excel_sources.py)

Readiness planning:
- [scripts/build_sql_readiness.py](scripts/build_sql_readiness.py)

## Recommended next steps

1. group PBIX tables into IAM, IVSA, commercial dimensions, manual overlays, and technical clutter
2. build a canonical domain map for the future SQL sources
3. identify which DAX logic is business-critical and must survive the rebuild
4. prioritize dashboard recreation over spreadsheet-table recreation wherever possible
