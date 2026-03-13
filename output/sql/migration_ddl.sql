-- =============================================
-- Power BI to SQL Migration — Auto-Generated DDL
-- =============================================

-- Create schemas
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dim')
    EXEC('CREATE SCHEMA dim');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'fact')
    EXEC('CREATE SCHEMA fact');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'staging')
    EXEC('CREATE SCHEMA staging');

CREATE TABLE [dim].[Banca_ordenadas] (
    [Banca_ordenadas_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [BANCA] NVARCHAR(255) NULL,
    [ORDEN] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Bancas] (
    [Bancas_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Banca] NVARCHAR(255) NULL,
    [Bancas_agrupados] NVARCHAR(255) NULL,
    [Column10] NVARCHAR(255) NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column4] NVARCHAR(255) NULL,
    [Column5] NVARCHAR(255) NULL,
    [Column6] NVARCHAR(255) NULL,
    [Column7] NVARCHAR(255) NULL,
    [Column8] NVARCHAR(255) NULL,
    [Column9] NVARCHAR(255) NULL,
    [N__Banca] NVARCHAR(255) NULL,
    [Orden] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Bind_Inversiones] (
    [Bind_Inversiones_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Banca] BIGINT NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column9] NVARCHAR(255) NULL,
    [Cuotapartista] NVARCHAR(255) NULL,
    [Empresa] NVARCHAR(255) NULL,
    [Nº_Bind_Inv] BIGINT NULL,
    [Oficial] BIGINT NULL,
    [Oficial_BI] BIGINT NULL,
    [Trader] BIGINT NULL,
    [cuit_CNV] NVARCHAR(255) NULL,
    [fecha_inicio] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Boletos_IVSA] (
    [Boletos_IVSA_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Asset_Class] NVARCHAR(255) NULL,
    [Año] NVARCHAR(255) NULL,
    [Boleto] BIGINT NULL,
    [COMITENTE] BIGINT NULL,
    [Canal] NVARCHAR(255) NULL,
    [ESPECIE] NVARCHAR(255) NULL,
    [Fecha_Operación] NVARCHAR(255) NULL,
    [Fee] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [N__Bind_Inversiones] BIGINT NULL,
    [OPERACION] NVARCHAR(255) NULL,
    [TC] NVARCHAR(255) NULL,
    [Volumen] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[CLUSTER_FACTURACIÓN] (
    [CLUSTER_FACTURACIÓN_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Cluster] NVARCHAR(255) NULL,
    [Limite_facturación] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[CPD_cheques_vendidos] (
    [CPD_cheques_vendidos_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Banco] NVARCHAR(255) NULL,
    [CUIT_Comprador] NVARCHAR(255) NULL,
    [Cod_Cheque] NVARCHAR(255) NULL,
    [Column19] NVARCHAR(255) NULL,
    [Comit_V_] BIGINT NULL,
    [Cond_] NVARCHAR(255) NULL,
    [Custodia] NVARCHAR(255) NULL,
    [Fec__Conc_] NVARCHAR(255) NULL,
    [Fec__Pago_] NVARCHAR(255) NULL,
    [ID_Cheque] BIGINT NULL,
    [IVSA_MOdelo_Cliente] NVARCHAR(255) NULL,
    [IVSA_MOdelo_Nº_Bind_Inv] BIGINT NULL,
    [Librador] NVARCHAR(255) NULL,
    [Moneda] NVARCHAR(255) NULL,
    [Monto_Nominal] NVARCHAR(255) NULL,
    [No_a_la_orden] NVARCHAR(255) NULL,
    [Nro_Cheque] BIGINT NULL,
    [Plaza] NVARCHAR(255) NULL,
    [SGR] NVARCHAR(255) NULL,
    [Segmento] NVARCHAR(255) NULL,
    [Tipo_de_op] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Calendario] (
    [Calendario_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Dia] NVARCHAR(255) NULL,
    [Habil] NVARCHAR(255) NULL,
    [ID_Semana] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Semana] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Calendario_semanas] (
    [Calendario_semanas_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [ID_Semana] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Semana] BIGINT NULL,
    [n__semana] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Canal_de_Operación_BI] (
    [Canal_de_Operación_BI_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Canal_1] NVARCHAR(255) NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Fecha_de_operacion] NVARCHAR(255) NULL,
    [Importe_real_Operacion] NVARCHAR(255) NULL,
    [N__Bind_Inversiones_1] BIGINT NULL,
    [N__de_Operacion] BIGINT NULL,
    [N__de_cliente_IAM_IVSA] BIGINT NULL,
    [Operación] NVARCHAR(255) NULL,
    [Producto_1] BIGINT NULL,
    [Volumen_BI] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Celula] (
    [Celula_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Celula] NVARCHAR(255) NULL,
    [Cod] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Clientes_Traders] (
    [Clientes_Traders_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Cod_Trader] BIGINT NULL,
    [Trader] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Clusters] (
    [Clusters_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Cluster] NVARCHAR(255) NULL,
    [Valor] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[DateTableTemplate_87f2cac1_29e4_49c6_8268_c17c71d788bd] (
    [DateTableTemplate_87f2cac1_29e4_49c6_8268_c17c71d788bd_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Embajadores] (
    [Embajadores_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Cod_Embajador] BIGINT NULL,
    [Column5] NVARCHAR(255) NULL,
    [Column6] NVARCHAR(255) NULL,
    [Column7] NVARCHAR(255) NULL,
    [Column8] NVARCHAR(255) NULL,
    [Column9] NVARCHAR(255) NULL,
    [Embajador] NVARCHAR(255) NULL,
    [Fecha_de_inicio] NVARCHAR(255) NULL,
    [Sucursal] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Empresas] (
    [Empresas_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Empresa] NVARCHAR(255) NULL,
    [N__Empresa] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[IAM_MOdelo] (
    [IAM_MOdelo_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Banca] BIGINT NULL,
    [Column10] NVARCHAR(255) NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Column8] NVARCHAR(255) NULL,
    [Column9] NVARCHAR(255) NULL,
    [Cuit] BIGINT NULL,
    [Cuotapartista] NVARCHAR(255) NULL,
    [Fecha_inicio] NVARCHAR(255) NULL,
    [Nº_Bind_Inv] BIGINT NULL,
    [Nº_IAM] BIGINT NULL,
    [Oficial] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[IVSA_MOdelo] (
    [IVSA_MOdelo_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Banca] BIGINT NULL,
    [Cliente] NVARCHAR(255) NULL,
    [Column10] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Column15] NVARCHAR(255) NULL,
    [Column16] NVARCHAR(255) NULL,
    [Column17] NVARCHAR(255) NULL,
    [Cuit] NVARCHAR(255) NULL,
    [Fecha_inicio] NVARCHAR(255) NULL,
    [Nº_Bind_Inv] BIGINT NULL,
    [Nº_IVSA] BIGINT NULL,
    [Oficial] BIGINT NULL,
    [Oficial_BI] NVARCHAR(255) NULL,
    [RESPOSABLE_SALDO] NVARCHAR(255) NULL,
    [trader] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_036f2928_2841_4ddb_9864_a544e4cd9cd3] (
    [LocalDateTable_036f2928_2841_4ddb_9864_a544e4cd9cd3_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_05265c9b_d7dc_4ed3_aa23_866fc1bc28d5] (
    [LocalDateTable_05265c9b_d7dc_4ed3_aa23_866fc1bc28d5_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_07a467dc_e26b_4ab4_8cea_ac56e7981074] (
    [LocalDateTable_07a467dc_e26b_4ab4_8cea_ac56e7981074_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Día] BIGINT NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] BIGINT NULL,
    [NroTrimestre] BIGINT NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_0c52aabc_3d0f_4cd0_a3d7_5d040abbadbf] (
    [LocalDateTable_0c52aabc_3d0f_4cd0_a3d7_5d040abbadbf_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_21aaf88e_9560_4264_9769_1b923a1eb543] (
    [LocalDateTable_21aaf88e_9560_4264_9769_1b923a1eb543_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_5487c9d7_86cb_4736_8a14_52865b52a6dc] (
    [LocalDateTable_5487c9d7_86cb_4736_8a14_52865b52a6dc_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_6659bb53_d4f6_4ccc_acd5_18ca132da20d] (
    [LocalDateTable_6659bb53_d4f6_4ccc_acd5_18ca132da20d_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_7ac6c5b8_4018_4f7d_bee3_be4301dc36f8] (
    [LocalDateTable_7ac6c5b8_4018_4f7d_bee3_be4301dc36f8_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_952f923b_f7a0_409f_8c27_f9d8fc155d49] (
    [LocalDateTable_952f923b_f7a0_409f_8c27_f9d8fc155d49_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_b3ede445_f065_4bf2_9a1b_64e8f0b84f9f] (
    [LocalDateTable_b3ede445_f065_4bf2_9a1b_64e8f0b84f9f_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Día] BIGINT NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] BIGINT NULL,
    [NroTrimestre] BIGINT NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_b6b1a558_467e_4bcd_89e8_629d03736099] (
    [LocalDateTable_b6b1a558_467e_4bcd_89e8_629d03736099_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Día] BIGINT NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] BIGINT NULL,
    [NroTrimestre] BIGINT NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_e7dcb9bf_022b_427b_b9c2_6ff9d50003c5] (
    [LocalDateTable_e7dcb9bf_022b_427b_b9c2_6ff9d50003c5_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_eee5078f_7a4b_481c_bae5_2a1dbcfd9b62] (
    [LocalDateTable_eee5078f_7a4b_481c_bae5_2a1dbcfd9b62_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Día] BIGINT NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] BIGINT NULL,
    [NroTrimestre] BIGINT NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_f20b6962_c6b9_462c_afcc_6d50c642d949] (
    [LocalDateTable_f20b6962_c6b9_462c_afcc_6d50c642d949_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Día] BIGINT NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] BIGINT NULL,
    [NroTrimestre] BIGINT NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[LocalDateTable_f8188739_932a_4162_973f_dfb89b57b593] (
    [LocalDateTable_f8188739_932a_4162_973f_dfb89b57b593_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Día] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [NroMes] NVARCHAR(255) NULL,
    [NroTrimestre] NVARCHAR(255) NULL,
    [Trimestre] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Moneda_de_saldos] (
    [Moneda_de_saldos_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [ID_Medida] BIGINT NULL,
    [Medida_seleccionada] BIGINT NULL,
    [Moneda] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Oficial_BI] (
    [Oficial_BI_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Email] NVARCHAR(255) NULL,
    [N__Oficial_BI] BIGINT NULL,
    [Oficial_BI] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Oficial_Banco] (
    [Oficial_Banco_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Column6] NVARCHAR(255) NULL,
    [N__Banca] BIGINT NULL,
    [N__Celula] NVARCHAR(255) NULL,
    [N__Oficial_BI] BIGINT NULL,
    [N__Oficial_Banco] BIGINT NULL,
    [Oficial_Banco] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_BI] (
    [Operaciones_BI_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Cod_Region] NVARCHAR(255) NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Facturacion] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [ID_Semana] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Nº_Bind_Inversiones] BIGINT NULL,
    [Nº_Cliente] BIGINT NULL,
    [PN] NVARCHAR(255) NULL,
    [Producto] BIGINT NULL,
    [Volumen] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_BI__2_] (
    [Operaciones_BI__2__SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Cod_Region] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Facturacion] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Nº_Bind_Inversiones] BIGINT NULL,
    [Nº_Cliente] BIGINT NULL,
    [PN] BIGINT NULL,
    [Producto] BIGINT NULL,
    [Volumen] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_BI_3] (
    [Operaciones_BI_3_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Cod_Region] BIGINT NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Column15] NVARCHAR(255) NULL,
    [Column16] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Facturacion] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Nº_Bind_Inversiones] BIGINT NULL,
    [Nº_Cliente] BIGINT NULL,
    [PN] NVARCHAR(255) NULL,
    [Producto] BIGINT NULL,
    [Volumen] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_BI_4] (
    [Operaciones_BI_4_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Cod_Region] BIGINT NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Column15] NVARCHAR(255) NULL,
    [Column16] NVARCHAR(255) NULL,
    [Column17] NVARCHAR(255) NULL,
    [Column18] NVARCHAR(255) NULL,
    [Column19] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Facturacion] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Nº_Bind_Inversiones] BIGINT NULL,
    [Nº_Cliente] BIGINT NULL,
    [PN] NVARCHAR(255) NULL,
    [Producto] BIGINT NULL,
    [Volumen] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_BI_5] (
    [Operaciones_BI_5_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Cod_Region] BIGINT NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Column15] NVARCHAR(255) NULL,
    [Column16] NVARCHAR(255) NULL,
    [Column17] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Facturacion] BIGINT NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Nº_Bind_Inversiones] BIGINT NULL,
    [Nº_Cliente] BIGINT NULL,
    [PN] BIGINT NULL,
    [Producto] BIGINT NULL,
    [Volumen] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_BI_6] (
    [Operaciones_BI_6_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Cod_Region] BIGINT NULL,
    [Empresa] BIGINT NULL,
    [Facturacion] BIGINT NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Nº_Bind_Inversiones] BIGINT NULL,
    [Nº_Cliente] BIGINT NULL,
    [PN] BIGINT NULL,
    [Producto] BIGINT NULL,
    [Semana] NVARCHAR(255) NULL,
    [Volumen] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_IAM] (
    [Operaciones_IAM_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [__Facturación_CP] NVARCHAR(255) NULL,
    [__PN_Cuotap___23_01_22_] NVARCHAR(255) NULL,
    [Año] BIGINT NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [NomCuotapartista] NVARCHAR(255) NULL,
    [NombreFondoAbreviado] BIGINT NULL,
    [NumCuotapartista] BIGINT NULL,
    [NumCuotapartista_1] BIGINT NULL,
    [N__Bind_Inversiones] BIGINT NULL,
    [Nº_Bind_Inversiones] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Operaciones_por_canal_IAM] (
    [Operaciones_por_canal_IAM_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [__Liquidación] BIGINT NULL,
    [Canal_de_Venta] NVARCHAR(255) NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Condición_de_I_E] NVARCHAR(255) NULL,
    [Cuit] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [IAM_MOdelo_Nº_Bind_Inv] BIGINT NULL,
    [Importe_operacion] NVARCHAR(255) NULL,
    [Importe_real_Operacion] NVARCHAR(255) NULL,
    [Nombre_Cuotapartista] NVARCHAR(255) NULL,
    [Producto] BIGINT NULL,
    [Tipo_de_operacion] NVARCHAR(255) NULL,
    [n__Cuotapartista] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[PEA_embajadores] (
    [PEA_embajadores_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Fecha] NVARCHAR(255) NULL,
    [Nº_Embajador] BIGINT NULL,
    [PEA] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Presupuesto_x_sem_x_producto] (
    [Presupuesto_x_sem_x_producto_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] BIGINT NULL,
    [Column10] NVARCHAR(255) NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column14] NVARCHAR(255) NULL,
    [Column15] NVARCHAR(255) NULL,
    [Column16] NVARCHAR(255) NULL,
    [Column9] NVARCHAR(255) NULL,
    [Columna] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [ID_Semana] NVARCHAR(255) NULL,
    [ID_Semana_Correcto] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [Nº_Producto] BIGINT NULL,
    [PEA] NVARCHAR(255) NULL,
    [Producto] NVARCHAR(255) NULL,
    [Semana] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Presupuesto_x_sem_y_of_BI] (
    [Presupuesto_x_sem_y_of_BI_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Ajuste] NVARCHAR(255) NULL,
    [Ajuste_2] NVARCHAR(255) NULL,
    [Año] NVARCHAR(255) NULL,
    [Column10] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Column9] NVARCHAR(255) NULL,
    [Empresa] NVARCHAR(255) NULL,
    [ID_Semana] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [OF_BI] NVARCHAR(255) NULL,
    [Oficial] NVARCHAR(255) NULL,
    [Orig] NVARCHAR(255) NULL,
    [Original_despues_de_Ajuste_1] NVARCHAR(255) NULL,
    [PEA] NVARCHAR(255) NULL,
    [Semana] NVARCHAR(255) NULL,
    [Ultima_version_PEA_] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Presupuesto_x_sem_y_of_Banco] (
    [Presupuesto_x_sem_y_of_Banco_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Año] NVARCHAR(255) NULL,
    [Column10] NVARCHAR(255) NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Column13] NVARCHAR(255) NULL,
    [Column8] NVARCHAR(255) NULL,
    [Column9] NVARCHAR(255) NULL,
    [Empresa] NVARCHAR(255) NULL,
    [ID_Oficial] NVARCHAR(255) NULL,
    [ID_Semana] NVARCHAR(255) NULL,
    [Mes] NVARCHAR(255) NULL,
    [PEA] NVARCHAR(255) NULL,
    [Semana] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Productos] (
    [Productos_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Agrupación_de_Productos] NVARCHAR(255) NULL,
    [N__Empresa] BIGINT NULL,
    [N__Producto] BIGINT NULL,
    [Producto] NVARCHAR(255) NULL,
    [Productos_por_empresa] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Referidos] (
    [Referidos_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Comitente] BIGINT NULL,
    [Descripcion] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Facturación__] NVARCHAR(255) NULL,
    [Facturación_CCL] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [ISIN] NVARCHAR(255) NULL,
    [Producto] BIGINT NULL,
    [Región] BIGINT NULL,
    [Tipo_de_cambio] NVARCHAR(255) NULL,
    [Volumen] BIGINT NULL,
    [nº_Bind_Inversiones] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Region] (
    [Region_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Cod_Region] BIGINT NULL,
    [Region] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Resumen_OP_BI] (
    [Resumen_OP_BI_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [__Operaciones] BIGINT NULL,
    [Canal_de_Operacion] NVARCHAR(255) NULL,
    [Empresa] BIGINT NULL,
    [Fecha] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Saldos_ivsa] (
    [Saldos_ivsa_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Cliente] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [N__Bind_Inversiones] BIGINT NULL,
    [N__Comitente] BIGINT NULL,
    [Saldo_en_Dolar_Cable] NVARCHAR(255) NULL,
    [Saldo_en_Dolar_MEP] NVARCHAR(255) NULL,
    [Saldo_en_Pesos] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Seguimiento_Bind_Inversiones_Sem] (
    [Seguimiento_Bind_Inversiones_Sem_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [CLUSTER_IAM] NVARCHAR(255) NULL,
    [CLUSTER_IVSA] NVARCHAR(255) NULL,
    [Cluster_BI] NVARCHAR(255) NULL,
    [Cluster_PN_IAM] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE_IAM] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE_IVSA] NVARCHAR(255) NULL,
    [cluster_Facturacion_IAM] NVARCHAR(255) NULL,
    [cluster_Facturacion_IVSA] NVARCHAR(255) NULL,
    [cluster_Vol_IVSA] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Seguimiento_Bind_Inversiones_mensual] (
    [Seguimiento_Bind_Inversiones_mensual_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [CLUSTER_IAM] NVARCHAR(255) NULL,
    [CLUSTER_IVSA] NVARCHAR(255) NULL,
    [Cluster_BI] NVARCHAR(255) NULL,
    [Cluster_PN_IAM] NVARCHAR(255) NULL,
    [PN_Prom] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE__IAM_] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE__IVSA_] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE_BI] NVARCHAR(255) NULL,
    [cluster_Facturacion_IAM] NVARCHAR(255) NULL,
    [cluster_Facturacion_IVSA] NVARCHAR(255) NULL,
    [cluster_Vol_IVSA] NVARCHAR(255) NULL,
    [dias_del_mes] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Seguimiento_IAM_mensual] (
    [Seguimiento_IAM_mensual_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [CLUSTER] NVARCHAR(255) NULL,
    [PN_Promedio] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE] NVARCHAR(255) NULL,
    [cluster_Facturacion] NVARCHAR(255) NULL,
    [cluster_PN] NVARCHAR(255) NULL,
    [dias_del_mes] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Seguimiento_IVSA_mensual] (
    [Seguimiento_IVSA_mensual_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [CLUSTER] NVARCHAR(255) NULL,
    [TIPO_DE_CLIENTE] NVARCHAR(255) NULL,
    [cluster_Facturacion] NVARCHAR(255) NULL,
    [cluster_Vol] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[Tabla__2_] (
    [Tabla__2__SK] INT IDENTITY(1,1) PRIMARY KEY,
    [Canal] NVARCHAR(255) NULL,
    [n_de_canal] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[boletos_IAM_3] (
    [boletos_IAM_3_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [__Facturación_CP] NVARCHAR(255) NULL,
    [__PN_Cuotap___23_01_22_] NVARCHAR(255) NULL,
    [Año] BIGINT NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [NomCuotapartista] NVARCHAR(255) NULL,
    [NombreFondoAbreviado] BIGINT NULL,
    [NumCuotapartista] BIGINT NULL,
    [N__Bind_Inversiones] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[boletos_IAM_4] (
    [boletos_IAM_4_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [__Facturación_CP] NVARCHAR(255) NULL,
    [__PN_Cuotap___23_01_22_] NVARCHAR(255) NULL,
    [Año] BIGINT NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [NomCuotapartista] NVARCHAR(255) NULL,
    [NombreFondoAbreviado] BIGINT NULL,
    [NumCuotapartista] BIGINT NULL,
    [NumCuotapartista_1] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[boletos_IAM_5] (
    [boletos_IAM_5_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [__Facturación_CP] NVARCHAR(255) NULL,
    [__PN_Cuotap___23_01_22_] NVARCHAR(255) NULL,
    [Año] BIGINT NULL,
    [Column11] NVARCHAR(255) NULL,
    [Column12] NVARCHAR(255) NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [NomCuotapartista] NVARCHAR(255) NULL,
    [NombreFondoAbreviado] BIGINT NULL,
    [NumCuotapartista] BIGINT NULL,
    [NumCuotapartista_1] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[boletos_IAM_6] (
    [boletos_IAM_6_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [__Facturación_CP] NVARCHAR(255) NULL,
    [__PN_Cuotap___23_01_22_] NVARCHAR(255) NULL,
    [Año] BIGINT NULL,
    [Fecha] NVARCHAR(255) NULL,
    [Mes] BIGINT NULL,
    [NomCuotapartista] NVARCHAR(255) NULL,
    [NombreFondoAbreviado] BIGINT NULL,
    [NumCuotapartista] BIGINT NULL,
    [NumCuotapartista_1] BIGINT NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

CREATE TABLE [dim].[inflación] (
    [inflación_SK] INT IDENTITY(1,1) PRIMARY KEY,
    [indice_tiempo] NVARCHAR(255) NULL,
    [ipc_nivel_general_nacional] NVARCHAR(255) NULL,
    [_LoadedAt] DATETIME2 DEFAULT GETDATE(),
    [_SourceFile] NVARCHAR(500) NULL
);

-- =============================================
-- Foreign Key Relationships
-- =============================================

-- ALTER TABLE [dim].[Oficial_Banco] ADD CONSTRAINT [FK_Oficial_Banco_Bancas] FOREIGN KEY ([N__Banca]) REFERENCES [dim].[Bancas] ([N__Banca]);
-- ALTER TABLE [dim].[Oficial_Banco] ADD CONSTRAINT [FK_Oficial_Banco_Oficial_BI] FOREIGN KEY ([N__Oficial_BI]) REFERENCES [dim].[Oficial_BI] ([N__Oficial_BI]);
-- ALTER TABLE [dim].[Bind_Inversiones] ADD CONSTRAINT [FK_Bind_Inversiones_Oficial_Banco] FOREIGN KEY ([Oficial]) REFERENCES [dim].[Oficial_Banco] ([N__Oficial_Banco]);
-- ALTER TABLE [dim].[Bind_Inversiones] ADD CONSTRAINT [FK_Bind_Inversiones_Clientes_Traders] FOREIGN KEY ([Trader]) REFERENCES [dim].[Clientes_Traders] ([Cod_Trader]);
-- ALTER TABLE [dim].[Bind_Inversiones] ADD CONSTRAINT [FK_Bind_Inversiones_Oficial_BI] FOREIGN KEY ([Oficial_BI]) REFERENCES [dim].[Oficial_BI] ([N__Oficial_BI]);
-- ALTER TABLE [dim].[Bind_Inversiones] ADD CONSTRAINT [FK_Bind_Inversiones_nan] FOREIGN KEY ([fecha_inicio]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_y_of_Banco] ADD CONSTRAINT [FK_Presupuesto_x_sem_y_of_Banco_Oficial_Banco] FOREIGN KEY ([ID_Oficial]) REFERENCES [dim].[Oficial_Banco] ([N__Oficial_Banco]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_y_of_Banco] ADD CONSTRAINT [FK_Presupuesto_x_sem_y_of_Banco_Empresas] FOREIGN KEY ([Empresa]) REFERENCES [dim].[Empresas] ([N__Empresa]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_y_of_Banco] ADD CONSTRAINT [FK_Presupuesto_x_sem_y_of_Banco_Calendario_semanas] FOREIGN KEY ([ID_Semana]) REFERENCES [dim].[Calendario_semanas] ([ID_Semana]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_x_producto] ADD CONSTRAINT [FK_Presupuesto_x_sem_x_producto_Productos] FOREIGN KEY ([Nº_Producto]) REFERENCES [dim].[Productos] ([N__Producto]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_x_producto] ADD CONSTRAINT [FK_Presupuesto_x_sem_x_producto_Empresas] FOREIGN KEY ([Empresa]) REFERENCES [dim].[Empresas] ([N__Empresa]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_x_producto] ADD CONSTRAINT [FK_Presupuesto_x_sem_x_producto_Calendario_semanas] FOREIGN KEY ([ID_Semana]) REFERENCES [dim].[Calendario_semanas] ([ID_Semana]);
-- ALTER TABLE [dim].[Operaciones_IAM] ADD CONSTRAINT [FK_Operaciones_IAM_Bind_Inversiones] FOREIGN KEY ([Nº_Bind_Inversiones]) REFERENCES [dim].[Bind_Inversiones] ([Nº_Bind_Inv]);
-- ALTER TABLE [dim].[Operaciones_IAM] ADD CONSTRAINT [FK_Operaciones_IAM_Calendario] FOREIGN KEY ([Fecha]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[Operaciones_IAM] ADD CONSTRAINT [FK_Operaciones_IAM_Productos] FOREIGN KEY ([NombreFondoAbreviado]) REFERENCES [dim].[Productos] ([N__Producto]);
-- ALTER TABLE [dim].[Boletos_IVSA] ADD CONSTRAINT [FK_Boletos_IVSA_Calendario] FOREIGN KEY ([Fecha_Operación]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[Boletos_IVSA] ADD CONSTRAINT [FK_Boletos_IVSA_Productos] FOREIGN KEY ([Asset_Class]) REFERENCES [dim].[Productos] ([N__Producto]);
-- ALTER TABLE [dim].[Boletos_IVSA] ADD CONSTRAINT [FK_Boletos_IVSA_Bind_Inversiones] FOREIGN KEY ([N__Bind_Inversiones]) REFERENCES [dim].[Bind_Inversiones] ([Nº_Bind_Inv]);
-- ALTER TABLE [dim].[Calendario] ADD CONSTRAINT [FK_Calendario_nan] FOREIGN KEY ([Mes]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Calendario] ADD CONSTRAINT [FK_Calendario_Calendario_semanas] FOREIGN KEY ([ID_Semana]) REFERENCES [dim].[Calendario_semanas] ([ID_Semana]);
-- ALTER TABLE [dim].[Resumen_OP_BI] ADD CONSTRAINT [FK_Resumen_OP_BI_Empresas] FOREIGN KEY ([Empresa]) REFERENCES [dim].[Empresas] ([N__Empresa]);
-- ALTER TABLE [dim].[Resumen_OP_BI] ADD CONSTRAINT [FK_Resumen_OP_BI_Calendario] FOREIGN KEY ([Fecha]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[CPD_cheques_vendidos] ADD CONSTRAINT [FK_CPD_cheques_vendidos_nan] FOREIGN KEY ([Fec__Pago_]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[CPD_cheques_vendidos] ADD CONSTRAINT [FK_CPD_cheques_vendidos_Calendario] FOREIGN KEY ([Fec__Conc_]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[IVSA_MOdelo] ADD CONSTRAINT [FK_IVSA_MOdelo_Oficial_BI] FOREIGN KEY ([Oficial_BI]) REFERENCES [dim].[Oficial_BI] ([N__Oficial_BI]);
-- ALTER TABLE [dim].[IVSA_MOdelo] ADD CONSTRAINT [FK_IVSA_MOdelo_Clientes_Traders] FOREIGN KEY ([trader]) REFERENCES [dim].[Clientes_Traders] ([Cod_Trader]);
-- ALTER TABLE [dim].[IVSA_MOdelo] ADD CONSTRAINT [FK_IVSA_MOdelo_Oficial_Banco] FOREIGN KEY ([Column10]) REFERENCES [dim].[Oficial_Banco] ([Column6]);
-- ALTER TABLE [dim].[Operaciones_por_canal_IAM] ADD CONSTRAINT [FK_Operaciones_por_canal_IAM_Bind_Inversiones] FOREIGN KEY ([IAM_MOdelo_Nº_Bind_Inv]) REFERENCES [dim].[Bind_Inversiones] ([Nº_Bind_Inv]);
-- ALTER TABLE [dim].[Operaciones_por_canal_IAM] ADD CONSTRAINT [FK_Operaciones_por_canal_IAM_Calendario] FOREIGN KEY ([Fecha]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[Canal_de_Operación_BI] ADD CONSTRAINT [FK_Canal_de_Operación_BI_Empresas] FOREIGN KEY ([Empresa]) REFERENCES [dim].[Empresas] ([N__Empresa]);
-- ALTER TABLE [dim].[Canal_de_Operación_BI] ADD CONSTRAINT [FK_Canal_de_Operación_BI_Calendario] FOREIGN KEY ([Fecha_de_operacion]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[Canal_de_Operación_BI] ADD CONSTRAINT [FK_Canal_de_Operación_BI_Bind_Inversiones] FOREIGN KEY ([N__Bind_Inversiones_1]) REFERENCES [dim].[Bind_Inversiones] ([Nº_Bind_Inv]);
-- ALTER TABLE [dim].[Canal_de_Operación_BI] ADD CONSTRAINT [FK_Canal_de_Operación_BI_Productos] FOREIGN KEY ([Producto_1]) REFERENCES [dim].[Productos] ([N__Producto]);
-- ALTER TABLE [dim].[Canal_de_Operación_BI] ADD CONSTRAINT [FK_Canal_de_Operación_BI_Tabla__2_] FOREIGN KEY ([Canal_1]) REFERENCES [dim].[Tabla__2_] ([Canal]);
-- ALTER TABLE [dim].[PEA_embajadores] ADD CONSTRAINT [FK_PEA_embajadores_Calendario] FOREIGN KEY ([Fecha]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[PEA_embajadores] ADD CONSTRAINT [FK_PEA_embajadores_Embajadores] FOREIGN KEY ([Nº_Embajador]) REFERENCES [dim].[Embajadores] ([Cod_Embajador]);
-- ALTER TABLE [dim].[Embajadores] ADD CONSTRAINT [FK_Embajadores_Oficial_Banco] FOREIGN KEY ([Sucursal]) REFERENCES [dim].[Oficial_Banco] ([N__Oficial_Banco]);
-- ALTER TABLE [dim].[Operaciones_BI__2_] ADD CONSTRAINT [FK_Operaciones_BI__2__nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_y_of_BI] ADD CONSTRAINT [FK_Presupuesto_x_sem_y_of_BI_Oficial_BI] FOREIGN KEY ([OF_BI]) REFERENCES [dim].[Oficial_BI] ([N__Oficial_BI]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_y_of_BI] ADD CONSTRAINT [FK_Presupuesto_x_sem_y_of_BI_Empresas] FOREIGN KEY ([Empresa]) REFERENCES [dim].[Empresas] ([N__Empresa]);
-- ALTER TABLE [dim].[Presupuesto_x_sem_y_of_BI] ADD CONSTRAINT [FK_Presupuesto_x_sem_y_of_BI_Calendario_semanas] FOREIGN KEY ([ID_Semana]) REFERENCES [dim].[Calendario_semanas] ([ID_Semana]);
-- ALTER TABLE [dim].[Saldos_ivsa] ADD CONSTRAINT [FK_Saldos_ivsa_Bind_Inversiones] FOREIGN KEY ([N__Bind_Inversiones]) REFERENCES [dim].[Bind_Inversiones] ([Nº_Bind_Inv]);
-- ALTER TABLE [dim].[Saldos_ivsa] ADD CONSTRAINT [FK_Saldos_ivsa_Calendario] FOREIGN KEY ([Fecha]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[inflación] ADD CONSTRAINT [FK_inflación_Calendario] FOREIGN KEY ([indice_tiempo]) REFERENCES [dim].[Calendario] ([Dia]);
-- ALTER TABLE [dim].[Operaciones_BI_3] ADD CONSTRAINT [FK_Operaciones_BI_3_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI_3] ADD CONSTRAINT [FK_Operaciones_BI_3_Region] FOREIGN KEY ([Cod_Region]) REFERENCES [dim].[Region] ([Cod_Region]);
-- ALTER TABLE [dim].[boletos_IAM_3] ADD CONSTRAINT [FK_boletos_IAM_3_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Banca_ordenadas] ADD CONSTRAINT [FK_Banca_ordenadas_Bancas] FOREIGN KEY ([BANCA]) REFERENCES [dim].[Bancas] ([Banca]);
-- ALTER TABLE [dim].[Referidos] ADD CONSTRAINT [FK_Referidos_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Referidos] ADD CONSTRAINT [FK_Referidos_Bind_Inversiones] FOREIGN KEY ([nº_Bind_Inversiones]) REFERENCES [dim].[Bind_Inversiones] ([Nº_Bind_Inv]);
-- ALTER TABLE [dim].[Operaciones_BI_4] ADD CONSTRAINT [FK_Operaciones_BI_4_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI_4] ADD CONSTRAINT [FK_Operaciones_BI_4_Region] FOREIGN KEY ([Cod_Region]) REFERENCES [dim].[Region] ([Cod_Region]);
-- ALTER TABLE [dim].[Operaciones_BI_4] ADD CONSTRAINT [FK_Operaciones_BI_4_Oficial_Banco] FOREIGN KEY ([Column13]) REFERENCES [dim].[Oficial_Banco] ([Column6]);
-- ALTER TABLE [dim].[boletos_IAM_4] ADD CONSTRAINT [FK_boletos_IAM_4_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI_5] ADD CONSTRAINT [FK_Operaciones_BI_5_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI_5] ADD CONSTRAINT [FK_Operaciones_BI_5_Region] FOREIGN KEY ([Cod_Region]) REFERENCES [dim].[Region] ([Cod_Region]);
-- ALTER TABLE [dim].[Operaciones_BI_5] ADD CONSTRAINT [FK_Operaciones_BI_5_Bancas] FOREIGN KEY ([Column13]) REFERENCES [dim].[Bancas] ([Column5]);
-- ALTER TABLE [dim].[boletos_IAM_5] ADD CONSTRAINT [FK_boletos_IAM_5_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI_6] ADD CONSTRAINT [FK_Operaciones_BI_6_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI_6] ADD CONSTRAINT [FK_Operaciones_BI_6_Region] FOREIGN KEY ([Cod_Region]) REFERENCES [dim].[Region] ([Cod_Region]);
-- ALTER TABLE [dim].[boletos_IAM_6] ADD CONSTRAINT [FK_boletos_IAM_6_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI] ADD CONSTRAINT [FK_Operaciones_BI_nan] FOREIGN KEY ([Fecha]) REFERENCES [dim].[nan] ([nan]);
-- ALTER TABLE [dim].[Operaciones_BI] ADD CONSTRAINT [FK_Operaciones_BI_Calendario_semanas] FOREIGN KEY ([ID_Semana]) REFERENCES [dim].[Calendario_semanas] ([ID_Semana]);
-- ALTER TABLE [dim].[Operaciones_BI] ADD CONSTRAINT [FK_Operaciones_BI_Bind_Inversiones] FOREIGN KEY ([Nº_Bind_Inversiones]) REFERENCES [dim].[Bind_Inversiones] ([Nº_Bind_Inv]);
-- ALTER TABLE [dim].[Operaciones_BI] ADD CONSTRAINT [FK_Operaciones_BI_Productos] FOREIGN KEY ([Producto]) REFERENCES [dim].[Productos] ([N__Producto]);
-- ALTER TABLE [dim].[Operaciones_BI] ADD CONSTRAINT [FK_Operaciones_BI_Region] FOREIGN KEY ([Cod_Region]) REFERENCES [dim].[Region] ([Cod_Region]);
-- ALTER TABLE [dim].[Operaciones_BI] ADD CONSTRAINT [FK_Operaciones_BI_Empresas] FOREIGN KEY ([Empresa]) REFERENCES [dim].[Empresas] ([N__Empresa]);
-- ALTER TABLE [dim].[Seguimiento_Bind_Inversiones_Sem] ADD CONSTRAINT [FK_Seguimiento_Bind_Inversiones_Sem_Calendario_semanas] FOREIGN KEY ([nan]) REFERENCES [dim].[Calendario_semanas] ([ID_Semana]);
-- ALTER TABLE [dim].[Seguimiento_Bind_Inversiones_mensual] ADD CONSTRAINT [FK_Seguimiento_Bind_Inversiones_mensual_nan] FOREIGN KEY ([nan]) REFERENCES [dim].[nan] ([nan]);
