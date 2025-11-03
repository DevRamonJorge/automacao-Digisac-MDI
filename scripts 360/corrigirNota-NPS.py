import csv
import os

# Caminho do CSV original
caminho = r"C:\Users\User\Downloads\DB_NPS_29-10-2025.csv"
backup = caminho + ".bak"

# Criar backup
os.replace(caminho, backup)

# Abrir o backup para leitura e o arquivo original para escrita
with open(backup, 'r', encoding='latin1', newline='') as entrada, \
     open(caminho, 'w', encoding='latin1', newline='') as saida:
    
    leitor = csv.reader(entrada, delimiter=',')  # Altere para ';' se o arquivo usar ponto e vírgula
    escritor = csv.writer(saida, delimiter=',')

    # Lê o cabeçalho
    cabecalho = next(leitor)
    escritor.writerow(cabecalho)

    # Identifica os índices das colunas
    idx_protocolo = cabecalho.index("NÃºmero do protocolo")
    idx_nota = cabecalho.index("Nota")
    idx_classificacao = cabecalho.index("ClassificaÃ§Ã£o")  # nova linha

    protocolo_alvo = "2025102948644"

    for linha in leitor:
        if linha[idx_protocolo] == protocolo_alvo and linha[idx_nota] == "1":
            linha[idx_nota] = "10"
            linha[idx_classificacao] = "Promotor"  # altera classificação também
        escritor.writerow(linha)

print("✅ Arquivo corrigido e salvo. Backup criado em:", backup)
