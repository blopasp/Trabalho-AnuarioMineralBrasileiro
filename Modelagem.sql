use AnuarioMineralBrasileiro;

CREATE TABLE IF NOT EXISTS Dim_Regiao(
	id_Regiao smallint PRIMARY KEY auto_increment
    ,UF varchar(2) unique NOT NULL
    ,Estado varchar(50) unique NOT NULL
); 
CREATE TABLE IF NOT EXISTS Dim_Calendar(
	id_Calendar smallint PRIMARY KEY auto_increment
    ,Data Date not null
    ,Dia varchar(02) not null
    ,Mes varchar(02) not null
    ,Ano smallint not null
);
CREATE TABLE IF NOT EXISTS Dim_UnidadeMedida(
	id_UnidadeMedida int primary key auto_increment
    ,Unidade varchar(2) UNIQUE NOT NULL
    ,Descricao varchar(20) NOT NULL
    ,RelacaoQuilo float NOT NULL
);
CREATE TABLE IF NOT EXISTS Dim_SubstanciaMineral(
	id_SubstanciaMineral int primary key auto_increment
    ,SubstanciaMineral varchar(255) UNIQUE NOT NULL
    ,ClasseSubstancia  varchar(50) NOT NULL
    ,IndicacaoContida varchar(50) 
);
CREATE TABLE IF NOT EXISTS Fato_ProdutoBeneficiado(
	id_Calendar smallint not null
    ,id_Regiao smallint not null
    ,id_SubstanciaMineral int not null
    ,id_UnidadeMedida int not null
    ,QuantidadeProducao decimal(20,2)
    ,QuantidadeContido decimal(20,2)
    ,QuantidadeVenda decimal(20,2)
    ,ValorVenda decimal(20,2)
    ,CONSTRAINT fk_calendar FOREIGN KEY (id_Calendar) REFERENCES Dim_Calendar (id_Calendar)
    ,CONSTRAINT fk_regiao FOREIGN KEY (id_Regiao) REFERENCES Dim_Regiao (id_Regiao)
    ,CONSTRAINT fk_submineral FOREIGN KEY (id_SubstanciaMineral) REFERENCES DIm_SubstanciaMineral (id_SubstanciaMineral)
    ,CONSTRAINT fk_Unidade FOREIGN KEY (id_UnidadeMedida) REFERENCES Dim_UnidadeMedida (id_UnidadeMedida)
); 
alter table Dim_Regiao add column Regiao varchar(50);