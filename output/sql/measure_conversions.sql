-- =============================================
-- DAX Measures → SQL Conversion Notes
-- =============================================

-- [Media_acumulada_de_Recuento_de_Nº_Bind_Inv]: Complex DAX measure — manual conversion required
-- Original DAX: 
IF(
	ISFILTERED('Bind Inversiones'[fecha inicio]),
	ERROR("La medida rápida de inteligencia de tiempo solo se puede agrupar o filtrar mediante la jerarquía de datos proporcionada por Power BI o por l...

-- [FC_CPD_Compra_s_BG]: Complex DAX measure — manual conversion required
-- Original DAX: calculate(sum('Boletos IVSA'[Fee]), 'Boletos IVSA'[OPERACION] = "COMPRA MAV CH")*(CALCULATE(SUM('CPD-cheques-vendidos'[Monto Nominal]),'CPD-cheques-vendidos'[SGR]<>"GARANTIAS BIND S.G.R.",'CPD-cheques...

-- [FC_CPD_Venta_s_BG_y_Bain]: Complex DAX measure — manual conversion required
-- Original DAX: calculate(sum('Boletos IVSA'[Fee]), 'Boletos IVSA'[OPERACION] = "venta mav CH",'Oficial Banco'[N° Banca] in {2,3,13})*(1-(CALCULATE(SUM('CPD-cheques-vendidos'[Monto Nominal]), 'CPD-cheques-vendidos'[S...

-- [Total_acumulado_de_Cant_Clientes_en_Año]: Complex DAX measure — manual conversion required
-- Original DAX: 
CALCULATE(
	[Cant Clientes],
	FILTER(
		ALLSELECTED('Bind Inversiones'[fecha inicio].[Año]),
		ISONORAFTER('Bind Inversiones'[fecha inicio].[Año], MAX('Bind Inversiones'[fecha inicio].[Año]), DESC)
	...

-- [Saldo_a_ayer__2]: Complex DAX measure — manual conversion required
-- Original DAX: if(WEEKDAY(SELECTEDVALUE(Calendario[Dia])-2)=1, calculate([Medida a usar Promedio], DATEADD(Calendario[Dia],-4,DAY)), if(WEEKDAY(SELECTEDVALUE(Calendario[Dia])-2)=7, calculate([Medida a usar Promedio]...

-- [Saldo_a_ayer__3]: Complex DAX measure — manual conversion required
-- Original DAX: if(WEEKDAY(SELECTEDVALUE(Calendario[Dia])-3)=1, calculate([Medida a usar Promedio], DATEADD(Calendario[Dia],-5,DAY)), if(WEEKDAY(SELECTEDVALUE(Calendario[Dia])-3)=7, calculate([Medida a usar Promedio]...

-- [Saldo_ayer__4]: Complex DAX measure — manual conversion required
-- Original DAX: if(WEEKDAY(SELECTEDVALUE(Calendario[Dia])-4)=1, calculate([Medida a usar Promedio], DATEADD(Calendario[Dia],-6,DAY)), if(WEEKDAY(SELECTEDVALUE(Calendario[Dia])-4)=7, calculate([Medida a usar Promedio]...

-- [saldo_a_ayer_1]: Complex DAX measure — manual conversion required
-- Original DAX: if(WEEKDAY(SELECTEDVALUE(Calendario[Dia])-1)=1, calculate([Medida a usar Promedio], DATEADD(Calendario[Dia],-3,DAY)), calculate([Medida a usar Promedio], DATEADD(Calendario[Dia],-1,DAY)))

-- [Pareto__]: Complex DAX measure — manual conversion required
-- Original DAX: 
VAR Total = [Facturación YTD]
VAR TotalGlobal = CALCULATE([Facturación YTD],ALLSELECTED('Operaciones BI'))

return
DIVIDE(
 SUMX(FILTER(SUMMARIZE(ALLSELECTED('Operaciones BI'), 'Operaciones BI'[Nº Bi...

-- [MTD_de_Recuento_de_Nº_Bind_Inv]: Complex DAX measure — manual conversion required
-- Original DAX: 
IF(
	ISFILTERED('Bind Inversiones'[fecha inicio]),
	ERROR("La medida rápida de inteligencia de tiempo solo se puede agrupar o filtrar mediante la jerarquía de datos proporcionada por Power BI o por l...

-- [FC_CPD_s_BG]: Complex DAX measure — manual conversion required
-- Original DAX: calculate(sum('Operaciones BI'[Facturacion]), Productos[Producto] = "CPD")*(1-CALCULATE(SUM('CPD-cheques-vendidos'[Monto Nominal]),'CPD-cheques-vendidos'[SGR]="GARANTIAS BIND S.G.R.",'CPD-cheques-vend...

-- [Facturación_acumulada]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Operaciones BI'[Facturacion]), FILTER(ALLEXCEPT(Calendario, Calendario[Año]), Calendario[Dia] <= MAX(Calendario[Dia]))) 

-- [PEA_CPD_Empresa_s__BG]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Presupuesto x sem x producto'[PEA])*CONVERT("0,6236",DOUBLE),'Presupuesto x sem x producto'[Producto] = "CPD")*(1-CALCULATE(SUM('CPD-cheques-vendidos'[Monto Nominal]),'CPD-cheques-vendi...

-- [PEA_YTD]: Complex DAX measure — manual conversion required
-- Original DAX: 
CALCULATE(
    SUM('Presupuesto x sem y of Banco'[PEA]),
    FILTER(
        ALL('Calendario semanas'[Año]),
        'Calendario semanas'[Año] <= MAX('Calendario semanas'[Año])
    )
)

-- [modelo_Minorista]: Complex DAX measure — manual conversion required
-- Original DAX: if(sum('Operaciones BI'[Facturacion]) -  CALCULATE(sum('Operaciones BI'[Facturacion]), Calendario[Mes] = 6, Calendario[Año] = 2022) >= 0, sum('Operaciones BI'[Facturacion]) -  CALCULATE(sum('Operacion...

-- [suscipriones_netas_acumuladas]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Canal de Operación BI'[Importe real Operacion]),FILTER(ALL(Calendario), Calendario[Mes] <= MAX(Calendario[Mes])))

-- [Clientes_Operativos_mes_anterior]: Complex DAX measure — manual conversion required
-- Original DAX: calculate(DISTINCTCOUNT('Operaciones BI'[Nº Bind Inversiones]), PREVIOUSMONTH(Calendario[Dia]), REMOVEFILTERS('Bind Inversiones'[fecha inicio]))

-- [Clientes_acumulados]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(COUNT('Bind Inversiones'[Nº Bind Inv]), all('Bind Inversiones'),'Bind Inversiones'[fecha inicio] <= max('Bind Inversiones'[fecha inicio]))

-- [PN_modelo_minorista]: Complex DAX measure — manual conversion required
-- Original DAX: if( 'Operaciones BI'[PN Prom bi] -  CALCULATE('Operaciones BI'[PN Prom bi], Calendario[Mes] = 6, Calendario[Año] = 2022) >= 0, 'Operaciones BI'[PN Prom bi] -  CALCULATE('Operaciones BI'[PN Prom bi], C...

-- [Pareto]: Complex DAX measure — manual conversion required
-- Original DAX: 
VAR Total = [Facturación YTD]
return
 SUMX(FILTER(SUMMARIZE(ALLSELECTED('Operaciones BI'), 'Operaciones BI'[Nº Bind Inversiones],"_Total", [Facturación YTD]), [_Total] >=Total),[_Total])

-- [__Canal_Digital]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(count('Canal de Operación BI'[N° de Operacion]), KEEPFILTERS('Canal de Operación BI'[Canal.1]="WEB" || 'Canal de Operación BI'[Canal.1]="bot") )/count('Canal de Operación BI'[N° de Operacion...

-- [PEA_Productos_YTD]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Presupuesto x sem x producto'[PEA]), REMOVEFILTERS(Calendario[Mes]),KEEPFILTERS(Calendario[Año]=2023), Calendario[Mes] < MONTH(TODAY()))

-- [cant_de_Op_web]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(COUNT('Canal de Operación BI'[N° de Operacion]),'Canal de Operación BI'[Canal.1] = "web") + CALCULATE(COUNT('Canal de Operación BI'[N° de Operacion]),'Canal de Operación BI'[Canal.1] = "BOT"...

-- [__Canal_BOT]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(count('Canal de Operación BI'[N° de Operacion]), KEEPFILTERS('Canal de Operación BI'[Canal.1]="bot") )/count('Canal de Operación BI'[N° de Operacion])

-- [__OP]: Complex DAX measure — manual conversion required
-- Original DAX: COUNT('Canal de Operación BI'[N° de Operacion])/calculate(count('Canal de Operación BI'[N° de Operacion]), REMOVEFILTERS('Canal de Operación BI'[Canal.1]))

-- [__vol_de_OP]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Canal de Operación BI'[Volumen BI]), KEEPFILTERS('Canal de Operación BI'[Canal.1]="bot") )/sum('Canal de Operación BI'[Volumen BI])

-- [__de_diferencia_entre_Clientes_acumulados_y_Clientes_acumulados]: Needs manual conversion (medium)
-- Original DAX: 
VAR __BASELINE_VALUE = [Clientes acumulados]
VAR __VALUE_TO_COMPARE = [Clientes acumulados]
RETURN
	IF(
		NOT ISBLANK(__VALUE_TO_COMPARE),
		DIVIDE(__VALUE_TO_COMPARE - __BASELINE_VALUE, __BASELINE_V...

-- [Clientes_Operativos]: Complex DAX measure — manual conversion required
-- Original DAX: calculate(DISTINCTCOUNT('Operaciones BI'[Nº Bind Inversiones]),REMOVEFILTERS('Bind Inversiones'[fecha inicio]))

-- [Diferencia]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(DISTINCTCOUNT('Operaciones BI'[Nº Bind Inversiones]), KEEPFILTERS(Calendario[Año]=2022)) - CALCULATE(DISTINCTCOUNT('Operaciones BI'[Nº Bind Inversiones]), KEEPFILTERS(Calendario[Año]=2021))

-- [Facturación___YTD]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Operaciones BI'[Facturacion]),REMOVEFILTERS(Calendario[Año]), KEEPFILTERS(Calendario[Año]=2024))

-- [Facturación_2021]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Operaciones BI'[Facturacion]),REMOVEFILTERS(Calendario[Año]), KEEPFILTERS(Calendario[Año]=2021))

-- [Facturación_2022]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Operaciones BI'[Facturacion]),REMOVEFILTERS(Calendario[Año]), KEEPFILTERS(Calendario[Año]=2022))

-- [Facturación_2023]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Operaciones BI'[Facturacion]),REMOVEFILTERS(Calendario[Año]), KEEPFILTERS(Calendario[Año]=2023))

-- [Facturación_YTD]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Operaciones BI'[Facturacion]),REMOVEFILTERS(Calendario[Mes]), KEEPFILTERS(Calendario[Año]=2024))

-- [PEA_CPD_Empresa]: Complex DAX measure — manual conversion required
-- Original DAX: CALCULATE(sum('Presupuesto x sem x producto'[PEA])*CONVERT("0,6236",DOUBLE),'Presupuesto x sem x producto'[Producto] = "CPD")

-- [Medida_a_usar_por_cliente]: Needs manual conversion (medium)
-- Original DAX: if(hasonefilter('Bind Inversiones'[Cuotapartista]),SWITCH('Moneda de saldos'[Moneda seleccionada], 1, sum('Saldos ivsa'[Saldo en Pesos]), 2, sum('Saldos ivsa'[Saldo en Dolar MEP]), 3, sum('Saldos ivsa...

-- [Cant_Clientes]: Needs manual conversion (medium)
-- Original DAX: calculate(count('Bind Inversiones'[Cuotapartista]))

-- [Clientes_Nuevos]: Needs manual conversion (medium)
-- Original DAX: CALCULATE(COUNT('Bind Inversiones'[Nº Bind Inv]))

-- [DIAS_DEL_MES]: Needs manual conversion (medium)
-- Original DAX: calculate(DISTINCTCOUNT(Calendario[Dia]), Calendario[Año]=2022)

-- [DOLAR_CABLE_HOY]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar Cable]), 'Calendario'[Dia] = today())

-- [DOLAR_MEP_HOY]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar MEP]), 'Calendario'[Dia] = today())

-- [Saldo_al_inicio_CABLE]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar Cable]), Calendario[Dia]= date(2023,04,27))

-- [Saldo_al_inicio_MEP]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar MEP]), Calendario[Dia]= date(2023,04,27))

-- [Saldo_dia_anterior]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar MEP]), Calendario[Dia]=today()-7)

-- [Saldo_semana_anterior_CABLE]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar Cable]), Calendario[Dia]=today()-7)

-- [Saldo_semana_anterior_MEP]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar MEP]), Calendario[Dia]=today()-7)

-- [Saldos_hoy_CABLE]: Needs manual conversion (medium)
-- Original DAX: calculate(sum('Saldos ivsa'[Saldo en Dolar Cable]), 'Saldos ivsa'[Fecha]=TODAY())

-- [Saldos_hoy_MEP]: Needs manual conversion (medium)
-- Original DAX: calculate(sum('Saldos ivsa'[Saldo en Dolar MEP]), 'Saldos ivsa'[Fecha]=TODAY())

-- [Saldos_pesos_hoy]: Needs manual conversion (medium)
-- Original DAX: calculate(sum('Saldos ivsa'[Saldo en Pesos]), 'Saldos ivsa'[Fecha]=TODAY())

-- [saldo_a_fin_de_mes_CABLE]: Needs manual conversion (medium)
-- Original DAX: Calculate(sum('Saldos ivsa'[Saldo en Dolar Cable]), Calendario[Dia]= date(2023,05,31))

-- [Performance_YTD]: Needs manual conversion (medium)
-- Original DAX: CALCULATE([Facturación YTD])/CALCULATE([PEA YTD])

-- [porcentaje_de_participacion]: Needs manual conversion (easy)
-- Original DAX: sum('CPD-cheques-vendidos'[Monto Nominal])/ sumx(ALLSELECTED('CPD-cheques-vendidos'),'CPD-cheques-vendidos'[Monto Nominal])

-- [Medida_a_usar]: Needs manual conversion (easy)
-- Original DAX: SWITCH('Moneda de saldos'[Moneda seleccionada], 1, Medidas[Saldos pesos hoy], 2, Medidas[Saldos hoy MEP], 3, Medidas[Saldos hoy CABLE])

-- [Medida_a_usar_Promedio]: Needs manual conversion (easy)
-- Original DAX: SWITCH('Moneda de saldos'[Moneda seleccionada], 1,[Pesos Promedio], 2, 'Moneda de saldos'[Mep Promedio], 3, [Cable Promedio])

-- [clasificacion_ABC]: Needs manual conversion (easy)
-- Original DAX: SWITCH(true(), Pareto[Pareto %]<=0.8,"A",Pareto[Pareto %]>0.8,"B","C")

-- [PN_Prom]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones IAM'[$ PN Cuotap. (23/01/22)])/DISTINCTCOUNT('Operaciones IAM'[Fecha])

-- [indice_fact_vol]: Needs manual conversion (easy)
-- Original DAX: sum('Boletos IVSA'[Fee])/sum('Boletos IVSA'[Volumen])

-- [Comisión_embajadores]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])*0.15

-- [Cant_OP_x_spread]: Needs manual conversion (easy)
-- Original DAX: [fc/vol]*COUNT('Operaciones BI'[Nº Bind Inversiones])

-- [Cant_de_operaciones]: Needs manual conversion (easy)
-- Original DAX: count('Boletos IVSA'[Boleto])+count('Operaciones por canal IAM'[n° Cuotapartista])

-- [Comprativo_año_anterior]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])/[Facturación 2022]

-- [Crecimiento]: Needs manual conversion (easy)
-- Original DAX: sum('Presupuesto x sem y of Banco'[PEA])/[Facturación YTD]-1

-- [Hoy]: Needs manual conversion (easy)
-- Original DAX: TODAY()

-- [Performance_BI]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])/sum('Presupuesto x sem y of Bi'[PEA])

-- [Vol_total]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Volumen])+ 'Operaciones BI'[PN Prom bi]

-- [fc_con_referidos]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion]) + sum(Referidos[Facturación $])

-- [fc_vol]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])/sum('Operaciones BI'[Volumen])

-- [fc_vol_Total]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])/'Medidas'[Vol total]

-- [performance_con_referidoss]: Needs manual conversion (easy)
-- Original DAX: [fc con referidos]/ sum('Presupuesto x sem y of BI'[PEA])

-- [vol_x_spread]: Needs manual conversion (easy)
-- Original DAX: [fc/vol]*sum('Operaciones BI'[Volumen])

-- [vol_q_ops]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Volumen])/COUNT('Operaciones BI'[Nº Cliente])

-- [Cable_Promedio]: Needs manual conversion (easy)
-- Original DAX: SUM('Saldos ivsa'[Saldo en Dolar Cable])/DISTINCTCOUNT('Saldos ivsa'[Fecha])

-- [Mep_Promedio]: Needs manual conversion (easy)
-- Original DAX: SUM('Saldos ivsa'[Saldo en Dolar MEP])/DISTINCTCOUNT('Saldos ivsa'[Fecha])

-- [Moneda_seleccionada]: Needs manual conversion (easy)
-- Original DAX: SELECTEDVALUE('Moneda de saldos'[ID Medida])

-- [Pesos_Promedio]: Needs manual conversion (easy)
-- Original DAX: SUM('Saldos ivsa'[Saldo en Pesos])/DISTINCTCOUNT('Saldos ivsa'[Fecha])

-- [PN_Prom_bi]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[PN])/DISTINCTCOUNT('Operaciones BI'[Fecha])

-- [Performance]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])/sum('Presupuesto x sem y of Banco'[PEA])

-- [performance_producto]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])/sum('Presupuesto x sem x producto'[PEA])

-- [Perfromance_Embajadores]: Needs manual conversion (easy)
-- Original DAX: sum('Operaciones BI'[Facturacion])/sum('PEA embajadores'[PEA])

-- [Medida]: Needs manual conversion (easy)
-- Original DAX: 

-- [Performance_Cheques_Empresa]: Needs manual conversion (easy)
-- Original DAX: [FC CPD s/BG]/[PEA CPD Empresa s/ BG]

-- [dif_mes_anterior]: Needs manual conversion (easy)
-- Original DAX: [Clientes Operativos]-[Clientes Operativos mes anterior]
