import os
from datetime import datetime, timedelta

downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

# Data usada para encontrar o arquivo: sempre ontem
def pegar_data_ontem():
    ontem = datetime.now() - timedelta(days=1)
    return ontem.strftime('%d_%m_%Y')

# Data usada para o novo nome: sexta-feira se hoje for segunda, senão ontem
def pegar_data_para_nome():
    hoje = datetime.now()
    if hoje.weekday() == 0:  # Segunda-feira
        sexta = hoje - timedelta(days=3)
        return sexta.strftime('%d_%m_%Y')
    else:
        return pegar_data_ontem()

# Datas
data_ontem = pegar_data_ontem()
data_para_nome = pegar_data_para_nome()

# Nomes novos com base na data ajustada
palavra_chave1 = 'historico_de_chamados'
novo_nome1 = f'DB_HISTÓRICO-CHAMADOS_{data_para_nome}.csv'

palavra_chave2 = 'estatisticas-avaliacoes'
novo_nome2 = f"DB_NPS_{data_para_nome}.csv"

def encontrar_e_Renomear(data, palavra_chave, novo_nome):
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

# Buscar arquivos com data de ontem, renomear com a data correta
encontrar_e_Renomear(data_ontem, palavra_chave1, novo_nome1)
encontrar_e_Renomear(data_ontem, palavra_chave2, novo_nome2)
