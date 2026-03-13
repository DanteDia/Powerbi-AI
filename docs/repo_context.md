# Repository Context

## Why this repository exists

This repository exists to reverse-engineer and rationalize a legacy Power BI environment before a migration to direct SQL-backed reporting.

The existing Power BI solution works from an output perspective, but it was assembled over years without stable technical access to the real source systems. As a result, many manually refreshed Excel files became de facto source systems for reporting.

That means the current PBIX reflects:
- business logic that matters
- report outputs that matter
- a source-layer implementation that is often temporary, redundant, and inefficient

## Core migration assumption

The future target is **not** to recreate every current spreadsheet table in SQL.

The better target is to:
- preserve the real business meaning
- preserve the useful dashboard outputs
- redesign the data model around the real upstream systems once SQL access arrives

## Upstream source context

Two main operational systems sit behind the business process:

### 1. VFondos / IAM
This is the funds side of the business.

Interpretation used in this repo:
- `VFondos` is the upstream platform family
- `IAM` is the internal business/entity naming visible in the PBIX
- likely concepts include: fund investors, subscriptions, holdings, fund products, patrimony, fund fees, account officers, and channel activity

### 2. VBOLSA / IVSA
This is the brokerage / securities side of the business.

Interpretation used in this repo:
- `VBOLSA` is the upstream platform family
- `IVSA` is the internal business/entity naming visible in the PBIX
- likely concepts include: comitentes, boletos, trades, balances, custody, settlement, cheques / CPD, fees, and trader/commercial assignments

## What the Excel layer probably represents

The Excel workbooks appear to be a mixture of:
- direct exports from IAM / IVSA workflows
- manual append files split by year or workbook size
- commercial mapping files maintained by the team
- budget / target / follow-up sheets
- small helper or adjustment tables

So the Excel layer should usually be treated as a **legacy replication workaround**, not the final design blueprint.

## What should survive into the future design

### Must survive
- business definitions
- KPI definitions
- dashboard intent
- DAX logic that encodes real business rules
- entity relationships that reflect real business processes
- organizational dimensions such as officer, trader, banca, region, product grouping

### Should usually not survive one-to-one
- time-sliced workbook fragments like `Boletos Bind Inversiones 2..6`
- repeated appended extracts
- local Power BI date tables
- temporary commercial follow-up worksheets used only because SQL was unavailable
- spreadsheet-specific cleanup steps that only exist to compensate for export limitations

## Current reverse-engineering findings

From the PBIX:
- 62 tables
- 69 relationships
- 82 measures
- 134 calculated columns
- 22 calculated tables
- 98 report pages
- 479 visuals

From the actual Excel source profiling:
- 22 accessible workbooks
- 83 profiled sheets
- 38 PBIX tables mapped to workbook sheets
- 20 workbooks with data-quality flags

## Strategic implication

The correct migration mindset is:
- **do not clone the mess**
- **understand the mess**
- **extract the business meaning**
- **rebuild a smaller canonical model**

## Suggested canonical target layers

### Domain masters
- client / account / investor
- officer / trader / banca / region
- product / fund / instrument / asset class
- legal entity and company mappings

### Operational facts
- IAM fund operations
- IVSA trade / boleto operations
- balances and positions
- CPD / cheque operations
- channel activity

### Commercial overlays
- budgets / PEA
- targets
- segmentation and clusters
- adjustment tables that represent real business rules rather than technical artifacts

### Presentation layer
- dashboard-specific measures
- curated semantic model
- rebuilt reports with fewer dependencies and cleaner grain

## Working rule for future contributors

When deciding whether a legacy PBIX table should exist in the new model, ask:

1. Is it a real business entity or event?
2. Does it correspond to something likely available directly from IAM or IVSA SQL?
3. Is it just a manual export fragment or append helper?
4. Is it only there to support an old Power BI workaround?

If the answer is mostly 3 or 4, the table should usually **not** be recreated directly.

## Related artifacts

- [docs/excel_source_documentation.md](docs/excel_source_documentation.md)
- [docs/excel_source_profile.json](docs/excel_source_profile.json)
- [output/model/consolidated_model.json](output/model/consolidated_model.json)
- [output/measures/dax_catalog.json](output/measures/dax_catalog.json)
- [output/reports/report_inventory.json](output/reports/report_inventory.json)
- [output/sql/migration_metadata.json](output/sql/migration_metadata.json)
