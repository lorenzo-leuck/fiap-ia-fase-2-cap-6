-- Criação das Tabelas para o Sistema de Sensores Agrícolas da FarmTech Solutions (SQLite)

-- Tabela de Sensores
CREATE TABLE Sensor (
    SensorID INTEGER PRIMARY KEY AUTOINCREMENT,
    TipoSensor TEXT NOT NULL,
    Localizacao TEXT,
    DataInstalacao TEXT,
    Status TEXT
);

-- Tabela de Tipos de Cultura
CREATE TABLE TipoCultura (
    TipoCulturaID INTEGER PRIMARY KEY AUTOINCREMENT,
    NomeCultura TEXT NOT NULL,
    DescricaoCultura TEXT,
    TempoMedioCiclo INTEGER,
    NecessidadeHidricaMedia REAL,
    NecessidadeNutrientesMedia TEXT
);

-- Tabela de Culturas
CREATE TABLE Cultura (
    CulturaID INTEGER PRIMARY KEY AUTOINCREMENT,
    TipoCulturaID INTEGER NOT NULL,
    Variedade TEXT,
    DataPlantio TEXT,
    DataColheitaPrevista TEXT,
    AreaHectare REAL,
    ProducaoEstimada REAL,
    FOREIGN KEY (TipoCulturaID) REFERENCES TipoCultura(TipoCulturaID)
);

-- Tabela de Talhões
CREATE TABLE Talhao (
    TalhaoID INTEGER PRIMARY KEY AUTOINCREMENT,
    CulturaID INTEGER NOT NULL,
    NomeTalhao TEXT,
    AreaHectare REAL,
    DensidadePlantio REAL,
    EspacamentoEntreLinhas REAL,
    CicloVegetativo TEXT,
    Latitude REAL,
    Longitude REAL,
    Altitude REAL,
    TipoSolo TEXT,
    FOREIGN KEY (CulturaID) REFERENCES Cultura(CulturaID)
);

-- Tabela de Leituras de Sensores
CREATE TABLE LeituraSensor (
    LeituraID INTEGER PRIMARY KEY AUTOINCREMENT,
    SensorID INTEGER NOT NULL,
    TalhaoID INTEGER NOT NULL,
    DataHora TEXT NOT NULL,
    ValorLeitura REAL,
    Unidade TEXT,
    FOREIGN KEY (SensorID) REFERENCES Sensor(SensorID),
    FOREIGN KEY (TalhaoID) REFERENCES Talhao(TalhaoID)
);

-- Tabela de Leituras de Umidade (S1)
CREATE TABLE LeituraUmidade (
    LeituraUmidadeID INTEGER PRIMARY KEY AUTOINCREMENT,
    LeituraID INTEGER NOT NULL,
    PercentualUmidade REAL,
    ProfundidadeMedicao REAL,
    TemperaturaAmbiente REAL,
    FOREIGN KEY (LeituraID) REFERENCES LeituraSensor(LeituraID)
);

-- Tabela de Leituras de pH (S2)
CREATE TABLE LeituraPH (
    LeituraPHID INTEGER PRIMARY KEY AUTOINCREMENT,
    LeituraID INTEGER NOT NULL,
    ValorPH REAL,
    ProfundidadeMedicao REAL,
    FOREIGN KEY (LeituraID) REFERENCES LeituraSensor(LeituraID)
);

-- Tabela de Leituras de Nutrientes (S3)
CREATE TABLE LeituraNutrientes (
    LeituraNutrientesID INTEGER PRIMARY KEY AUTOINCREMENT,
    LeituraID INTEGER NOT NULL,
    NivelFosforo REAL,
    NivelPotassio REAL,
    NivelNitrogenio REAL,
    ProfundidadeMedicao REAL,
    FOREIGN KEY (LeituraID) REFERENCES LeituraSensor(LeituraID)
);

-- Tabela de Irrigação
CREATE TABLE Irrigacao (
    IrrigacaoID INTEGER PRIMARY KEY AUTOINCREMENT,
    TalhaoID INTEGER NOT NULL,
    DataHora TEXT NOT NULL,
    QuantidadeAgua REAL,
    DuracaoMinutos INTEGER,
    TipoIrrigacao TEXT,
    PressaoAgua REAL,
    FonteAgua TEXT,
    FOREIGN KEY (TalhaoID) REFERENCES Talhao(TalhaoID)
);

-- Tabela de Aplicação de Nutrientes
CREATE TABLE AplicacaoNutrientes (
    AplicacaoID INTEGER PRIMARY KEY AUTOINCREMENT,
    TalhaoID INTEGER NOT NULL,
    DataHora TEXT NOT NULL,
    TipoNutriente TEXT,
    Quantidade REAL,
    MetodoAplicacao TEXT,
    CondicaoClimatica TEXT,
    Formulacao TEXT,
    FOREIGN KEY (TalhaoID) REFERENCES Talhao(TalhaoID)
);

-- Tabela de Histórico Climático
CREATE TABLE HistoricoClimatico (
    HistoricoID INTEGER PRIMARY KEY AUTOINCREMENT,
    TalhaoID INTEGER NOT NULL,
    DataHora TEXT NOT NULL,
    Temperatura REAL,
    Precipitacao REAL,
    UmidadeAr REAL,
    VelocidadeVento REAL,
    DirecaoVento TEXT,
    RadiacaoSolar REAL,
    FOREIGN KEY (TalhaoID) REFERENCES Talhao(TalhaoID)
);

-- Tabela de Previsões e Recomendações
CREATE TABLE PrevisaoRecomendacao (
    PrevisaoID INTEGER PRIMARY KEY AUTOINCREMENT,
    TalhaoID INTEGER NOT NULL,
    DataHoraGeracao TEXT NOT NULL,
    TipoPrevisao TEXT,
    DescricaoRecomendacao TEXT,
    PrioridadeAcao INTEGER,
    DataLimiteAcao TEXT,
    EconomiaEstimada REAL,
    FOREIGN KEY (TalhaoID) REFERENCES Talhao(TalhaoID)
);

-- Tabela para armazenar os dados do FarmTech App
CREATE TABLE FarmTechDados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_lote TEXT NOT NULL,
    cultura INTEGER NOT NULL,
    comprimento INTEGER NOT NULL,
    largura INTEGER NOT NULL
);



-- Inserção de dados de exemplo para tipos de cultura
INSERT INTO TipoCultura (NomeCultura, DescricaoCultura, TempoMedioCiclo, NecessidadeHidricaMedia, NecessidadeNutrientesMedia)
VALUES ('Soja', 'Cultura de grãos oleaginosos, rica em proteínas', 120, 450, 'NPK 00-20-20');

INSERT INTO TipoCultura (NomeCultura, DescricaoCultura, TempoMedioCiclo, NecessidadeHidricaMedia, NecessidadeNutrientesMedia)
VALUES ('Milho', 'Cereal utilizado para alimentação humana e animal', 150, 600, 'NPK 04-14-08');

INSERT INTO TipoCultura (NomeCultura, DescricaoCultura, TempoMedioCiclo, NecessidadeHidricaMedia, NecessidadeNutrientesMedia)
VALUES ('Algodão', 'Cultura de fibra natural utilizada na indústria têxtil', 180, 700, 'NPK 04-20-20');

INSERT INTO TipoCultura (NomeCultura, DescricaoCultura, TempoMedioCiclo, NecessidadeHidricaMedia, NecessidadeNutrientesMedia)
VALUES ('Café', 'Cultura perene produtora de grãos para bebidas', 730, 1500, 'NPK 20-05-20');

INSERT INTO TipoCultura (NomeCultura, DescricaoCultura, TempoMedioCiclo, NecessidadeHidricaMedia, NecessidadeNutrientesMedia)
VALUES ('Cana-de-açúcar', 'Cultura semi-perene utilizada para produção de açúcar e etanol', 365, 1500, 'NPK 05-25-25');
