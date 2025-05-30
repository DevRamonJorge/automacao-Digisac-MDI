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

# Carregar variáveis do .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
email = os.getenv("EMAIL-SHAREPOINT")
senha = os.getenv("SENHA-SHAREPOINT")

# Iniciar navegador
navegador = webdriver.Chrome()
navegador.get("https://login.microsoftonline.com/")
navegador.maximize_window()
wait = WebDriverWait(navegador, 10)

try:

    def acessarLogin():
        # Login
        email_Element = wait.until(EC.presence_of_element_located((By.ID, 'i0116')))
        email_Element.send_keys(email)
        email_boton = wait.until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        email_boton.click()

        senha_Element = wait.until(EC.presence_of_element_located((By.ID, 'i0118')))
        senha_Element.send_keys(senha)
        senha_boton = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Entrar']")))
        senha_boton.click()

        nao_button = wait.until(EC.element_to_be_clickable((By.ID, 'idBtn_Back')))
        nao_button.click()
    acessarLogin()

    def acessarSharepoint():
        # Acessando SharePoint no Microsoft 365
        mcr365_apps = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Inicializador de aplicativos']")))
        mcr365_apps.click()

        sharepoint_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='SharePoint será aberto em uma nova guia']")))
    
        # Guardar a aba atual
        aba_original = navegador.current_window_handle

        # Clicar no botão que abre nova aba
        sharepoint_button.click()

        # Aguardar nova aba abrir
        wait.until(lambda driver: len(driver.window_handles) > 1)

        # Alternar para nova aba
        for aba in navegador.window_handles:
            if aba != aba_original:
                navegador.switch_to.window(aba)
                break
    acessarSharepoint()

    def inserindo_documentos():
        baseDe_dados_chamados = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://mditicombr.sharepoint.com/sites/Analisedechamados']")))
        baseDe_dados_chamados.click()
    inserindo_documentos()

except Exception as e:
    print("❌ Algo deu errado.")
    navegador.save_screenshot("erro.png")
    print("📸 Screenshot salva como erro.png")
    print("🔍 Erro:", e)

finally:
    time.sleep(5)
    navegador.quit()