from dotenv import load_dotenv
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import pyautogui

# Função para pegar data e hora do dia anterior formatada
def data_hora_dia_anterior(hora_str="07:00"):
    hoje = datetime.now()
    dia_anterior = hoje - timedelta(days=1)
    hora, minuto = map(int, hora_str.split(":"))
    resultado = datetime(
        year=dia_anterior.year,
        month=dia_anterior.month,
        day=dia_anterior.day,
        hour=hora,
        minute=minuto
    )
    return resultado.strftime("%d/%m/%Y %H:%M")

# Carregar variáveis do arquivo .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Acessa as credenciais
email = os.getenv("EMAIL")
senha = os.getenv("SENHA")

# Iniciar navegador Chrome
navegador = webdriver.Chrome()
navegador.get("https://mditi.digisac.co/login")
navegador.maximize_window()

# Criar espera explícita
wait = WebDriverWait(navegador, 10)

try:
    # Preencher campo de e-mail
    email_Element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    email_Element.send_keys(email)

    # Preencher campo de senha
    password_Element = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_Element.send_keys(senha)

    # Clicar no botão de login
    login_Button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button-login']")))
    login_Button.click()

    # Esperar o site carregar completamente (verifica pela presença de "Chats")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Chats']")))
    print("✅ Login realizado com sucesso!")

    # Clicar no ícone de menu superior
    icone_menu = wait.until(EC.element_to_be_clickable((By.ID, "radix-:r0:")))
    icone_menu.click()

    # Clicar no item "Histórico de chamados"
    historico = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Histórico de chamados']")))
    historico.click()
    print("📂 Acessou 'Histórico de chamados' com sucesso.")

    # Clicar no botão "Exibir Filtros"
    exibir_Filtro = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='ticketHistory-button-Show-Filters']")))
    exibir_Filtro.click()

    # Obter data e hora do filtro desejado
    data_filtro = data_hora_dia_anterior("07:00")
    print("Data e hora do filtro:", data_filtro)

    # Função para aplicar o filtro de status "Fechado"
    def filtros_chamados():

        def clicarBotão_chamados():
            status_chamados = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'react_select__control')))
            status_chamados.click()
            pyautogui.write("Fechado")
            pyautogui.press("enter")
        clicarBotão_chamados()

    filtros_chamados()

except Exception as e:
    print("❌ Algo deu errado.")
    navegador.save_screenshot("erro.png")  # Salva uma captura de tela do erro
    print("📸 Screenshot salva como erro.png")
    print("🔍 Erro:", e)

finally:
    time.sleep(5)  # Tempo para visualizar o resultado final
    navegador.quit()  # Fecha o navegador
