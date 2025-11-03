import csv
import os

caminho = r"C:\Users\User\Downloads\01_09_2025 15_19_47_historico_de_chamados.csv"
backup = caminho + ".bak"

# Criar backup
os.replace(caminho, backup)

with open(backup, 'r', encoding='utf-8', newline='') as entrada, \
     open(caminho, 'w', encoding='utf-8', newline='') as saida:
    
    leitor = csv.reader(entrada, delimiter=';')  # ajuste se for vírgula
    escritor = csv.writer(saida, delimiter=';')

    for linha in leitor:
        nova_linha = ["00:10:00" if valor in ("17:36:02", "17:16:01") else valor for valor in linha]
        escritor.writerow(nova_linha)

print("Arquivo corrigido e salvo. Backup criado em:", backup)
