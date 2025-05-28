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

# Função para buscar data do dia anterior entre 07:00 e 22:00
def datas_dia_anterior(hora1="07:00", hora2="22:00"):
    hoje = datetime.now()
    dia_anterior = hoje - timedelta(days=1)

    h1, m1 = map(int, hora1.split(":"))
    h2, m2 = map(int, hora2.split(":"))

    data_hora1 = datetime(
        year=dia_anterior.year, month=dia_anterior.month,
        day=dia_anterior.day, hour=h1, minute=m1
    )

    data_hora2 = datetime(
        year=dia_anterior.year, month=dia_anterior.month,
        day=dia_anterior.day, hour=h2, minute=m2
    )

    return data_hora1.strftime("%d/%m/%Y %H:%M"), data_hora2.strftime("%d/%m/%Y %H:%M")

# Datas usadas no filtro
primeira_data_07, segunda_data_22 = datas_dia_anterior()

# Carregar variáveis do .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
email = os.getenv("EMAIL")
senha = os.getenv("SENHA")

# Iniciar navegador
navegador = webdriver.Chrome()
navegador.get("https://mditi.digisac.co/login")
navegador.maximize_window()
wait = WebDriverWait(navegador, 10)

try:
    # Login
    email_Element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    email_Element.send_keys(email)

    password_Element = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_Element.send_keys(senha)

    login_Button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button-login']")))
    login_Button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Chats']")))
    print("✅ Login realizado com sucesso!")

    # Acessar menu > Histórico de chamados
    icone_menu = wait.until(EC.element_to_be_clickable((By.ID, "radix-:r0:")))
    icone_menu.click()

    historico = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Histórico de chamados']")))
    historico.click()
    print("📂 Acessou 'Histórico de chamados' com sucesso.")

    # Exibir filtros
    exibir_Filtro = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='ticketHistory-button-Show-Filters']")))
    exibir_Filtro.click()

    # Aplicar filtros
    def filtros_chamados():
        def clicarBotao_chamados_status():
            status_chamados = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'react_select__control')))
            status_chamados.click()
            time.sleep(1)
            pyautogui.write("Fechado")
            pyautogui.press("enter")

        def clicarBotao_chamados_tipoDePeriodo():
            tipoDePeriodo_chamados = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Todos']")))
            tipoDePeriodo_chamados.click()
            time.sleep(1)
            pyautogui.write("Data de fechamento")
            pyautogui.press("enter")

        def clicarBotao_chamados_Periodo():
            campos_data = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[data-testid="DataTime-input"]')))
            
            # "De"
            campos_data[0].click()
            campos_data[0].send_keys(Keys.CONTROL, 'a')
            campos_data[0].send_keys(Keys.BACKSPACE)
            campos_data[0].send_keys(primeira_data_07)
            pyautogui.press("enter")

            # "Até"
            campos_data[1].click()
            campos_data[1].send_keys(Keys.CONTROL, 'a')
            campos_data[1].send_keys(Keys.BACKSPACE)
            campos_data[1].send_keys(segunda_data_22)
            pyautogui.press("enter")

        clicarBotao_chamados_status()
        clicarBotao_chamados_tipoDePeriodo()
        clicarBotao_chamados_Periodo()

    filtros_chamados()

except Exception as e:
    print("❌ Algo deu errado.")
    navegador.save_screenshot("erro.png")
    print("📸 Screenshot salva como erro.png")
    print("🔍 Erro:", e)

finally:
    time.sleep(5)
    navegador.quit()