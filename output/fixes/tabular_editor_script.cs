// =============================================================================
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
    mesAnoCol.Expression = "FORMAT(Calendario[Dia], \"YYYY-MM\")";
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
        "CALCULATE(\n" +
        "    DISTINCTCOUNT('Operaciones BI'[Nº Bind Inversiones]),\n" +
        "    DATEADD(Calendario[Dia], -1, MONTH),\n" +
        "    REMOVEFILTERS('Bind Inversiones'[fecha inicio])\n" +
        ")";
    Info("Updated measure: Clientes Operativos mes anterior");
}
else
{
    var m = medidas.AddMeasure("Clientes Operativos mes anterior",
        "CALCULATE(\n" +
        "    DISTINCTCOUNT('Operaciones BI'[Nº Bind Inversiones]),\n" +
        "    DATEADD(Calendario[Dia], -1, MONTH),\n" +
        "    REMOVEFILTERS('Bind Inversiones'[fecha inicio])\n" +
        ")");
    Info("Created measure: Clientes Operativos mes anterior");
}

// 3b. Replace "dif mes anterior"
if (medidas.Measures.Contains("dif mes anterior"))
{
    medidas.Measures["dif mes anterior"].Expression =
        "VAR _current = [Clientes Operativos]\n" +
        "VAR _previous = [Clientes Operativos mes anterior]\n" +
        "RETURN\n" +
        "    IF(\n" +
        "        NOT ISBLANK(_previous) && NOT ISBLANK(_current),\n" +
        "        _current - _previous,\n" +
        "        BLANK()\n" +
        "    )";
    Info("Updated measure: dif mes anterior");
}

// 3c. Create "% cambio MoM Clientes Operativos"
if (!medidas.Measures.Contains("% cambio MoM Clientes Operativos"))
{
    var m = medidas.AddMeasure("% cambio MoM Clientes Operativos",
        "VAR _current = [Clientes Operativos]\n" +
        "VAR _previous = [Clientes Operativos mes anterior]\n" +
        "RETURN\n" +
        "    IF(\n" +
        "        NOT ISBLANK(_previous) && _previous <> 0,\n" +
        "        DIVIDE(_current - _previous, _previous),\n" +
        "        BLANK()\n" +
        "    )");
    m.FormatString = "0.0%;-0.0%;0.0%";
    Info("Created measure: % cambio MoM Clientes Operativos");
}

// 3d. Create "Clientes Nuevos mes anterior"
if (!medidas.Measures.Contains("Clientes Nuevos mes anterior"))
{
    var m = medidas.AddMeasure("Clientes Nuevos mes anterior",
        "CALCULATE(\n" +
        "    COUNT('Bind Inversiones'[Nº Bind Inv]),\n" +
        "    DATEADD(Calendario[Dia], -1, MONTH)\n" +
        ")");
    Info("Created measure: Clientes Nuevos mes anterior");
}

// 3e. Create "dif Clientes Nuevos MoM"
if (!medidas.Measures.Contains("dif Clientes Nuevos MoM"))
{
    var m = medidas.AddMeasure("dif Clientes Nuevos MoM",
        "VAR _current = [Clientes Nuevos]\n" +
        "VAR _previous = [Clientes Nuevos mes anterior]\n" +
        "RETURN\n" +
        "    IF(\n" +
        "        NOT ISBLANK(_previous) && NOT ISBLANK(_current),\n" +
        "        _current - _previous,\n" +
        "        BLANK()\n" +
        "    )");
    Info("Created measure: dif Clientes Nuevos MoM");
}

Info("\n=== ALL CHANGES APPLIED ===\nSave to PBI Desktop with Ctrl+S");
