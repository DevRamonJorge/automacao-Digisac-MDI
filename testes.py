import os
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis do .env (ajuste o caminho se necessário)
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Pega e-mail e senha do .env
email = os.getenv("EMAIL")
senha = os.getenv("SENHA")

def enviar_email_teste(remetente, senha_email, destinatario):
    assunto = 'Teste de envio de e-mail pelo Python'
    corpo = 'Esse é um e-mail de teste enviado pelo script Python usando SMTP e Gmail.'

    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha_email)
        servidor.send_message(msg)

if __name__ == "__main__":
    enviar_email_teste(email, senha, email)
    print("E-mail de teste enviado com sucesso!")
