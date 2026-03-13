# Fix: "Clientes nuevos y Operativos PARA COMITE" Dashboard

## Diagnosis

### Why `dif mes anterior` always shows zero

The measure `Clientes Operativos mes anterior` uses `PREVIOUSMONTH(Calendario[Dia])` to get
the previous month's client count. However, **there is no relationship** between
`Operaciones BI[Fecha]` and `Calendario[Dia]`.

The relationship `Operaciones BI[Fecha] -> nan[nan]` is **broken** (points to an auto-generated
LocalDateTable that was deleted or never existed).

Without this path, `PREVIOUSMONTH(Calendario[Dia])` cannot filter `Operaciones BI`,
so the measure returns the same value as `Clientes Operativos` → difference = 0.

### Why the slicers don't work for MoM

The page has `Calendario[Año]` and `Calendario[Mes]` slicers. If you select Año=2024 and
Mes=1 (January), the "previous month" is December 2023 — but the year filter **excludes**
all 2023 data. The slicer design contradicts the MoM comparison logic.

---

## Fix Steps

### Option A: Tabular Editor Script (Recommended — 1 click)

1. Open the .pbix in **Power BI Desktop**
2. Open **Tabular Editor** → connect to the running PBI Desktop instance
3. Go to **Advanced Scripting** tab
4. Paste the contents of `tabular_editor_script.cs` and press **F5** (Run)
5. Save back to PBI Desktop (**Ctrl+S** in Tabular Editor)

The script creates the relationship, calculated column, and all measures automatically.

### Option B: Manual Steps in Power BI Desktop

#### Step 1: Create the missing relationship

1. Go to **Model** view
2. Drag `Operaciones BI[Fecha]` to `Calendario[Dia]`
3. Verify: Cardinality = Many-to-One, Cross filter = Single direction

> **This is the critical fix.** Without it, no time intelligence on Calendario[Dia]
> can filter Operaciones BI data.

#### Step 2: Create calculated column `Calendario[MesAño]`

Go to the Calendario table → New Column:

```dax
MesAño = FORMAT(Calendario[Dia], "YYYY-MM")
```

This column enables a month-year slicer that doesn't block previous month calculations.

#### Step 3: Replace `Clientes Operativos mes anterior` measure

Select the existing measure and replace its DAX with:

```dax
Clientes Operativos mes anterior =
CALCULATE(
    DISTINCTCOUNT('Operaciones BI'[Nº Bind Inversiones]),
    DATEADD(Calendario[Dia], -1, MONTH),
    REMOVEFILTERS('Bind Inversiones'[fecha inicio])
)
```

**Why DATEADD instead of PREVIOUSMONTH?** DATEADD works with partial month selections
and doesn't require a full month in context. More robust.

#### Step 4: Replace `dif mes anterior` measure

```dax
dif mes anterior =
VAR _current = [Clientes Operativos]
VAR _previous = [Clientes Operativos mes anterior]
RETURN
    IF(
        NOT ISBLANK(_previous) && NOT ISBLANK(_current),
        _current - _previous,
        BLANK()
    )
```

#### Step 5: Create new measures

**% cambio MoM Clientes Operativos** (format as percentage):

```dax
% cambio MoM Clientes Operativos =
VAR _current = [Clientes Operativos]
VAR _previous = [Clientes Operativos mes anterior]
RETURN
    IF(
        NOT ISBLANK(_previous) && _previous <> 0,
        DIVIDE(_current - _previous, _previous),
        BLANK()
    )
```

**Clientes Nuevos mes anterior**:

```dax
Clientes Nuevos mes anterior =
CALCULATE(
    COUNT('Bind Inversiones'[Nº Bind Inv]),
    DATEADD(Calendario[Dia], -1, MONTH)
)
```

**dif Clientes Nuevos MoM**:

```dax
dif Clientes Nuevos MoM =
VAR _current = [Clientes Nuevos]
VAR _previous = [Clientes Nuevos mes anterior]
RETURN
    IF(
        NOT ISBLANK(_previous) && NOT ISBLANK(_current),
        _current - _previous,
        BLANK()
    )
```

---

## New Visual Layout

The script also modifies the report layout to replace the old page with:

| Element | Type | Description |
|---------|------|-------------|
| MesAño slicer | Dropdown | Filter by YYYY-MM without blocking previous month |
| Bancas slicer | Dropdown | Filter by Banca |
| Card: Clientes Operativos | KPI | Current month count |
| Card: dif mes anterior | KPI | Difference vs previous month |
| Card: % cambio MoM | KPI | Percentage change |
| Card: Clientes Nuevos | KPI | New clients count |
| Table | Detail | Banca breakdown with all measures |
| Bar chart | Comparison | Current vs previous month by Banca |

---

## Relationship Architecture Note

The `Calendario semanas` intermediate table remains useful for weekly aggregation tables
(`Presupuesto x sem y of Banco`, `Presupuesto x sem x producto`, `Operaciones BI`).
The new direct `Operaciones BI[Fecha] → Calendario[Dia]` relationship runs in parallel
and enables time intelligence functions. Both relationships can coexist — Power BI will
use the appropriate one based on the columns referenced in each measure.

If you encounter an ambiguous relationship warning, make the `Operaciones BI[ID Semana]
→ Calendario semanas[ID Semana]` relationship **inactive** and use `USERELATIONSHIP()`
in measures that need the weekly path.
