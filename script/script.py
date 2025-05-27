from dotenv import load_dotenv
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Carregar variáveis .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Acessa as credenciais
email = os.getenv("EMAIL")
senha = os.getenv("SENHA")

# Iniciar navegador
navegador = webdriver.Chrome()
navegador.get("https://mditi.digisac.co/login")
navegador.maximize_window()

# Criar espera explícita
wait = WebDriverWait(navegador, 10)

try:
    # Preencher login
    email_Element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    email_Element.send_keys(email)

    # Preencher senha
    password_Element = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_Element.send_keys(senha)

    # Clicar no botão de login
    login_Button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button-login']")))
    login_Button.click()

    # Esperar o site carregar
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Chats']")))
    print("✅ Login realizado com sucesso!")

    # Clicar no ícone de menu superior (pode mudar dependendo do site)
    icone_menu = wait.until(EC.element_to_be_clickable((By.ID, "radix-:r0:")))
    icone_menu.click()

    # Clicar no item "Histórico de chamados"
    historico = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Histórico de chamados']")))
    historico.click()
    print("📂 Acessou 'Histórico de chamados' com sucesso.")

except Exception as e:
    print("❌ Algo deu errado.")
    navegador.save_screenshot("erro.png")
    print("📸 Screenshot salva como erro.png")
    print("🔍 Erro:", e)

finally:
    time.sleep(5)  # Tempo para ver o que aconteceu
    navegador.quit()
