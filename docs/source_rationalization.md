# Source Rationalization Notes

## Purpose

This note translates the legacy Excel layer into migration-oriented buckets.

The goal is not to preserve every workbook. The goal is to identify:
- likely IAM / VFondos data
- likely IVSA / VBOLSA data
- commercial overlay files
- helper / technical artifacts
- candidates that should disappear once SQL access arrives

## Recommended framing

### Category A — likely direct operational extracts from real source systems
These are the strongest candidates to replace with direct SQL queries.

#### IAM / VFondos leaning
- `Boletos IAM.xlsm`
- `Boletos IAM3.xlsx`
- `Boletos IAM 4.xlsx`
- `Boletos IAM 5.xlsx`
- `Boletos IAM 6.xlsx`
- `Canales de operacion.xlsx` for IAM channel-related facts

Likely business meaning:
- fund operations
- investor / cuotapartista activity
- channel activity
- period-level fact exports

#### IVSA / VBOLSA leaning
- `Boletos IVSA.xlsx` (2023)
- `Boletos IVSA.xlsx` (2022 copy used for calendar/helper content)
- `Saldos IVSA.xlsx`
- `cheques operados.xlsx`

Likely business meaning:
- securities / brokerage tickets
- balances by account/date/currency
- CPD / cheque operations
- trade fee and volume facts

#### Bind Inversiones operational extracts
- `Boletos Bind Inversiones.xlsx`
- `Boletos Bind Inversiones 2.xlsx`
- `Boletos Bind Inversiones 3.xlsx`
- `Boletos Bind Inversiones 4.xlsx`
- `Boletos Bind Inversiones 5.xlsx`
- `Boletos Bind Inversiones 6.xlsx`

Interpretation:
- these look like partitioned exports of the same logical operational fact domain
- they are strong candidates to collapse into one canonical SQL fact instead of keeping workbook-by-workbook lineage

## Category B — likely master / mapping / commercial dimension files
These may still matter conceptually, but often as dimensions rather than raw replicated tables.

- `Estructura Comercial.xlsx`
- `clientes Bind Inversiones.xlsx`

Likely business meaning:
- banca
- officer assignments
- traders
- regions
- products
- customer crosswalks
- IAM / IVSA client model links

These should probably survive as **clean dimensions or business mappings**, not as loosely copied spreadsheet tabs.

## Category C — commercial planning / target / management overlay files
These are important to reporting, but they are not the same thing as upstream operational systems.

- `PEA 2023.xlsx`
- `Boletos Bind UY.xlsx`
- `inflacion.xlsx`
- `Ajustes RV.xlsx`

Likely business meaning:
- targets / quotas / budget overlays
- commercial adjustments
- external or side-market contribution
- inflation correction support

These may need a curated home in SQL, but usually as small controlled business tables rather than direct system ingestion.

## Category D — helper / calendar / technical artifacts
These are usually not worth rebuilding one-to-one.

Examples visible from the PBIX and workbook profiling:
- calendar sheets inside operational workbooks
- appended workbook fragments
- local date tables inside the PBIX
- small helper tables embedded directly in Power Query

These should usually be replaced by:
- one shared date dimension
- one canonical operational fact per business process
- explicit dimensions for product, officer, region, channel, and entity

## High-value simplification opportunities

### 1. Collapse fragmented workbook families
Strong candidates:
- `Boletos Bind Inversiones` + `2..6`
- `Boletos IAM` + `3..6`

These look like physical fragmentation of one logical dataset.

### 2. Separate real facts from commercial overlays
Operational facts should come from IAM / IVSA SQL.
Commercial overlays should be loaded as small maintained dimension/fact tables.

### 3. Replace workbook calendars and local date tables
Use one canonical date dimension.

### 4. Keep business mappings, not spreadsheet structure
For example:
- banca
- officer
- trader
- region
- product grouping
- client crosswalks

These are likely still needed, but not in their current workbook-driven shape.

## Practical target model direction

### Canonical dimensions
- client / account / investor
- legal entity
- officer / trader / banca / region
- product / fund / instrument / asset class
- channel
- date

### Canonical facts
- IAM operations
- IVSA operations / boletos
- balances / positions
- CPD / cheque operations
- commercial targets / adjustments where truly needed

## Decision rule

A legacy Excel-fed PBIX table should only be rebuilt if it represents at least one of these:
- a real business entity
- a real operational event
- a business-controlled overlay that still has no upstream owner

If it is only:
- an append fragment
- an export slice
- a helper calendar
- a workaround for missing SQL access

then it should usually be removed from the future design.
