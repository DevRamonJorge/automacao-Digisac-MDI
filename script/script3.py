import os
from datetime import datetime, timedelta

# Função para calcular a data para nomear o arquivo
def calcular_data_para_nome():
    hoje = datetime.today()
    # Se hoje for segunda-feira (weekday == 0)
    if hoje.weekday() == 0:
        # sexta-feira passada: hoje - 3 dias
        data_ajustada = hoje - timedelta(days=3)
    else:
        # qualquer outro dia: dia anterior (hoje - 1)
        data_ajustada = hoje - timedelta(days=1)
    return data_ajustada.strftime('%d-%m-%Y')

# Caminho da pasta Downloads (ajuste se necessário)
pasta_downloads = os.path.expanduser('~/Downloads')

# Data para nomear
data_para_nome = calcular_data_para_nome()

# Palavras-chave e novos nomes
palavra_chave1 = 'historico_de_chamados'
novo_nome1 = f'DB_HISTÓRICO-CHAMADOS_{data_para_nome}.csv'

palavra_chave2 = 'estatisticas-avaliacoes'
novo_nome2 = f'DB_NPS_{data_para_nome}.csv'

# Listar arquivos na pasta downloads
arquivos = os.listdir(pasta_downloads)

# Função para renomear arquivo
def renomear_arquivo(pasta, arquivo_antigo, novo_nome):
    caminho_antigo = os.path.join(pasta, arquivo_antigo)
    caminho_novo = os.path.join(pasta, novo_nome)
    # Se o arquivo com o novo nome já existir, evita sobrescrever
    if os.path.exists(caminho_novo):
        print(f"Aviso: {novo_nome} já existe. Não será renomeado.")
    else:
        os.rename(caminho_antigo, caminho_novo)
        print(f'Renomeado: {arquivo_antigo} -> {novo_nome}')

# Procurar e renomear arquivos
for arquivo in arquivos:
    if palavra_chave1 in arquivo.lower():
        renomear_arquivo(pasta_downloads, arquivo, novo_nome1)
    elif palavra_chave2 in arquivo.lower():
        renomear_arquivo(pasta_downloads, arquivo, novo_nome2)
