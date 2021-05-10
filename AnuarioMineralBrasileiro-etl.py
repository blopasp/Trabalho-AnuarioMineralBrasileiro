def comando(string):
    
    con = pymysql.connect(host='localhost', user='root', password='1234', db='AnuarioMineralBrasileiro', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with con.cursor() as cursor:
            cursor.execute(string)
        con.commit()
        print("Dados inseridos")
    except:
        print("Comando inválido")

# funcao para obter o estado atraves do UF
def regiao(estado):
    if estado in ['MA','PI','CE','RN','PE','PB','SE','AL','BA']:
        return 'Nordeste'
    elif estado in ['AM', 'RR', 'RO', 'AP', 'TO', 'RO', 'AC']:
        return 'Norte'
    elif estado in ['MT', 'MS', 'GO', 'DF']:
        return 'Centro-Oeste'
    elif estado in ['SP', 'RJ', 'ES', 'MG']:
        return 'Sudeste'
    else:
        return 'Sul'

# funcao para obter a regiao atraves do UF
def estado(uf):
    if uf == 'MA':
        return 'Maranhão'
    elif uf == 'PI':
        return 'Piauí'
    elif uf == 'CE':
        return 'Ceará'
    elif uf == 'BA':
        return 'Bahia'
    elif uf == 'AL':
        return 'Alagoas'
    elif uf == 'SE':
        return 'Sergipe'
    elif uf == 'RN':
        return 'Rio Grande do Norte'
    elif uf == 'PE':
        return 'Pernambuco'
    elif uf == 'PB':
        return 'Paraíba'
    elif uf == 'AM':
        return 'Amazonas'
    elif uf == 'RR':
        return 'Roraima'
    elif uf == 'AP':
        return 'Amapá'
    elif uf == 'PA':
        return 'Pará'
    elif uf == 'TO':
        return 'Tocantins'
    elif uf == 'RO':
        return 'Rondonia'
    elif uf == 'AC':
        return 'Acre'
    elif uf == 'MT':
        return 'Mato Grosso'
    elif uf == 'MS':
        return 'Mato Grosso do Sul'
    elif uf == 'GO':
        return 'Goiás'
    elif uf == 'SP':
        return 'São Paulo'
    elif uf == 'RJ':
        return 'Rio de Janeiro'
    elif uf == 'ES':
        return 'Espirito Santo'
    elif uf == 'MG':
        return 'Minas Gerais'
    elif uf == 'PR':
        return 'Paraná'
    elif uf == 'RS':
        return 'Rio Grande do Sul'
    elif uf == 'SC':
        return 'Santa Catarina'
    elif uf == 'DF':
    	return 'Distrito Federal'
    else:
    	return ''

#função para descricao das unidades
def desUnidade(und):
	if und == 't':
		return 'tonelada'
	elif und == 'kg':
		return 'Quilograma'
	elif und == 'ct':
		return 'Quilate'
	else:
		return ''

#funcao para relacao das unidades com o quilograma
def relaQuilo(und):
	if und == 't':
		return 1000
	elif und == 'kg':
		return 1
	elif und == 'ct':
		return 0.0002
	else:
		return 0

#funcao para carregar dados para as tabelas dimensões
def carregarDimensoes(arquivo):
	for ano in arquivo['Ano base'].unique():
		data = str(ano)+'-01-01'
		data = pd.to_datetime(data)
		sql = """INSERT INTO Dim_Calendar(Data, Dia, Mes, Ano) VALUES ("{}", "{}", "{}", {})""".format(data, data.day, data.month, data.year)
		comando(sql)
	
	for uf in arquivo['UF'].unique():
		sql = """INSERT INTO Dim_Regiao(UF, Estado, Regiao) VALUES ("{}", "{}", "{}")""".format(uf, estado(uf), regiao(uf))
		comando(sql)
	
	for und in arquivo['Unidade de Medida - Produção'].unique():
		sql = """INSERT INTO Dim_UnidadeMedida(Unidade, Descricao, RelacaoQuilo) VALUES ("{}", "{}", {})""".format(und, desUnidade(und), relaQuilo(und))
		comando(sql)

	substancia = pd.DataFrame(arquivo, columns = ['Substância Mineral', 'Classe Substância', 'Indicação Contido'])
	substancia = substancia.drop_duplicates('Substância Mineral')
	substancia["Indicação Contido"] = substancia["Indicação Contido"].fillna("Sem Indicacao Contido")
	substancia.info()
	
	for row in substancia.values:
		sql = """INSERT INTO Dim_SubstanciaMineral(SubstanciaMineral, ClasseSubstancia, IndicacaoContida) VALUES ("{}", "{}", "{}")""".format(*row)
		comando(sql)
#funcao para carregar dados para a tabela fato
def carregarFato(arquivo):
	con = pymysql.connect(host='localhost', user='root', password='1234', db='AnuarioMineralBrasileiro', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	with con.cursor() as cursor:
		for i in range(len(arquivo)):
			calendar = """
				SELECT id_Calendar FROM DIM_CALENDAR WHERE ANO = {};
			""".format(arquivo['Ano base'][i])
			cursor.execute(calendar)
			calendar = cursor.fetchone()

			# carregando estado
			regiao = """
				SELECT id_Regiao FROM DIM_REGIAO WHERE UF = "{}";
			""".format(arquivo['UF'][i])
			cursor.execute(regiao)
			regiao = cursor.fetchone()

			#carrergando Substancia mineral
			substancia = """
				SELECT id_SubstanciaMineral FROM DIM_SUBSTANCIAMINERAL WHERE SubstanciaMineral = "{}"
			""".format(arquivo['Substância Mineral'][i])
			cursor.execute(substancia)
			substancia = cursor.fetchone()

			#carregando unidade de medida
			unidade = """
				SELECT id_UnidadeMedida FROM DIM_UnidadeMedida WHERE Unidade = "{}"
			""".format(arquivo['Unidade de Medida - Produção'][i])
			cursor.execute(unidade)
			unidade = cursor.fetchone()

			#inserindo dados na tabela fato
			dados = """
				insert into Fato_ProdutoBeneficiado(id_Calendar, id_Regiao, id_SubstanciaMineral, id_UnidadeMedida, QuantidadeProducao, QuantidadeContido, QuantidadeVenda, ValorVenda) VALUES(%d,%d,%d,%d,%.2f,%.2f,%.2f, %.2f)
			"""%(calendar["id_Calendar"], regiao["id_Regiao"], substancia["id_SubstanciaMineral"], unidade["id_UnidadeMedida"], arquivo["Quantidade Produção"][i], arquivo["Quantidade Contido"][i], arquivo["Quantidade Venda"][i], arquivo["Valor Venda (R$)"][i])
			cursor.execute(dados)
	con.commit()
	print("Dados Inseridos")
	con.close()	

if __name__ == '__main__':
    import pandas as pd
    import pymysql
    
    arquivo = pd.read_csv("Producao_Beneficiada.csv", encoding = "ISO-8859-1", sep=',', engine = 'python')
    
    arquivo["Quantidade Produção"] = arquivo["Quantidade Produção"].apply(lambda x: float(x.replace(".","").replace(",",".")))
    arquivo["Quantidade Contido"] = arquivo["Quantidade Contido"].apply(lambda x: float(x.replace(".","").replace(",",".")))
    arquivo["Quantidade Venda"] = arquivo["Quantidade Venda"].apply(lambda x: float(x.replace(".","").replace(",",".")))
    arquivo["Valor Venda (R$)"] = arquivo["Valor Venda (R$)"].apply(lambda x: float(x.replace(".","").replace(",",".")))
	#carregarDimensoes(arquivo)
    carregarFato(arquivo)
