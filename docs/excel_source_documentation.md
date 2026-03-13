# Excel Source Documentation

Generated: 2026-03-13T01:27:47

## Summary

- Workbooks analyzed: 22
- Accessible workbooks: 22
- Sheets profiled: 83
- PBIX tables mapped to Excel: 38
- Workbooks with data quality flags: 20

## Workbook Inventory

| Workbook | Size MB | Sheets | PBIX Tables | |
|---|---:|---:|---:|---|
| Boletos Bind Inversiones.xlsx | 89.68 | 4 | 1 | \\CPDWFSGRPBIND\iam$\Comercial\Seguimiento comercial 2022\Boletos Bind Inversiones.xlsx |
| Boletos IAM.xlsm | 86.14 | 4 | 2 | \\CPDWFSGRPBIND\iam$\Comercial\Seguimiento comercial 2022\Boletos IAM.xlsm |
| Ajustes RV.xlsx | 0.01 | 1 | 1 | G:\Comercial\Seguimiento comercial 2022\Ajustes RV.xlsx |
| Boletos IVSA.xlsx | 12.56 | 4 | 1 | G:\Comercial\Seguimiento comercial 2022\Boletos IVSA.xlsx |
| inflacion.xlsx | 0.01 | 2 | 1 | G:\Comercial\Seguimiento comercial 2022\Seguimiento Comercial Zafiro\inflacion.xlsx |
| Boletos Bind Inversiones 2.xlsx | 84.78 | 3 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 2.xlsx |
| Boletos Bind Inversiones 3.xlsx | 84.66 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 3.xlsx |
| Boletos Bind Inversiones 4.xlsx | 81.35 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 4.xlsx |
| Boletos Bind Inversiones 5.xlsx | 82.52 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 5.xlsx |
| Boletos Bind Inversiones 6.xlsx | 65.07 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 6.xlsx |
| Boletos Bind UY.xlsx | 0.83 | 9 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos Bind UY.xlsx |
| Boletos IAM 4.xlsx | 86.76 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos IAM 4.xlsx |
| Boletos IAM 5.xlsx | 70.28 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos IAM 5.xlsx |
| Boletos IAM 6.xlsx | 40.29 | 2 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos IAM 6.xlsx |
| Boletos IAM3.xlsx | 85.16 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos IAM3.xlsx |
| Boletos IVSA.xlsx | 52.92 | 4 | 1 | G:\Comercial\Seguimiento comercial 2023\Boletos IVSA.xlsx |
| Canales de operacion.xlsx | 42.14 | 5 | 2 | G:\Comercial\Seguimiento comercial 2023\Canales de operacion.xlsx |
| cheques operados.xlsx | 3.28 | 4 | 1 | G:\Comercial\Seguimiento comercial 2023\cheques operados.xlsx |
| clientes Bind Inversiones.xlsx | 8.18 | 7 | 3 | G:\Comercial\Seguimiento comercial 2023\clientes Bind Inversiones.xlsx |
| Estructura Comercial.xlsx | 0.03 | 11 | 10 | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| PEA 2023.xlsx | 2.36 | 15 | 4 | G:\Comercial\Seguimiento comercial 2023\PEA 2023.xlsx |
| Saldos IVSA.xlsx | 30.77 | 1 | 1 | G:\Comercial\Seguimiento comercial 2023\Saldos IVSA.xlsx |

## Boletos Bind Inversiones.xlsx

- Path: \\CPDWFSGRPBIND\iam$\Comercial\Seguimiento comercial 2022\Boletos Bind Inversiones.xlsx
- Size: 89.68 MB
- Modified: 2023-04-12T13:04:30
- Sheets: 4
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Operaciones BI` ← Operaciones BI [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Operaciones BI | yes | 1048575 | 12 | 725 | - | duplicate_rows |
| Hoja1 | no | 6478 | 4 | 0 | - | - |
| Semanas | no | 363 | 11 | 0 | Dia | high_missingness |
| Calendario semanas | no | 52 | 4 | 0 | ID Semana | - |

### Referenced sheet column details

#### Operaciones BI

PBIX tables: Operaciones BI

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 2 |  |
| Cod Region | numeric | 0.0 | 1 |  |
| Nº Bind Inversiones | numeric | 0.0 | 4493 |  |
| Nº Cliente | numeric | 0.0 | 6177 |  |
| Fecha | datetime | 0.0 | 605 |  |
| Producto | numeric | 0.0 | 20 |  |
| Semana | numeric | 0.0 | 38 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 2 |  |
| PN | numeric | 0.0 | 669588 |  |
| Volumen | numeric | 0.01 | 81965 |  |
| Facturacion | numeric | 0.0 | 712689 |  |


## Boletos IAM.xlsm

- Path: \\CPDWFSGRPBIND\iam$\Comercial\Seguimiento comercial 2022\Boletos IAM.xlsm
- Size: 86.14 MB
- Modified: 2026-02-03T04:11:11
- Sheets: 4
- Referenced sheets: 2

### PBIX tables fed by this workbook

- `Calendario semanas` ← Calendario semanas [Sheet]
- `Operaciones IAM` ← Operaciones IAM [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Operaciones IAM | yes | 1048575 | 10 | 0 | - | - |
| Operaciones de la semana | no | 43844 | 6 | 0 | - | - |
| Semanas | no | 363 | 14 | 0 | Dia | high_missingness |
| Calendario semanas | yes | 347 | 5 | 0 | ID Semana | - |

### Referenced sheet column details

#### Operaciones IAM

PBIX tables: Operaciones IAM

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Nº Bind Inversiones | numeric | 0.0 | 3055 |  |
| NumCuotapartista | numeric | 0.0 | 3056 |  |
| Fecha | datetime | 0.0 | 653 |  |
| NomCuotapartista | text | 0.0 | 3119 |  |
| NombreFondoAbreviado | numeric | 0.0 | 12 |  |
| $ PN Cuotap. (23/01/22) | numeric | 0.0 | 741602 |  |
| $ Facturación CP | numeric | 0.0 | 736284 |  |
| Semana | numeric | 0.0 | 45 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 2 |  |

#### Calendario semanas

PBIX tables: Calendario semanas

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| ID Semana | text | 0.0 | 347 | candidate key |
| n° semana | numeric | 0.0 | 50 |  |
| Año | numeric | 0.0 | 7 |  |
| Mes | numeric | 0.0 | 12 |  |
| Semana | numeric | 0.0 | 5 |  |


## Ajustes RV.xlsx

- Path: G:\Comercial\Seguimiento comercial 2022\Ajustes RV.xlsx
- Size: 0.01 MB
- Modified: 2022-04-08T17:17:43
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Medidas` ← Ajustes RV [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Ajustes RV | yes | 4 | 4 | 0 | Ajuste $ | - |

### Referenced sheet column details

#### Ajustes RV

PBIX tables: Medidas

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Fecha | datetime | 0.0 | 3 |  |
| Oficial Bind Inversiones | numeric | 0.0 | 2 |  |
| Ajuste $ | numeric | 0.0 | 4 | candidate key |
| Observación | text | 0.0 | 2 |  |


## Boletos IVSA.xlsx

- Path: G:\Comercial\Seguimiento comercial 2022\Boletos IVSA.xlsx
- Size: 12.56 MB
- Modified: 2026-02-02T13:35:10
- Sheets: 4
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Calendario` ← Calendario [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Boletos IVSA | no | 1048314 | 19 | 924452 | - | duplicate_rows, high_missingness |
| Hoja1 | no | 17013 | 14 | 0 | Boleto | - |
| Semanas | no | 363 | 11 | 0 | Dia | high_missingness |
| Calendario | yes | 2189 | 6 | 0 | Dia | - |

### Referenced sheet column details

#### Calendario

PBIX tables: Calendario

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Dia | datetime | 0.0 | 2189 | candidate key |
| Año | numeric | 0.0 | 6 |  |
| Mes | numeric | 0.0 | 12 |  |
| Semana | numeric | 0.0 | 51 |  |
| ID Semana | text | 0.0 | 248 |  |
| Habil | numeric | 0.0 | 2 |  |


## inflacion.xlsx

- Path: G:\Comercial\Seguimiento comercial 2022\Seguimiento Comercial Zafiro\inflacion.xlsx
- Size: 0.01 MB
- Modified: 2024-02-19T16:01:25
- Sheets: 2
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `inflación` ← inflación [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| inflación | yes | 85 | 2 | 0 | indice_tiempo, ipc_nivel_general_nacional | - |
| dolar 3500 | no | 37 | 2 | 0 | Fecha, TC 3500 | - |

### Referenced sheet column details

#### inflación

PBIX tables: inflación

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| indice_tiempo | datetime | 0.0 | 85 | candidate key |
| ipc_nivel_general_nacional | numeric | 0.0 | 85 | candidate key |


## Boletos Bind Inversiones 2.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 2.xlsx
- Size: 84.78 MB
- Modified: 2023-12-28T12:59:49
- Sheets: 3
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Operaciones BI (2)` ← Operaciones BI [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Operaciones BI | yes | 1025823 | 12 | 3098 | - | duplicate_rows, high_missingness |
| Semanas | no | 363 | 11 | 0 | Dia | high_missingness |
| Calendario semanas | no | 52 | 4 | 0 | ID Semana | - |

### Referenced sheet column details

#### Operaciones BI

PBIX tables: Operaciones BI (2)

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 2 |  |
| Cod Region | numeric | 0.0 | 2 |  |
| Nº Bind Inversiones | numeric | 0.0 | 5048 |  |
| Nº Cliente | numeric | 0.0 | 5623 |  |
| Fecha | datetime | 0.0 | 330 |  |
| Producto | numeric | 0.0 | 20 |  |
| Semana | numeric | 72.06 | 15 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 2 |  |
| PN | numeric | 0.0 | 673464 |  |
| Volumen | numeric | 0.0 | 57018 |  |
| Facturacion | numeric | 0.0 | 699677 |  |


## Boletos Bind Inversiones 3.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 3.xlsx
- Size: 84.66 MB
- Modified: 2024-08-15T11:50:04
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Operaciones BI 3` ← Hoja1 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Hoja1 | yes | 1017227 | 13 | 4252 | - | duplicate_rows, high_missingness |

### Referenced sheet column details

#### Hoja1

PBIX tables: Operaciones BI 3

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 2 |  |
| Cod Region | numeric | 0.0 | 3 |  |
| Nº Bind Inversiones | numeric | 0.0 | 4952 |  |
| Nº Cliente | numeric | 0.0 | 5582 |  |
| Fecha | datetime | 0.0 | 279 |  |
| Producto | numeric | 0.0 | 21 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 9 |  |
| Año | numeric | 0.0 | 2 |  |
| PN | numeric | 0.0 | 633981 |  |
| Volumen | numeric | 0.0 | 55834 |  |
| Facturacion | numeric | 0.0 | 664281 |  |
| Unnamed: 12 | text | 89.42 | 3357 |  |


## Boletos Bind Inversiones 4.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 4.xlsx
- Size: 81.35 MB
- Modified: 2025-05-08T12:44:49
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Operaciones BI 4` ← Operaciones BI 4 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Operaciones BI 4 | yes | 1001186 | 19 | 813 | - | duplicate_rows, high_missingness |

### Referenced sheet column details

#### Operaciones BI 4

PBIX tables: Operaciones BI 4

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 3 |  |
| Cod Region | numeric | 0.0 | 3 |  |
| Nº Bind Inversiones | numeric | 0.0 | 5044 |  |
| Nº Cliente | numeric | 0.0 | 5611 |  |
| Fecha | datetime | 0.0 | 356 |  |
| Producto | numeric | 0.0 | 26 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 3 |  |
| PN | numeric | 0.01 | 623482 |  |
| Volumen | numeric | 0.0 | 61882 |  |
| Facturacion | numeric | 0.0 | 658127 |  |
| Unnamed: 12 | numeric | 99.1 | 17 |  |
| Unnamed: 13 | text | 100.0 | 1 | candidate key |
| Unnamed: 14 | numeric | 100.0 | 2 |  |
| Unnamed: 15 | numeric | 100.0 | 1 | candidate key |
| Unnamed: 16 | empty | 100.0 | 0 |  |
| Unnamed: 17 | empty | 100.0 | 0 |  |
| Unnamed: 18 | numeric | 100.0 | 1 | candidate key |


## Boletos Bind Inversiones 5.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 5.xlsx
- Size: 82.52 MB
- Modified: 2025-09-04T16:01:53
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Operaciones BI 5` ← Operaciones BI 5 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Operaciones BI 5 | yes | 1023266 | 13 | 725 | - | duplicate_rows, high_missingness |

### Referenced sheet column details

#### Operaciones BI 5

PBIX tables: Operaciones BI 5

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 3 |  |
| Cod Region | numeric | 0.0 | 3 |  |
| Nº Bind Inversiones | numeric | 0.0 | 4966 |  |
| Nº Cliente | numeric | 0.0 | 7636 |  |
| Fecha | datetime | 0.0 | 380 |  |
| Producto | numeric | 0.0 | 33 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 2 |  |
| PN | numeric | 0.23 | 642704 |  |
| Volumen | numeric | 0.01 | 63484 |  |
| Facturacion | numeric | 0.0 | 675010 |  |
| Unnamed: 12 | text | 100.0 | 2 | candidate key |


## Boletos Bind Inversiones 6.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 6.xlsx
- Size: 65.07 MB
- Modified: 2026-03-12T14:44:36
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Operaciones BI 6` ← Operaciones BI 6 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Operaciones BI 6 | yes | 796926 | 12 | 1801 | - | duplicate_rows, high_missingness |

### Referenced sheet column details

#### Operaciones BI 6

PBIX tables: Operaciones BI 6

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 3 |  |
| Cod Region | numeric | 0.0 | 2 |  |
| Nº Bind Inversiones | numeric | 0.0 | 5664 |  |
| Nº Cliente | numeric | 0.0 | 6164 |  |
| Fecha | datetime | 0.0 | 259 |  |
| Producto | numeric | 0.0 | 31 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 8 |  |
| Año | numeric | 0.0 | 2 |  |
| PN | numeric | 0.04 | 540310 |  |
| Volumen | numeric | 0.01 | 81274 |  |
| Facturacion | numeric | 0.0 | 587158 |  |


## Boletos Bind UY.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos Bind UY.xlsx
- Size: 0.83 MB
- Modified: 2026-02-05T15:11:52
- Sheets: 9
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Referidos` ← Referidos [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Datos para Boletos BI | no | 2079 | 26 | 34 | - | duplicate_rows, high_missingness |
| Listado de ISIN | no | 790 | 3 | 2 | - | duplicate_rows, high_missingness |
| Rebates & Management Fees | no | 168 | 32 | 0 | - | high_missingness |
| Safra | no | 10 | 6 | 0 | Unnamed: 2, Unnamed: 3, Unnamed: 4 | high_missingness |
| Parametros | no | 24 | 2 | 0 | N° Producto, Producto | - |
| Referidos | yes | 7 | 12 | 0 | Facturación CCL, Facturación $ | - |
| CUITS IVSA | no | 10172 | 3 | 0 | Nro. BINV | - |
| TdC | no | 1 | 37 | 0 | Unnamed: 0, 2023-01-01 00:00:00, 2023-02-01 00:00:00 | - |
| Hoja1 | no | 0 | 0 | 0 | - | empty_sheet |

### Referenced sheet column details

#### Referidos

PBIX tables: Referidos

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 1 |  |
| Región | numeric | 0.0 | 1 |  |
| nº Bind Inversiones | numeric | 0.0 | 3 |  |
| Comitente | numeric | 0.0 | 3 |  |
| Fecha | datetime | 0.0 | 4 |  |
| ISIN | text | 0.0 | 3 |  |
| Descripcion | text | 0.0 | 3 |  |
| Producto | numeric | 0.0 | 3 |  |
| Volumen | numeric | 0.0 | 6 |  |
| Facturación CCL | numeric | 0.0 | 7 | candidate key |
| Tipo de cambio | numeric | 0.0 | 1 |  |
| Facturación $ | numeric | 0.0 | 7 | candidate key |


## Boletos IAM 4.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos IAM 4.xlsx
- Size: 86.76 MB
- Modified: 2025-05-08T12:16:28
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `boletos IAM 4` ← boletos IAM 4 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| boletos IAM 4 | yes | 1046537 | 10 | 0 | - | high_missingness |

### Referenced sheet column details

#### boletos IAM 4

PBIX tables: boletos IAM 4

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| NumCuotapartista | numeric | 0.0 | 4015 |  |
| NumCuotapartista.1 | numeric | 0.0 | 4018 |  |
| Fecha | datetime | 0.0 | 247 |  |
| NomCuotapartista | text | 0.0 | 4010 |  |
| NombreFondoAbreviado | numeric | 0.0 | 17 |  |
| $ PN Cuotap. (23/01/22) | numeric | 0.0 | 722802 |  |
| $ Facturación CP | numeric | 0.0 | 718146 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 9 |  |
| Año | numeric | 0.0 | 2 |  |


## Boletos IAM 5.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos IAM 5.xlsx
- Size: 70.28 MB
- Modified: 2025-11-03T12:37:01
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `boletos IAM 5` ← boletos IAM 5 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| boletos IAM 5 | yes | 836963 | 12 | 0 | - | high_missingness |

### Referenced sheet column details

#### boletos IAM 5

PBIX tables: boletos IAM 5

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| NumCuotapartista | numeric | 0.0 | 3903 |  |
| NumCuotapartista.1 | numeric | 0.0 | 3901 |  |
| Fecha | datetime | 0.0 | 196 |  |
| NomCuotapartista | text | 0.0 | 3921 |  |
| NombreFondoAbreviado | numeric | 0.0 | 17 |  |
| $ PN Cuotap. (23/01/22) | numeric | 0.0 | 583632 |  |
| $ Facturación CP | numeric | 0.0 | 579204 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 7 |  |
| Año | numeric | 0.0 | 1 |  |
| Unnamed: 10 | empty | 100.0 | 0 |  |
| Unnamed: 11 | numeric | 100.0 | 1 | candidate key |


## Boletos IAM 6.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos IAM 6.xlsx
- Size: 40.29 MB
- Modified: 2026-03-10T12:35:57
- Sheets: 2
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `boletos IAM 6` ← Boletos IAM 6 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Boletos IAM 6 | yes | 421041 | 11 | 0 | - | high_missingness |
| Hoja1 | no | 17 | 3 | 0 | Unnamed: 1, Unnamed: 2 | high_missingness |

### Referenced sheet column details

#### Boletos IAM 6

PBIX tables: boletos IAM 6

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| NumCuotapartista | numeric | 0.0 | 4721 |  |
| NumCuotapartista.1 | numeric | 0.0 | 4725 |  |
| Fecha | datetime | 0.0 | 100 |  |
| NomCuotapartista | text | 0.0 | 4673 |  |
| NombreFondoAbreviado | numeric | 0.0 | 17 |  |
| $ PN Cuotap. (23/01/22) | numeric | 0.0 | 333374 |  |
| $ Facturación CP | numeric | 0.0 | 333491 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 5 |  |
| Año | numeric | 0.0 | 2 |  |
| Unnamed: 10 | empty | 100.0 | 0 |  |


## Boletos IAM3.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos IAM3.xlsx
- Size: 85.16 MB
- Modified: 2024-08-14T12:25:58
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `boletos IAM 3` ← boletos IAM 3 [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| boletos IAM 3 | yes | 1017059 | 10 | 0 | - | high_missingness |

### Referenced sheet column details

#### boletos IAM 3

PBIX tables: boletos IAM 3

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| N° Bind Inversiones | numeric | 0.0 | 3929 |  |
| NumCuotapartista | numeric | 0.0 | 3929 |  |
| Fecha | datetime | 0.0 | 270 |  |
| NomCuotapartista | text | 0.0 | 3937 |  |
| NombreFondoAbreviado | numeric | 0.0 | 14 |  |
| $ PN Cuotap. (23/01/22) | numeric | 0.0 | 668163 |  |
| $ Facturación CP | numeric | 0.0 | 663102 |  |
| Semana | empty | 100.0 | 0 |  |
| Mes | numeric | 0.0 | 9 |  |
| Año | numeric | 0.0 | 2 |  |


## Boletos IVSA.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Boletos IVSA.xlsx
- Size: 52.92 MB
- Modified: 2026-03-10T13:47:07
- Sheets: 4
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Boletos IVSA` ← Boletos IVSA [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Boletos IVSA | yes | 516361 | 17 | 1335 | - | duplicate_rows, high_missingness |
| Hoja1 | no | 472233 | 14 | 455218 | - | duplicate_rows, high_missingness |
| Semanas | no | 363 | 11 | 0 | Dia | high_missingness |
| Calendario | no | 1093 | 5 | 0 | Dia | - |

### Referenced sheet column details

#### Boletos IVSA

PBIX tables: Boletos IVSA

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| N° Bind Inversiones | numeric | 0.0 | 4248 |  |
| Boleto | numeric | 1.14 | 168313 |  |
| COMITENTE | numeric | 0.0 | 4224 |  |
| ESPECIE | text | 11.85 | 11659 |  |
| Asset Class | numeric | 0.0 | 15 |  |
| Fecha Operación | datetime | 0.0 | 1261 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 6 |  |
| Semana | numeric | 87.53 | 49 |  |
| OPERACION | text | 0.0 | 130 |  |
| Volumen | numeric | 0.0 | 378825 |  |
| Fee | numeric | 0.0 | 210289 |  |
| TC | text | 27.4 | 882 |  |
| Canal | text | 8.11 | 5 |  |
| Unnamed: 14 | numeric | 82.96 | 185 |  |
| Unnamed: 15 | text | 100.0 | 10 | candidate key |
| Unnamed: 16 | numeric | 100.0 | 10 | candidate key |


## Canales de operacion.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Canales de operacion.xlsx
- Size: 42.14 MB
- Modified: 2026-01-20T17:50:08
- Sheets: 5
- Referenced sheets: 2

### PBIX tables fed by this workbook

- `Operaciones por canal IAM` ← Operaciones IAM [Sheet]
- `Resumen OP BI` ← Resumen OP BI [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Operaciones IAM | yes | 633578 | 14 | 0 | - | high_missingness |
| Operaciones IVSA | no | 40689 | 16 | 0 | - | - |
| Resumen OP IVSA | no | 1729 | 3 | 2 | - | duplicate_rows |
| Resumen OP IAM | no | 2685 | 3 | 6 | - | duplicate_rows |
| Resumen OP BI | yes | 4485 | 4 | 86 | - | duplicate_rows |

### Referenced sheet column details

#### Operaciones IAM

PBIX tables: Operaciones por canal IAM

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| # Liquidación | numeric | 0.0 | 365284 |  |
| Fecha | datetime | 0.0 | 974 |  |
| Cuotapartista | numeric | 0.0 | 6214 |  |
| Cuotapartista.1 | text | 0.0 | 6202 |  |
| Moneda de Liquidación | numeric | 0.0 | 183166 |  |
| Fondo | text | 0.0 | 18 |  |
| Tipo de Liquidación | text | 0.0 | 4 |  |
| Cuotapartista.2 | numeric | 0.5 | 5793 |  |
| Condición de I/E | text | 0.0 | 8 |  |
| Canal de Venta | text | 0.0 | 3 |  |
| Unnamed: 10 | empty | 100.0 | 0 |  |
| Unnamed: 11 | empty | 100.0 | 0 |  |
| Unnamed: 12 | empty | 100.0 | 0 |  |
| Unnamed: 13 | numeric | 100.0 | 1 | candidate key |

#### Resumen OP BI

PBIX tables: Resumen OP BI

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Fecha | datetime | 1.34 | 1004 |  |
| Canal de Operacion | text | 1.34 | 6 |  |
| # Operaciones | numeric | 1.34 | 663 |  |
| Empresa | numeric | 3.37 | 2 |  |


## cheques operados.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\cheques operados.xlsx
- Size: 3.28 MB
- Modified: 2024-02-29T10:55:47
- Sheets: 4
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `CPD-cheques-vendidos` ← CPD-cheques-vendidos [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| CPD-cheques-vendidos | yes | 31820 | 19 | 0 | - | high_missingness |
| SGR | no | 62 | 10 | 0 | Unnamed: 0 | high_missingness |
| Hoja1 | no | 19 | 19 | 1 | - | duplicate_rows, high_missingness |
| Hoja2 | no | 14 | 1 | 0 | *BIF | - |

### Referenced sheet column details

#### CPD-cheques-vendidos

PBIX tables: CPD-cheques-vendidos

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| ID Cheque | numeric | 0.0 | 27362 |  |
| Custodia | text | 0.0 | 2 |  |
| Fec. Pago | datetime | 0.0 | 1129 |  |
| Fec. Conc. | datetime | 0.0 | 742 |  |
| Monto Nominal | numeric | 0.0 | 9716 |  |
| Segmento | text | 0.0 | 10 |  |
| Nro Cheque | numeric | 39.97 | 6249 |  |
| Cod Cheque | text | 0.12 | 27323 |  |
| Comit V. | numeric | 0.0 | 458 |  |
| CUIT Comprador | text | 0.0 | 148 |  |
| Cond. | text | 0.0 | 4 |  |
| Banco | text | 37.54 | 48 |  |
| Plaza | text | 42.19 | 10 |  |
| Librador | text | 90.85 | 416 |  |
| SGR | text | 0.0 | 49 |  |
| Tipo de op | text | 0.0 | 4 |  |
| No a la orden | boolean-like text | 0.19 | 2 |  |
| Moneda | text | 0.0 | 3 |  |
| Unnamed: 18 | numeric | 18.27 | 4 |  |


## clientes Bind Inversiones.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\clientes Bind Inversiones.xlsx
- Size: 8.18 MB
- Modified: 2026-03-10T15:30:09
- Sheets: 7
- Referenced sheets: 3

### PBIX tables fed by this workbook

- `Bind Inversiones` ← Bind Inversiones [Sheet]
- `IAM MOdelo` ← IAM MOdelo [Sheet]
- `IVSA MOdelo` ← IVSA MOdelo [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| IVSA | no | 8287 | 6 | 12 | - | duplicate_rows, high_missingness |
| IAM | no | 11579 | 16384 | 89 | - | duplicate_rows, high_missingness |
| compartidos | no | 7707 | 14 | 173 | - | duplicate_rows, high_missingness |
| compaginacion | no | 15113 | 16 | 0 | - | high_missingness |
| Bind Inversiones | yes | 15056 | 11 | 0 | Nº Bind Inv | - |
| IVSA MOdelo | yes | 8267 | 17 | 0 | Nº Bind Inv, Nº Bind Inv.1 | high_missingness |
| IAM MOdelo | yes | 11488 | 8 | 0 | - | - |

### Referenced sheet column details

#### Bind Inversiones

PBIX tables: Bind Inversiones

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Nº Bind Inv | numeric | 0.0 | 15056 | candidate key |
| Cuotapartista | text | 0.03 | 14737 |  |
| Banca | numeric | 0.82 | 20 |  |
| Oficial | numeric | 0.82 | 163 |  |
| Empresa | text | 0.01 | 4 |  |
| fecha inicio | text | 0.76 | 2306 |  |
| Oficial BI | numeric | 1.34 | 8 |  |
| Trader | numeric | 0.21 | 2 |  |
| Unnamed: 8 | numeric | 0.0 | 2 |  |
| cuit CNV | numeric | 0.12 | 13772 |  |
| Unnamed: 10 | numeric | 2.15 | 1 |  |

#### IVSA MOdelo

PBIX tables: IVSA MOdelo

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Nº Bind Inv | numeric | 0.0 | 8267 | candidate key |
| Nº IVSA | numeric | 0.0 | 8136 |  |
| Cuit | numeric | 0.19 | 7301 |  |
| Cliente | text | 0.0 | 8027 |  |
| Banca | numeric | 0.83 | 20 |  |
| Oficial | numeric | 0.83 | 144 |  |
| Fecha inicio | text | 0.08 | 930 |  |
| Oficial BI | numeric | 1.0 | 10 |  |
| trader | numeric | 0.02 | 6 |  |
| Unnamed: 9 | numeric | 0.0 | 1 |  |
| RESPOSABLE SALDO | numeric | 24.13 | 7 |  |
| Unnamed: 11 | empty | 100.0 | 0 |  |
| Unnamed: 12 | datetime | 99.99 | 1 | candidate key |
| Unnamed: 13 | empty | 100.0 | 0 |  |
| Unnamed: 14 | numeric | 2.59 | 8050 |  |
| Nº IVSA.1 | numeric | 0.0 | 8136 |  |
| Nº Bind Inv.1 | numeric | 0.0 | 8267 | candidate key |

#### IAM MOdelo

PBIX tables: IAM MOdelo

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Nº Bind Inv | numeric | 0.0 | 11487 |  |
| Nº IAM | numeric | 0.0 | 11475 |  |
| Cuit | numeric | 0.84 | 10523 |  |
| Cuotapartista | text | 0.04 | 11296 |  |
| Banca | numeric | 1.9 | 18 |  |
| Oficial | numeric | 1.92 | 159 |  |
| Fecha inicio | datetime | 0.33 | 2357 |  |
| Unnamed: 7 | numeric | 2.01 | 2 |  |


## Estructura Comercial.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx
- Size: 0.03 MB
- Modified: 2026-03-10T10:59:41
- Sheets: 11
- Referenced sheets: 10

### PBIX tables fed by this workbook

- `Bancas` ← Bancas [Sheet]
- `Celula` ← Celula [Sheet]
- `Clientes Traders` ← Clientes Traders [Sheet]
- `Clusters` ← Clusters [Sheet]
- `Embajadores` ← Embajadores [Sheet]
- `Empresas` ← Empresas [Sheet]
- `Oficial BI` ← Oficial BI [Sheet]
- `Oficial Banco` ← Oficial Banco [Sheet]
- `Productos` ← Productos [Sheet]
- `Region` ← Region [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Oficial BI | yes | 9 | 3 | 0 | N° Oficial BI, Oficial BI | - |
| Celula | yes | 3 | 2 | 0 | Cod, Celula | - |
| Empresas | yes | 3 | 2 | 0 | N° Empresa, Empresa | - |
| Region | yes | 3 | 2 | 0 | Cod Region, Region | - |
| Bancas | yes | 16 | 6 | 0 | N° Banca, Banca, Unnamed: 4 | high_missingness |
| Oficial Banco | yes | 174 | 6 | 0 | N° Oficial Banco, Oficial Banco, Unnamed: 5 | - |
| Embajadores | yes | 18 | 4 | 0 | Cod Embajador, Embajador | - |
| Clientes Traders | yes | 2 | 2 | 0 | Cod Trader, Trader | - |
| Clusters | yes | 8 | 2 | 0 | Cluster, Valor | - |
| Productos | yes | 46 | 3 | 0 | N° Producto | - |
| Equipo BI | no | 96 | 3 | 0 | - | high_missingness |

### Referenced sheet column details

#### Oficial BI

PBIX tables: Oficial BI

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| N° Oficial BI | numeric | 0.0 | 9 | candidate key |
| Oficial BI | text | 0.0 | 9 | candidate key |
| Email | text | 0.0 | 6 |  |

#### Celula

PBIX tables: Celula

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Cod | numeric | 0.0 | 3 | candidate key |
| Celula | text | 0.0 | 3 | candidate key |

#### Empresas

PBIX tables: Empresas

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| N° Empresa | numeric | 0.0 | 3 | candidate key |
| Empresa | text | 0.0 | 3 | candidate key |

#### Region

PBIX tables: Region

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Cod Region | numeric | 0.0 | 3 | candidate key |
| Region | text | 0.0 | 3 | candidate key |

#### Bancas

PBIX tables: Bancas

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| N° Banca | numeric | 0.0 | 16 | candidate key |
| Banca | text | 0.0 | 16 | candidate key |
| Orden | numeric | 0.0 | 7 |  |
| Unnamed: 3 | empty | 100.0 | 0 |  |
| Unnamed: 4 | text | 0.0 | 16 | candidate key |
| Unnamed: 5 | numeric | 0.0 | 16 | candidate key |

#### Oficial Banco

PBIX tables: Oficial Banco

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| N° Oficial Banco | numeric | 0.0 | 174 | candidate key |
| Oficial Banco | text | 0.0 | 174 | candidate key |
| N° Banca | numeric | 0.0 | 16 |  |
| N° Oficial BI | numeric | 0.0 | 7 |  |
| N° Celula | numeric | 0.0 | 2 |  |
| Unnamed: 5 | numeric | 0.0 | 174 | candidate key |

#### Embajadores

PBIX tables: Embajadores

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Cod Embajador | numeric | 0.0 | 18 | candidate key |
| Embajador | text | 0.0 | 18 | candidate key |
| Fecha de inicio | datetime | 0.0 | 3 |  |
| Sucursal | numeric | 0.0 | 15 |  |

#### Clientes Traders

PBIX tables: Clientes Traders

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Cod Trader | numeric | 0.0 | 2 | candidate key |
| Trader | text | 0.0 | 2 | candidate key |

#### Clusters

PBIX tables: Clusters

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Cluster | text | 12.5 | 7 | candidate key |
| Valor | numeric | 0.0 | 8 | candidate key |

#### Productos

PBIX tables: Productos

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| N° Producto | numeric | 0.0 | 46 | candidate key |
| Producto | text | 0.0 | 45 |  |
| N° Empresa | numeric | 0.0 | 3 |  |


## PEA 2023.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\PEA 2023.xlsx
- Size: 2.36 MB
- Modified: 2026-02-06T14:25:15
- Sheets: 15
- Referenced sheets: 4

### PBIX tables fed by this workbook

- `PEA embajadores` ← PEA embajadores [Sheet]
- `Presupuesto x sem x producto` ← Presupuesto x sem x producto [Sheet]
- `Presupuesto x sem y of BI` ← Presupuesto x sem y of BI [Sheet]
- `Presupuesto x sem y of Banco` ← Presupuesto x sem y of Banco [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Presupuesto x sem y of BI | yes | 10705 | 16 | 3488 | - | duplicate_rows, high_missingness |
| Presupuesto x sem y of Banco | yes | 42141 | 13 | 0 | - | high_missingness |
| Presupuesto x sem x producto | yes | 5533 | 16 | 0 | - | high_missingness |
| Presupuesto x mes y x banca IVS | no | 19 | 15 | 1 | 2022-01-01 00:00:00, 2022-02-01 00:00:00, 2022-03-01 00:00:00 | duplicate_rows, high_missingness |
| Presupuesto x mes y Banca IAM | no | 19 | 15 | 0 | 2022-01-01 00:00:00, 2022-02-01 00:00:00, 2022-03-01 00:00:00 | high_missingness |
| Presupuesto x mes y OF Banco IV | no | 66 | 15 | 0 | ID Oficial, Oficial | - |
| Presupuesto x mes y OF Banco IA | no | 104 | 15 | 0 | ID Oficial, Oficial | - |
| Ajuste pea Of BI | no | 85 | 22 | 34 | - | duplicate_rows, high_missingness |
| Presupuesto Mensual IVSA x Banc | no | 85 | 41 | 6 | - | duplicate_rows, high_missingness |
| Presupuesto Mensual IAM x Banca | no | 90 | 42 | 11 | - | duplicate_rows, high_missingness |
| Hoja3 | no | 66 | 16 | 0 | - | high_missingness |
| Hoja2 | no | 23 | 13 | 0 | Asset Class, 2022-01-01 00:00:00, 2022-02-01 00:00:00 | - |
| PEA x cant clientes | no | 14 | 6 | 0 | Banca, Bind Inversiones, Unnamed: 5 | - |
| PEA embajadores | yes | 2116 | 3 | 0 | - | - |
| Hoja1 | no | 1104 | 3 | 0 | - | - |

### Referenced sheet column details

#### Presupuesto x sem y of BI

PBIX tables: Presupuesto x sem y of BI

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 2 |  |
| ID Semana | text | 0.0 | 247 |  |
| Semana | numeric | 0.0 | 50 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 5 |  |
| PEA | numeric | 0.0 | 1647 |  |
| OF BI | numeric | 0.0 | 7 |  |
| Oficial | text | 84.12 | 7 |  |
| Unnamed: 8 | empty | 100.0 | 0 |  |
| Unnamed: 9 | text | 99.96 | 2 |  |
| Orig | numeric | 98.75 | 37 |  |
| Unnamed: 11 | numeric | 99.85 | 7 |  |
| Ajuste | numeric | 98.75 | 13 |  |
| Ajuste 2 | numeric | 99.32 | 22 |  |
| Original despues de Ajuste 1 | numeric | 99.36 | 19 |  |
| Ultima version PEA | numeric | 99.39 | 15 |  |

#### Presupuesto x sem y of Banco

PBIX tables: Presupuesto x sem y of Banco

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 2 |  |
| ID Semana | text | 0.0 | 247 |  |
| Semana | numeric | 0.0 | 50 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 5 |  |
| ID Oficial | numeric | 0.0 | 159 |  |
| PEA | numeric | 0.0 | 7094 |  |
| Unnamed: 7 | empty | 100.0 | 0 |  |
| Unnamed: 8 | numeric | 100.0 | 1 | candidate key |
| Unnamed: 9 | empty | 100.0 | 0 |  |
| Unnamed: 10 | empty | 100.0 | 0 |  |
| Unnamed: 11 | empty | 100.0 | 0 |  |
| Unnamed: 12 | numeric | 100.0 | 1 | candidate key |

#### Presupuesto x sem x producto

PBIX tables: Presupuesto x sem x producto

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Empresa | numeric | 0.0 | 2 |  |
| ID Semana | text | 0.0 | 249 |  |
| Semana | numeric | 0.0 | 51 |  |
| Mes | numeric | 0.0 | 12 |  |
| Año | numeric | 0.0 | 5 |  |
| Nº Producto | numeric | 0.0 | 29 |  |
| Producto | text | 0.0 | 31 |  |
| PEA | numeric | 0.0 | 1312 |  |
| Unnamed: 8 | numeric | 99.1 | 16 |  |
| Unnamed: 9 | numeric | 99.1 | 12 |  |
| Unnamed: 10 | numeric | 99.1 | 12 |  |
| Unnamed: 11 | numeric | 92.07 | 65 |  |
| Unnamed: 12 | empty | 100.0 | 0 |  |
| Unnamed: 13 | numeric | 99.93 | 1 |  |
| Unnamed: 14 | numeric | 99.96 | 1 |  |
| Unnamed: 15 | numeric | 99.96 | 1 |  |

#### PEA embajadores

PBIX tables: PEA embajadores

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| Fecha | datetime | 0.0 | 184 |  |
| Nº Embajador | numeric | 0.0 | 17 |  |
| PEA | numeric | 0.0 | 2 |  |


## Saldos IVSA.xlsx

- Path: G:\Comercial\Seguimiento comercial 2023\Saldos IVSA.xlsx
- Size: 30.77 MB
- Modified: 2025-09-18T11:19:36
- Sheets: 1
- Referenced sheets: 1

### PBIX tables fed by this workbook

- `Saldos ivsa` ← Listado_Pesos_y_Dolares [Sheet]

### Sheet profiling

| Sheet | Referenced | Rows | Cols | Duplicate Rows | Key Candidates | Flags |
|---|---|---:|---:|---:|---|---|
| Listado_Pesos_y_Dolares | yes | 623799 | 6 | 82636 | - | duplicate_rows |

### Referenced sheet column details

#### Listado_Pesos_y_Dolares

PBIX tables: Saldos ivsa

| Column | Type | Null % | Unique Non-Null | |
|---|---|---:|---:|---|
| 'Comitente' | numeric | 0.0 | 4205 |  |
| 'Nombre de la cuenta' | text | 0.0 | 6855 |  |
| 'Pesos Venc.' | numeric | 0.0 | 23480 |  |
| 'DOLAR CABLE     Venc' | numeric | 0.0 | 12922 |  |
| 'DOLARES         Venc' | numeric | 0.0 | 12534 |  |
| Fecha | datetime | 0.0 | 164 |  |

