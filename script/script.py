from dotenv import load_dotenv
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import pyautogui
import time

# Função para buscar data do dia anterior entre 07:00 e 22:00
def datas_dia_anterior(hora1="07:00", hora2="22:00"):
    hoje = datetime.now()
    if hoje.weekday() == 0:
        dia_anterior = hoje - timedelta(days=3)
    else:
        dia_anterior = hoje - timedelta(days=1)

    h1, m1 = map(int, hora1.split(":"))
    h2, m2 = map(int, hora2.split(":"))

    data_hora1 = datetime(dia_anterior.year, dia_anterior.month, dia_anterior.day, h1, m1)
    data_hora2 = datetime(dia_anterior.year, dia_anterior.month, dia_anterior.day, h2, m2)

    return data_hora1.strftime("%d/%m/%Y %H:%M"), data_hora2.strftime("%d/%m/%Y %H:%M")

# Tentativas automáticas com espera
def tentar(func, tentativas=3, delay=1):
    for _ in range(tentativas):
        try:
            func()
            return
        except Exception:
            time.sleep(delay)
    raise TimeoutException("⚠️ Ação falhou após múltiplas tentativas")

# Carregar variáveis do .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
email = os.getenv("EMAIL")
senha = os.getenv("SENHA")

if not email or not senha:
    raise ValueError("⚠️ EMAIL ou SENHA não encontrados no .env")

# Datas usadas no filtro
primeira_data_07, segunda_data_22 = datas_dia_anterior()

# Iniciar navegador
navegador = webdriver.Chrome()
navegador.get("https://mditi.digisac.co/login")
navegador.maximize_window()
wait = WebDriverWait(navegador, 10)

try:

    def acessarLogin():
        email_Element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        email_Element.send_keys(email)

        password_Element = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_Element.send_keys(senha)

        login_Button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='login-button-submit']")))
        login_Button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Chats']")))
        print("✅ Login realizado com sucesso!")

    acessarLogin()

    def acessarHistoricoDeChamados():
        # Acessar menu
        tentar(lambda: wait.until(EC.element_to_be_clickable((By.ID, "radix-:r0:"))).click())
        tentar(lambda: wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Histórico de chamados']"))).click())
        print("📂 Acessou 'Histórico de chamados' com sucesso.")

        # Exibir filtros
        tentar(lambda: wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='ticketHistory-button-Show-Filters']"))).click())

        def filtros_chamados():
            def clicarBotao_chamados_status():
                tentar(lambda: wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'react_select__control'))).click())
                pyautogui.write("Fechado")
                pyautogui.press("enter")

            def clicarBotao_chamados_tipoDePeriodo():
                tentar(lambda: wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Todos']"))).click())
                pyautogui.write("Data de fechamento")
                pyautogui.press("enter")

            def clicarBotao_chamados_Periodo():
                campos_data = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[data-testid="DataTime-input"]')))
                campos_data[0].click()
                campos_data[0].send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
                campos_data[0].send_keys(primeira_data_07)
                pyautogui.press("enter")

                campos_data[1].click()
                campos_data[1].send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
                campos_data[1].send_keys(segunda_data_22)
                pyautogui.press("enter")

            def clicarBotao_chamados_departamento():
                tentar(lambda: wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.react_select__single-value.css-hypuar-singleValue'))).click())
                pyautogui.write("Suporte")
                pyautogui.press("enter")

            def clicarBotao_chamados_conexao():
                tentar(lambda: wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.react_select__placeholder.css-smo73u-placeholder'))).click())
                pyautogui.write("WhatsApp")
                pyautogui.press("enter")

            clicarBotao_chamados_status()
            clicarBotao_chamados_tipoDePeriodo()
            clicarBotao_chamados_Periodo()
            clicarBotao_chamados_departamento()
            clicarBotao_chamados_conexao()

            def aplicar_e_baixar_chamados():
                tentar(lambda: wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="ticketHistory-button-Apply-Filters"]'))).click())
                tentar(lambda: wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Exportar")]'))).click())
                print("📥 Exportação iniciada com sucesso.")

            aplicar_e_baixar_chamados()

        filtros_chamados()

    acessarHistoricoDeChamados()

except Exception as e:
    print("❌ Algo deu errado.")
    navegador.save_screenshot("erro.png")
    print("📸 Screenshot salva como erro.png")
    print("🔍 Erro:", e)

finally:
    time.sleep(5)
    navegador.quit()
