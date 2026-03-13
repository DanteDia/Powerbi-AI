# SQL Access Readiness Plan

This document captures everything that can be prepared before the real SQL schema is available.

## Current state

- Tables inventoried: 62
- Relationships inventoried: 69
- Measures inventoried: 82
- Report pages inventoried: 98
- Visuals inventoried: 479

## Working rule

Do not recreate the legacy Excel layer table-by-table unless the table represents a real business entity, real operational fact, or a business-owned overlay that still has no upstream owner.

## Domain split

- calendar: 2
- commercial: 23
- iam: 13
- ivsa: 7
- shared_or_unknown: 1
- technical: 16

## Recommended actions summary

- drop_powerbi_auto_date: 1
- keep_as_business_overlay: 12
- keep_as_small_manual_mapping: 2
- replace_with_shared_date_dimension: 2
- replace_with_sql_dimension: 11
- replace_with_sql_fact: 17
- review_after_sql_access: 17

## High-priority tables to replace with SQL facts

| Table | Domain | Priority | Source |
|---|---|---|---|
| Boletos IVSA | ivsa | high | G:\Comercial\Seguimiento comercial 2023\Boletos IVSA.xlsx |
| CPD-cheques-vendidos | ivsa | high | G:\Comercial\Seguimiento comercial 2023\cheques operados.xlsx |
| Moneda de saldos | ivsa | high | - |
| Operaciones BI | iam | high | \\CPDWFSGRPBIND\iam$\Comercial\Seguimiento comercial 2022\Boletos Bind Inversiones.xlsx |
| Operaciones BI (2) | commercial | high | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 2.xlsx |
| Operaciones BI 3 | commercial | high | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 3.xlsx |
| Operaciones BI 4 | commercial | high | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 4.xlsx |
| Operaciones BI 5 | commercial | high | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 5.xlsx |
| Operaciones BI 6 | commercial | high | G:\Comercial\Seguimiento comercial 2023\Boletos Bind Inversiones 6.xlsx |
| Operaciones IAM | iam | high | \\CPDWFSGRPBIND\iam$\Comercial\Seguimiento comercial 2022\Boletos IAM.xlsm |
| Operaciones por canal IAM | iam | high | G:\Comercial\Seguimiento comercial 2023\Canales de operacion.xlsx |
| Resumen OP BI | commercial | high | G:\Comercial\Seguimiento comercial 2023\Canales de operacion.xlsx |
| Saldos ivsa | ivsa | high | G:\Comercial\Seguimiento comercial 2023\Saldos IVSA.xlsx |
| boletos IAM 3 | iam | high | G:\Comercial\Seguimiento comercial 2023\Boletos IAM3.xlsx |
| boletos IAM 4 | iam | high | G:\Comercial\Seguimiento comercial 2023\Boletos IAM 4.xlsx |
| boletos IAM 5 | iam | high | G:\Comercial\Seguimiento comercial 2023\Boletos IAM 5.xlsx |
| boletos IAM 6 | iam | high | G:\Comercial\Seguimiento comercial 2023\Boletos IAM 6.xlsx |

## Dimension candidates to preserve conceptually

| Table | Domain | Action | Source |
|---|---|---|---|
| Banca ordenadas | commercial | replace_with_sql_dimension | - |
| Bancas | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| Clientes Traders | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| Empresas | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| IAM MOdelo | iam | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\clientes Bind Inversiones.xlsx |
| IVSA MOdelo | ivsa | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\clientes Bind Inversiones.xlsx |
| Oficial BI | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| Oficial Banco | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| Presupuesto x sem x producto | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\PEA 2023.xlsx |
| Productos | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| Region | commercial | replace_with_sql_dimension | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |

## Business overlays likely to remain curated

| Table | Domain | Source |
|---|---|---|
| CLUSTER FACTURACIÓN | shared_or_unknown | - |
| Clusters | commercial | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| Embajadores | commercial | G:\Comercial\Seguimiento comercial 2023\Estructura Comercial.xlsx |
| PEA embajadores | commercial | G:\Comercial\Seguimiento comercial 2023\PEA 2023.xlsx |
| Presupuesto x sem y of BI | commercial | G:\Comercial\Seguimiento comercial 2023\PEA 2023.xlsx |
| Presupuesto x sem y of Banco | commercial | G:\Comercial\Seguimiento comercial 2023\PEA 2023.xlsx |
| Referidos | ivsa | G:\Comercial\Seguimiento comercial 2023\Boletos Bind UY.xlsx |
| Seguimiento Bind Inversiones Sem | iam | - |
| Seguimiento Bind Inversiones mensual | iam | - |
| Seguimiento IAM mensual | iam | - |
| Seguimiento IVSA mensual | ivsa | - |
| inflación | commercial | G:\Comercial\Seguimiento comercial 2022\Seguimiento Comercial Zafiro\inflacion.xlsx |

## Low-value technical artifacts

| Table | Recommended action |
|---|---|
| Calendario | replace_with_shared_date_dimension |
| Calendario semanas | replace_with_shared_date_dimension |
| DateTableTemplate_87f2cac1-29e4-49c6-8268-c17c71d788bd | drop_powerbi_auto_date |

## Complex measures to protect during rebuild

| Measure | Complexity | SQL difficulty |
|---|---:|---|
| Bind Inversiones[Media acumulada de Recuento de Nº Bind Inv] | 10 | hard |
| Medidas[FC CPD Compra s/BG] | 10 | hard |
| Medidas[FC CPD Venta s/BG y Bain] | 10 | hard |
| Medidas[Total acumulado de Cant Clientes en Año] | 10 | hard |
| Moneda de saldos[Saldo a ayer -2] | 10 | hard |
| Moneda de saldos[Saldo a ayer -3] | 10 | hard |
| Moneda de saldos[Saldo ayer -4] | 10 | hard |
| Moneda de saldos[saldo a ayer-1] | 10 | hard |
| Pareto[Pareto %] | 10 | hard |
| Bind Inversiones[MTD de Recuento de Nº Bind Inv] | 9 | hard |
| Medidas[FC CPD s/BG] | 9 | hard |
| Medidas[Facturación acumulada] | 9 | hard |
| Medidas[PEA CPD Empresa s/ BG] | 9 | hard |
| Medidas[PEA YTD] | 9 | hard |
| Medidas[modelo Minorista] | 9 | hard |

## Questions to answer once SQL access arrives

1. Which SQL tables are the true operational sources for IAM facts?
2. Which SQL tables are the true operational sources for IVSA facts?
3. What are the durable business keys for client, investor, comitente, product, officer, and channel?
4. Which workbook overlays still need manual stewardship after SQL access?
5. Which current PBIX calculations should move into SQL views versus stay in the semantic layer?
6. Which report outputs depend on business rules that are not present in the upstream transactional schema?

## Recommended next implementation steps

1. Build a source-to-domain map for IAM vs IVSA entities.
2. Trace the highest-value dashboards to the minimum canonical facts and dimensions they need.
3. Review the complex measures first, because they are the biggest rebuild risk.
4. Replace duplicate workbook families with a single canonical fact design once SQL tables are known.
