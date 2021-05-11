# Anuario Mineral Brasileiro (Produção Benficiada)

Modelagem dimensional de um DW e a produção de indicadores a partir dos dados extraídos do site dados.gov.br, mantidos pela Agência Nacional de Mineração. A modelagem dos metadados foram feitas a partir do software Rise Editor, a criação do banco de dados e das tabelas foram criadas através do SGBD MySQL, versão gratuita, e o processo de etl feito a partir de um script python. A representação do modelo de dados foi através da técnica star schema. São 4 tabelas dimensão (Dim_Calendar, Dim_SubstanciaMineral, Dim_Regiao, Dim_UnidadeMedida) e uma tabela fato (Fato_ProducaoBeneficiada).

O dashboard foi feito a partir do software MS Power BI, utilizando uma conexão odbc com o banco de dados mysql. Foram geradas algumas métricas em DAX para criar os indicadores. Os indicadores foram pensados em torno de quantidade produzida, quantidade de venda, e valor de venda, distribuídos em cenário, tais como: vendas por estado, os produtos que mais se destacam, representação temporal das vendas, o quantitativo total dos parâmetros e a distribuicao das vendas por regiao.

Autores:
  Bruno Ximenes
  Pablo Andreson
