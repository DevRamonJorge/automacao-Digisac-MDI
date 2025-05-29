import os
from datetime import datetime

downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

def pegar_data_atual():
    return datetime.now()

# Formato da data no arquivo: '29_05_2025'
data = pegar_data_atual().strftime('%d_%m_%Y')

palavra_chave1 = 'historico_de_chamados'
novo_nome1 = 'historico_final.csv'

palavra_chave2 = 'estatisticas-avaliacoes'
novo_nome2 = 'historico_final2.csv'

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

encontrar_e_Renomear(data, palavra_chave1, novo_nome1)
encontrar_e_Renomear(data, palavra_chave2, novo_nome2)
