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

""" Função para buscar data do dia anterior """
def datas_dia_anterior(hora1="07:00", hora2="22:00"):
    hoje = datetime.now()
    dia_anterior = hoje - timedelta(days=1)

    # Extrai hora e minuto da primeira hora
    h1, m1 = map(int, hora1.split(":"))
    # Extrai hora e minuto da segunda hora
    h2, m2 = map(int, hora2.split(":"))

    data_hora1 = datetime(
        year=dia_anterior.year,
        month=dia_anterior.month,
        day=dia_anterior.day,
        hour=h1,
        minute=m1
    )

    data_hora2 = datetime(
        year=dia_anterior.year,
        month=dia_anterior.month,
        day=dia_anterior.day,
        hour=h2,
        minute=m2
    )

    return data_hora1.strftime("%d/%m/%Y %H:%M"), data_hora2.strftime("%d/%m/%Y %H:%M")
# Uso:
primeira_data_07, segunda_data_22 = datas_dia_anterior()


"""" Código Main """
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

    # Função para aplicar os filtros
    def filtros_chamados():

        # Função interna para selecionar o status "Fechado"
        def clicarBotao_chamados_status():
            status_chamados = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'react_select__control')))
            status_chamados.click()
            time.sleep(1)  # Pequena pausa para garantir que o dropdown abriu
            pyautogui.write("Fechado")
            pyautogui.press("enter")

        # Função interna para selecionar o tipo de período "Últimos 30 dias"
        def clicarBotao_chamados_tipoDePeriodo():
            tipoDePeriodo_chamados = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Todos']")))
            tipoDePeriodo_chamados.click()
            time.sleep(1)
            pyautogui.write("Data de fechamento")
            pyautogui.press("enter")

        def clicarBotao_chamados_Periodo_De():
            de_chamados = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Todos']")))
            de_chamados.click()
            time.sleep(1)
            pyautogui.write(primeira_data_07)
            pyautogui.press("enter")

        # Chamar as funções internas para aplicar os filtros
        clicarBotao_chamados_status()
        clicarBotao_chamados_tipoDePeriodo()
        clicarBotao_chamados_Periodo_De()

    # Executa a função principal que aplica os filtros
    filtros_chamados()

except Exception as e:
    print("❌ Algo deu errado.")
    navegador.save_screenshot("erro.png")  # Salva uma captura de tela do erro
    print("📸 Screenshot salva como erro.png")
    print("🔍 Erro:", e)

finally:
    time.sleep(5)  # Tempo para visualizar o resultado final antes de fechar
    navegador.quit()  # Fecha o navegador
