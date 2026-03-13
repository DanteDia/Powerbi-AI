"""
Fix "Clientes nuevos y Operativos PARA COMITE" dashboard page.

Hybrid approach:
  A) Modifies the .pbix Report/Layout JSON directly (visuals, slicers, cards)
  B) Generates DAX/relationship instructions + Tabular Editor C# script

Root cause: PREVIOUSMONTH(Calendario[Dia]) can't filter Operaciones BI because
there's NO direct relationship Operaciones BI[Fecha] -> Calendario[Dia].
The only path goes through Calendario semanas via ID Semana (weekly granularity),
which breaks time intelligence functions.

Usage:
    python scripts/fix_clientes_dashboard.py <path_to.pbix> [--output-dir output/fixes]
    python scripts/fix_clientes_dashboard.py --instructions-only [--output-dir output/fixes]
"""

import argparse
import copy
import json
import os
import shutil
import uuid
import zipfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TARGET_PAGE = "Clientes nuevos y Operativos PARA COMITE"
PAGE_WIDTH = 1280
PAGE_HEIGHT = 720

# Bancas filter: exclude null, 'Sin Banca', 'MELI'
BANCAS_FILTER = {
    "name": f"Filter{uuid.uuid4().hex[:24]}",
    "expression": {
        "Column": {
            "Expression": {"SourceRef": {"Entity": "Bancas"}},
            "Property": "Banca",
        }
    },
    "filter": {
        "Version": 2,
        "From": [{"Name": "b", "Entity": "Bancas", "Type": 0}],
        "Where": [
            {
                "Condition": {
                    "Not": {
                        "Expression": {
                            "In": {
                                "Expressions": [
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "b"}
                                            },
                                            "Property": "Banca",
                                        }
                                    }
                                ],
                                "Values": [
                                    [{"Literal": {"Value": "null"}}],
                                    [{"Literal": {"Value": "'Sin Banca'"}}],
                                    [{"Literal": {"Value": "'MELI'"}}],
                                ],
                            }
                        }
                    }
                }
            }
        ],
    },
    "type": "Categorical",
    "howCreated": 0,
    "objects": {
        "general": [
            {
                "properties": {
                    "isInvertedSelectionMode": {
                        "expr": {"Literal": {"Value": "true"}}
                    }
                }
            }
        ]
    },
    "isHiddenInViewMode": False,
}


# ---------------------------------------------------------------------------
# Visual container builders (raw Power BI Report/Layout JSON format)
# ---------------------------------------------------------------------------


def _make_visual_name():
    """Generate a unique visual container name."""
    return uuid.uuid4().hex[:20]


def _make_slicer(x, y, w, h, z, entity, prop, title=""):
    """Build a slicer visualContainer dict."""
    name = _make_visual_name()
    config = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "tabOrder": z,
                },
            }
        ],
        "singleVisual": {
            "visualType": "slicer",
            "projections": {
                "Values": [
                    {
                        "queryRef": f"{entity}.{prop}",
                        "active": True,
                    }
                ]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": entity, "Type": 0}],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "t"}},
                            "Property": prop,
                        },
                        "Name": f"{entity}.{prop}",
                    }
                ],
            },
            "objects": {
                "data": [
                    {
                        "properties": {
                            "mode": {
                                "expr": {"Literal": {"Value": "'Dropdown'"}}
                            }
                        }
                    }
                ]
            },
        },
    }
    if title:
        config["singleVisual"]["vcObjects"] = {
            "title": [
                {
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {
                            "expr": {"Literal": {"Value": f"'{title}'"}}
                        },
                    }
                }
            ]
        }
    return {
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "z": z,
        "config": json.dumps(config),
        "filters": "[]",
    }


def _make_card(x, y, w, h, z, measure_table, measure_name, title=""):
    """Build a card visualContainer dict referencing a measure."""
    name = _make_visual_name()
    query_ref = f"Sum({measure_table}.{measure_name})" if measure_table != "Medidas" else f"{measure_table}.{measure_name}"
    # For measures in a measures table, use Measure reference
    config = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "tabOrder": z,
                },
            }
        ],
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [
                    {
                        "queryRef": f"{measure_table}.{measure_name}",
                        "active": True,
                    }
                ]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "m", "Entity": measure_table, "Type": 0}],
                "Select": [
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": measure_name,
                        },
                        "Name": f"{measure_table}.{measure_name}",
                    }
                ],
            },
        },
    }
    if title:
        config["singleVisual"]["vcObjects"] = {
            "title": [
                {
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {
                            "expr": {"Literal": {"Value": f"'{title}'"}}
                        },
                    }
                }
            ]
        }
    return {
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "z": z,
        "config": json.dumps(config),
        "filters": "[]",
    }


def _make_table(x, y, w, h, z, columns, filters=None):
    """Build a tableEx visualContainer.

    columns: list of (entity, property, is_measure) tuples.
    """
    name = _make_visual_name()
    projections = {"Values": []}
    from_entities = {}
    selects = []

    for i, (entity, prop, is_measure) in enumerate(columns):
        projections["Values"].append(
            {"queryRef": f"{entity}.{prop}", "active": i == 0}
        )
        if entity not in from_entities:
            alias = f"t{len(from_entities)}"
            from_entities[entity] = alias

        alias = from_entities[entity]
        if is_measure:
            selects.append(
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": alias}},
                        "Property": prop,
                    },
                    "Name": f"{entity}.{prop}",
                }
            )
        else:
            selects.append(
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": alias}},
                        "Property": prop,
                    },
                    "Name": f"{entity}.{prop}",
                }
            )

    config = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "tabOrder": z,
                },
            }
        ],
        "singleVisual": {
            "visualType": "tableEx",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": alias, "Entity": ent, "Type": 0}
                    for ent, alias in from_entities.items()
                ],
                "Select": selects,
            },
        },
    }

    filter_json = json.dumps(filters) if filters else "[]"
    return {
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "z": z,
        "config": json.dumps(config),
        "filters": filter_json if isinstance(filter_json, str) else json.dumps(filter_json),
    }


def _make_bar_chart(x, y, w, h, z, category_entity, category_prop,
                    measures):
    """Build a clusteredBarChart visualContainer.

    measures: list of (entity, property) tuples.
    """
    name = _make_visual_name()
    from_entities = {}
    selects = []

    # Category
    if category_entity not in from_entities:
        from_entities[category_entity] = f"t{len(from_entities)}"
    cat_alias = from_entities[category_entity]
    selects.append(
        {
            "Column": {
                "Expression": {"SourceRef": {"Source": cat_alias}},
                "Property": category_prop,
            },
            "Name": f"{category_entity}.{category_prop}",
        }
    )

    # Measures
    measure_projections = []
    for ment, mprop in measures:
        if ment not in from_entities:
            from_entities[ment] = f"t{len(from_entities)}"
        m_alias = from_entities[ment]
        selects.append(
            {
                "Measure": {
                    "Expression": {"SourceRef": {"Source": m_alias}},
                    "Property": mprop,
                },
                "Name": f"{ment}.{mprop}",
            }
        )
        measure_projections.append(
            {"queryRef": f"{ment}.{mprop}", "active": False}
        )

    config = {
        "name": name,
        "layouts": [
            {
                "id": 0,
                "position": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "tabOrder": z,
                },
            }
        ],
        "singleVisual": {
            "visualType": "clusteredBarChart",
            "projections": {
                "Category": [
                    {
                        "queryRef": f"{category_entity}.{category_prop}",
                        "active": True,
                    }
                ],
                "Y": measure_projections,
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": alias, "Entity": ent, "Type": 0}
                    for ent, alias in from_entities.items()
                ],
                "Select": selects,
            },
        },
    }

    return {
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "z": z,
        "config": json.dumps(config),
        "filters": "[]",
    }


# ---------------------------------------------------------------------------
# Layout builder — construct the new page
# ---------------------------------------------------------------------------


def build_new_visuals():
    """Build the complete set of visual containers for the redesigned page."""
    visuals = []
    z = 0

    # Row 1: Slicers
    # MesAño slicer (uses new calculated column Calendario[MesAño])
    visuals.append(_make_slicer(
        x=20, y=10, w=300, h=55, z=(z := z + 1000),
        entity="Calendario", prop="MesA\u00f1o",
        title="Mes-A\u00f1o",
    ))

    # Bancas slicer
    visuals.append(_make_slicer(
        x=340, y=10, w=250, h=55, z=(z := z + 1000),
        entity="Bancas", prop="Banca",
        title="Banca",
    ))

    # Row 2: KPI Cards
    card_y = 80
    card_h = 90

    visuals.append(_make_card(
        x=20, y=card_y, w=200, h=card_h, z=(z := z + 1000),
        measure_table="Medidas", measure_name="Clientes Operativos",
        title="Clientes Operativos",
    ))

    visuals.append(_make_card(
        x=240, y=card_y, w=200, h=card_h, z=(z := z + 1000),
        measure_table="Medidas", measure_name="dif mes anterior",
        title="Dif vs Mes Anterior",
    ))

    visuals.append(_make_card(
        x=460, y=card_y, w=200, h=card_h, z=(z := z + 1000),
        measure_table="Medidas",
        measure_name="% cambio MoM Clientes Operativos",
        title="% Cambio MoM",
    ))

    visuals.append(_make_card(
        x=680, y=card_y, w=200, h=card_h, z=(z := z + 1000),
        measure_table="Medidas", measure_name="Clientes Nuevos",
        title="Clientes Nuevos",
    ))

    # Row 3: Main table
    table_columns = [
        ("Bancas", "Banca", False),
        ("Medidas", "Clientes Operativos", True),
        ("Medidas", "Clientes Nuevos", True),
        ("Medidas", "dif mes anterior", True),
        ("Medidas", "% cambio MoM Clientes Operativos", True),
        ("Medidas", "dif Clientes Nuevos MoM", True),
    ]
    visuals.append(_make_table(
        x=20, y=185, w=850, h=260, z=(z := z + 1000),
        columns=table_columns,
        filters=[BANCAS_FILTER],
    ))

    # Row 4: Bar chart — Clientes Operativos by Banca
    visuals.append(_make_bar_chart(
        x=20, y=460, w=850, h=240, z=(z := z + 1000),
        category_entity="Bancas", category_prop="Banca",
        measures=[
            ("Medidas", "Clientes Operativos"),
            ("Medidas", "Clientes Operativos mes anterior"),
        ],
    ))

    return visuals


# ---------------------------------------------------------------------------
# .pbix modifier
# ---------------------------------------------------------------------------


def modify_pbix(pbix_path, output_path=None):
    """Open a .pbix, replace the target page's visuals, save a new .pbix."""
    pbix_path = Path(pbix_path)
    if output_path is None:
        output_path = pbix_path.parent / f"{pbix_path.stem}_FIXED{pbix_path.suffix}"
    else:
        output_path = Path(output_path)

    # Copy original first
    shutil.copy2(pbix_path, output_path)

    # Read and modify Report/Layout inside the ZIP
    with zipfile.ZipFile(output_path, "r") as zin:
        namelist = zin.namelist()
        if "Report/Layout" not in namelist:
            print("ERROR: Report/Layout not found in .pbix archive")
            return None

        with zin.open("Report/Layout") as f:
            raw = f.read()

        try:
            layout_json = json.loads(raw.decode("utf-16-le").lstrip("\ufeff"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            layout_json = json.loads(raw.decode("utf-8"))

        # Read all other files
        other_files = {}
        for name in namelist:
            if name != "Report/Layout":
                with zin.open(name) as f:
                    other_files[name] = f.read()

    # Find and modify the target page
    modified = False
    for section in layout_json.get("sections", []):
        if section.get("displayName") == TARGET_PAGE:
            print(f"  Found page: '{TARGET_PAGE}'")
            print(f"  Original visuals: {len(section.get('visualContainers', []))}")

            # Replace all visual containers with our new layout
            new_visuals = build_new_visuals()
            section["visualContainers"] = new_visuals
            # Clear page-level filters (we handle filtering at visual level)
            section["filters"] = "[]"

            print(f"  New visuals: {len(new_visuals)}")
            modified = True
            break

    if not modified:
        print(f"ERROR: Page '{TARGET_PAGE}' not found in report")
        return None

    # Write modified .pbix
    new_layout_bytes = json.dumps(layout_json).encode("utf-16-le")
    # Add BOM
    new_layout_bytes = b"\xff\xfe" + new_layout_bytes

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        # Write modified layout
        zout.writestr("Report/Layout", new_layout_bytes)
        # Write all other files unchanged
        for name, data in other_files.items():
            zout.writestr(name, data)

    print(f"  Saved modified .pbix: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# DAX / Relationship instructions generator
# ---------------------------------------------------------------------------

DAX_MEASURES = {
    "Calendario[MesAño]": {
        "type": "calculated_column",
        "table": "Calendario",
        "name": "MesAño",
        "expression": 'FORMAT(Calendario[Dia], "YYYY-MM")',
        "description": "Calculated column for month-year slicer. Allows filtering by month without blocking previous month data.",
    },
    "Clientes Operativos mes anterior": {
        "type": "measure",
        "table": "Medidas",
        "name": "Clientes Operativos mes anterior",
        "expression": (
            "CALCULATE(\n"
            "    DISTINCTCOUNT('Operaciones BI'[N\u00ba Bind Inversiones]),\n"
            "    DATEADD(Calendario[Dia], -1, MONTH),\n"
            "    REMOVEFILTERS('Bind Inversiones'[fecha inicio])\n"
            ")"
        ),
        "description": "REPLACE existing. Uses DATEADD instead of PREVIOUSMONTH for robustness with partial month selections.",
    },
    "dif mes anterior": {
        "type": "measure",
        "table": "Medidas",
        "name": "dif mes anterior",
        "expression": (
            "VAR _current = [Clientes Operativos]\n"
            "VAR _previous = [Clientes Operativos mes anterior]\n"
            "RETURN\n"
            "    IF(\n"
            "        NOT ISBLANK(_previous) && NOT ISBLANK(_current),\n"
            "        _current - _previous,\n"
            "        BLANK()\n"
            "    )"
        ),
        "description": "REPLACE existing. Returns BLANK instead of 0 when data is missing.",
    },
    "% cambio MoM Clientes Operativos": {
        "type": "measure",
        "table": "Medidas",
        "name": "% cambio MoM Clientes Operativos",
        "expression": (
            "VAR _current = [Clientes Operativos]\n"
            "VAR _previous = [Clientes Operativos mes anterior]\n"
            "RETURN\n"
            "    IF(\n"
            "        NOT ISBLANK(_previous) && _previous <> 0,\n"
            "        DIVIDE(_current - _previous, _previous),\n"
            "        BLANK()\n"
            "    )"
        ),
        "description": "NEW. Percentage change month-over-month for Clientes Operativos.",
    },
    "Clientes Nuevos mes anterior": {
        "type": "measure",
        "table": "Medidas",
        "name": "Clientes Nuevos mes anterior",
        "expression": (
            "CALCULATE(\n"
            "    COUNT('Bind Inversiones'[N\u00ba Bind Inv]),\n"
            "    DATEADD(Calendario[Dia], -1, MONTH)\n"
            ")"
        ),
        "description": "NEW. Count of new clients from previous month.",
    },
    "dif Clientes Nuevos MoM": {
        "type": "measure",
        "table": "Medidas",
        "name": "dif Clientes Nuevos MoM",
        "expression": (
            "VAR _current = [Clientes Nuevos]\n"
            "VAR _previous = [Clientes Nuevos mes anterior]\n"
            "RETURN\n"
            "    IF(\n"
            "        NOT ISBLANK(_previous) && NOT ISBLANK(_current),\n"
            "        _current - _previous,\n"
            "        BLANK()\n"
            "    )"
        ),
        "description": "NEW. Month-over-month difference for Clientes Nuevos.",
    },
}

RELATIONSHIP_FIX = {
    "from_table": "Operaciones BI",
    "from_column": "Fecha",
    "to_table": "Calendario",
    "to_column": "Dia",
    "cardinality": "Many-to-One",
    "cross_filter": "Single",
    "description": (
        "This is the CRITICAL fix. Without this relationship, "
        "PREVIOUSMONTH/DATEADD on Calendario[Dia] cannot filter "
        "Operaciones BI, causing all MoM measures to return BLANK/zero."
    ),
}


def generate_tabular_editor_script():
    """Generate a C# script for Tabular Editor to apply all DAX/relationship fixes."""
    script = '''// =============================================================================
// Tabular Editor C# Script — Fix "Clientes nuevos y Operativos PARA COMITE"
// =============================================================================
// HOW TO USE:
// 1. Open the .pbix in Power BI Desktop
// 2. Open Tabular Editor and connect to the running PBI Desktop instance
//    (File > Open > From DB... > localhost:<port>)
// 3. Go to Advanced Scripting tab (C# Script)
// 4. Paste this entire script and click Run (F5)
// 5. Save changes back to PBI Desktop (Ctrl+S in Tabular Editor)
// =============================================================================

// --- Step 1: Create the relationship Operaciones BI[Fecha] -> Calendario[Dia] ---
// Check if relationship already exists
var fromTable = Model.Tables["Operaciones BI"];
var toTable = Model.Tables["Calendario"];
var fromCol = fromTable.Columns["Fecha"];
var toCol = toTable.Columns["Dia"];

bool relExists = false;
foreach (var rel in Model.Relationships)
{
    if (rel.FromColumn == fromCol && rel.ToColumn == toCol)
    {
        relExists = true;
        break;
    }
}

if (!relExists)
{
    var newRel = Model.AddRelationship();
    newRel.FromColumn = fromCol;
    newRel.ToColumn = toCol;
    // Cardinality and CrossFilteringBehavior are set automatically
    Info("Created relationship: Operaciones BI[Fecha] -> Calendario[Dia]");
}
else
{
    Info("Relationship Operaciones BI[Fecha] -> Calendario[Dia] already exists");
}

// --- Step 2: Add calculated column Calendario[MesAño] ---
var calTable = Model.Tables["Calendario"];
if (!calTable.Columns.Contains("MesAño"))
{
    var mesAnoCol = calTable.AddCalculatedColumn("MesAño");
    mesAnoCol.Expression = "FORMAT(Calendario[Dia], \\"YYYY-MM\\")";
    mesAnoCol.DataType = DataType.String;
    Info("Created calculated column: Calendario[MesAño]");
}
else
{
    Info("Calendario[MesAño] already exists");
}

// --- Step 3: Fix/Create measures in Medidas table ---
var medidas = Model.Tables["Medidas"];

// 3a. Replace "Clientes Operativos mes anterior"
if (medidas.Measures.Contains("Clientes Operativos mes anterior"))
{
    medidas.Measures["Clientes Operativos mes anterior"].Expression =
        "CALCULATE(\\n" +
        "    DISTINCTCOUNT(\'Operaciones BI\'[Nº Bind Inversiones]),\\n" +
        "    DATEADD(Calendario[Dia], -1, MONTH),\\n" +
        "    REMOVEFILTERS(\'Bind Inversiones\'[fecha inicio])\\n" +
        ")";
    Info("Updated measure: Clientes Operativos mes anterior");
}
else
{
    var m = medidas.AddMeasure("Clientes Operativos mes anterior",
        "CALCULATE(\\n" +
        "    DISTINCTCOUNT(\'Operaciones BI\'[Nº Bind Inversiones]),\\n" +
        "    DATEADD(Calendario[Dia], -1, MONTH),\\n" +
        "    REMOVEFILTERS(\'Bind Inversiones\'[fecha inicio])\\n" +
        ")");
    Info("Created measure: Clientes Operativos mes anterior");
}

// 3b. Replace "dif mes anterior"
if (medidas.Measures.Contains("dif mes anterior"))
{
    medidas.Measures["dif mes anterior"].Expression =
        "VAR _current = [Clientes Operativos]\\n" +
        "VAR _previous = [Clientes Operativos mes anterior]\\n" +
        "RETURN\\n" +
        "    IF(\\n" +
        "        NOT ISBLANK(_previous) && NOT ISBLANK(_current),\\n" +
        "        _current - _previous,\\n" +
        "        BLANK()\\n" +
        "    )";
    Info("Updated measure: dif mes anterior");
}

// 3c. Create "% cambio MoM Clientes Operativos"
if (!medidas.Measures.Contains("% cambio MoM Clientes Operativos"))
{
    var m = medidas.AddMeasure("% cambio MoM Clientes Operativos",
        "VAR _current = [Clientes Operativos]\\n" +
        "VAR _previous = [Clientes Operativos mes anterior]\\n" +
        "RETURN\\n" +
        "    IF(\\n" +
        "        NOT ISBLANK(_previous) && _previous <> 0,\\n" +
        "        DIVIDE(_current - _previous, _previous),\\n" +
        "        BLANK()\\n" +
        "    )");
    m.FormatString = "0.0%;-0.0%;0.0%";
    Info("Created measure: % cambio MoM Clientes Operativos");
}

// 3d. Create "Clientes Nuevos mes anterior"
if (!medidas.Measures.Contains("Clientes Nuevos mes anterior"))
{
    var m = medidas.AddMeasure("Clientes Nuevos mes anterior",
        "CALCULATE(\\n" +
        "    COUNT(\'Bind Inversiones\'[Nº Bind Inv]),\\n" +
        "    DATEADD(Calendario[Dia], -1, MONTH)\\n" +
        ")");
    Info("Created measure: Clientes Nuevos mes anterior");
}

// 3e. Create "dif Clientes Nuevos MoM"
if (!medidas.Measures.Contains("dif Clientes Nuevos MoM"))
{
    var m = medidas.AddMeasure("dif Clientes Nuevos MoM",
        "VAR _current = [Clientes Nuevos]\\n" +
        "VAR _previous = [Clientes Nuevos mes anterior]\\n" +
        "RETURN\\n" +
        "    IF(\\n" +
        "        NOT ISBLANK(_previous) && NOT ISBLANK(_current),\\n" +
        "        _current - _previous,\\n" +
        "        BLANK()\\n" +
        "    )");
    Info("Created measure: dif Clientes Nuevos MoM");
}

Info("\\n=== ALL CHANGES APPLIED ===\\nSave to PBI Desktop with Ctrl+S");
'''
    return script


def generate_instructions(output_dir):
    """Generate markdown instructions file."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    instructions = f"""# Fix: "Clientes nuevos y Operativos PARA COMITE" Dashboard

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
    DISTINCTCOUNT('Operaciones BI'[N\u00ba Bind Inversiones]),
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
    COUNT('Bind Inversiones'[N\u00ba Bind Inv]),
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
"""

    # Write instructions
    instructions_path = output_dir / "clientes_dashboard_instructions.md"
    with open(instructions_path, "w", encoding="utf-8") as f:
        f.write(instructions)
    print(f"  Instructions: {instructions_path}")

    # Write Tabular Editor C# script
    script_path = output_dir / "tabular_editor_script.cs"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(generate_tabular_editor_script())
    print(f"  Tabular Editor script: {script_path}")

    # Write machine-readable fix spec
    fix_spec = {
        "target_page": TARGET_PAGE,
        "root_cause": {
            "broken_relationship": "Operaciones BI[Fecha] -> nan[nan]",
            "missing_relationship": RELATIONSHIP_FIX,
            "filter_conflict": "Año/Mes slicers block PREVIOUSMONTH from accessing previous year data",
        },
        "relationship_fix": RELATIONSHIP_FIX,
        "dax_changes": DAX_MEASURES,
        "visual_layout": {
            "page_size": {"width": PAGE_WIDTH, "height": PAGE_HEIGHT},
            "visuals": [
                {"type": "slicer", "field": "Calendario.MesAño", "position": "top-left"},
                {"type": "slicer", "field": "Bancas.Banca", "position": "top-center"},
                {"type": "card", "measure": "Clientes Operativos"},
                {"type": "card", "measure": "dif mes anterior"},
                {"type": "card", "measure": "% cambio MoM Clientes Operativos"},
                {"type": "card", "measure": "Clientes Nuevos"},
                {"type": "tableEx", "columns": ["Banca", "Clientes Operativos", "Clientes Nuevos", "dif mes anterior", "% cambio MoM", "dif Clientes Nuevos MoM"]},
                {"type": "clusteredBarChart", "category": "Banca", "measures": ["Clientes Operativos", "Clientes Operativos mes anterior"]},
            ],
        },
    }
    fix_path = output_dir / "clientes_dashboard_fix.json"
    with open(fix_path, "w", encoding="utf-8") as f:
        json.dump(fix_spec, f, indent=2, ensure_ascii=False)
    print(f"  Fix spec: {fix_path}")

    return instructions_path, script_path, fix_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description='Fix "Clientes nuevos y Operativos PARA COMITE" dashboard'
    )
    parser.add_argument(
        "pbix_path",
        nargs="?",
        help="Path to the .pbix file to modify (optional if --instructions-only)",
    )
    parser.add_argument(
        "--output-dir",
        default="output/fixes",
        help="Output directory for instructions and fix spec (default: output/fixes)",
    )
    parser.add_argument(
        "--instructions-only",
        action="store_true",
        help="Only generate instructions, don't modify .pbix",
    )
    parser.add_argument(
        "--output-pbix",
        help="Output path for modified .pbix (default: <original>_FIXED.pbix)",
    )

    args = parser.parse_args()

    print("=" * 70)
    print('FIX: "Clientes nuevos y Operativos PARA COMITE"')
    print("=" * 70)

    # Always generate instructions
    print("\n[1/2] Generating DAX & relationship instructions...")
    generate_instructions(args.output_dir)

    # Modify .pbix if path provided and not instructions-only
    if args.pbix_path and not args.instructions_only:
        print(f"\n[2/2] Modifying .pbix layout...")
        result = modify_pbix(args.pbix_path, args.output_pbix)
        if result:
            print(f"\nDone! Modified .pbix saved to: {result}")
            print(f"Apply DAX changes using: {args.output_dir}/tabular_editor_script.cs")
        else:
            print("\nFailed to modify .pbix. Use instructions for manual fix.")
    elif args.instructions_only or not args.pbix_path:
        print("\n[2/2] Skipping .pbix modification (no file provided or --instructions-only)")
        print(f"\nDone! Apply changes using files in: {args.output_dir}/")
    else:
        print("\nProvide a .pbix path to also modify the report layout.")

    print("\nNext steps:")
    print("  1. Open the .pbix in Power BI Desktop")
    print("  2. Open Tabular Editor → connect to PBI Desktop")
    print(f"  3. Run the script: {args.output_dir}/tabular_editor_script.cs")
    print("  4. Save and verify 'dif mes anterior' shows non-zero values")


if __name__ == "__main__":
    main()
