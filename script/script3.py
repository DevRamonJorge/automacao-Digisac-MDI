import os
from datetime import datetime, timedelta

downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

# Data de hoje para encontrar os arquivos
def pegar_data_hoje():
    hoje = datetime.now()
    return hoje.strftime('%d_%m_%Y')

# Data usada para o novo nome: sexta-feira se hoje for segunda, senão hoje
def pegar_data_para_nome():
    hoje = datetime.now()
    if hoje.weekday() == 0:  # Segunda-feira
        sexta = hoje - timedelta(days=3)
        return sexta.strftime('%d_%m_%Y')
    else:
        return hoje.strftime('%d_%m_%Y')

# Datas
data_hoje = pegar_data_hoje()
data_para_nome = pegar_data_para_nome()

# Nomes novos com base na data ajustada
palavra_chave1 = 'historico_de_chamados'
novo_nome1 = f'DB_HISTÓRICO-CHAMADOS_{data_para_nome}.csv'

palavra_chave2 = 'estatisticas-avaliacoes'
novo_nome2 = f"DB_NPS_{data_para_nome}.csv"

def encontrar_e_renomear(data, palavra_chave, novo_nome):
    encontrado = False
    for arquivo in os.listdir(downloads):
        if data in arquivo and palavra_chave in arquivo:
            caminho_antigo = os.path.join(downloads, arquivo)
            caminho_novo = os.path.join(downloads, novo_nome)
            os.rename(caminho_antigo, caminho_novo)
            print(f"✅ Arquivo '{arquivo}' renomeado para '{novo_nome}'")
            encontrado = True
            break
    if not encontrado:
        print("❌ Nenhum arquivo com a data e nome informados foi encontrado na pasta Downloads.")

# Buscar arquivos com data de hoje, renomear com a data correta
encontrar_e_renomear(data_hoje, palavra_chave1, novo_nome1)
encontrar_e_renomear(data_hoje, palavra_chave2, novo_nome2)
