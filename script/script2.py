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
    if hoje.weekday() == 0:
        dia_anterior = hoje - timedelta(days=3)
    else:
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

primeira_data_07, segunda_data_22 = datas_dia_anterior()

def rodar_script():
    # Carregar variáveis do .env
    env_path = Path(__file__).resolve().parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    email = os.getenv("EMAIL")
    senha = os.getenv("SENHA")

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

            login_Button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button-login']")))
            login_Button.click()

            wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Chats']")))
            print("✅ Login realizado com sucesso!")
        acessarLogin()

        def acessarEstatisticas_De_Avaliacoes():
            icone_menu = wait.until(EC.element_to_be_clickable((By.ID, "radix-:r0:")))
            icone_menu.click()

            estatisticasE_Avaliacoes = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Estatísticas de avaliações']")))
            estatisticasE_Avaliacoes.click()
            print("📂 Acessou 'Estatísticas de avaliações.")

            exibir_Filtro = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="stats-Evaluation-button-Show-Filters"]')))
            exibir_Filtro.click()

            def filtros_avaliacoes():
                def clicarBotao_avaliacoes_status():
                    ultimoDepartamento_avaliacoes = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'react_select__placeholder') and contains(@class, 'css-smo73u-placeholder')]")))
                    ultimoDepartamento_avaliacoes.click()
                    time.sleep(1)
                    pyautogui.write("Suporte")
                    pyautogui.press("enter")

                def clicarBotao_avaliacoes_conexao():
                    conexao_avaliacoes = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'react_select__placeholder') and text()='Selecione'])[2]")))
                    conexao_avaliacoes.click()
                    time.sleep(1)
                    pyautogui.write("WhatsApp")
                    pyautogui.press("enter")

                def clicarBotao_avaliacoes_periodo():
                    conexao_avaliacoes = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='react-select-periodType-input']/ancestor::div[contains(@class, 'react_select__value-container')]//div[contains(@class, 'react_select__single-value')]")))
                    conexao_avaliacoes.click()
                    time.sleep(1)
                    pyautogui.write("Data de fechamento")
                    pyautogui.press("enter")

                def clicarBotao_avaliacoes_deAte():
                    campos_data = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[data-testid="DataTime-input"]')))
                    campos_data[0].click()
                    campos_data[0].send_keys(Keys.CONTROL, 'a')
                    campos_data[0].send_keys(Keys.BACKSPACE)
                    campos_data[0].send_keys(primeira_data_07)
                    pyautogui.press("enter")

                    campos_data[1].click()
                    campos_data[1].send_keys(Keys.CONTROL, 'a')
                    campos_data[1].send_keys(Keys.BACKSPACE)
                    campos_data[1].send_keys(segunda_data_22)
                    pyautogui.press("enter")

                def clicarBotao_avaliacoes_tipo():
                    tipo_avaliacoes = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "react_select__placeholder") and contains(@class, "css-1wa3eu0-placeholder") and text()="Selecione"]')))
                    tipo_avaliacoes.click()
                    time.sleep(1)
                    pyautogui.write("NPS")
                    pyautogui.press("enter")

                clicarBotao_avaliacoes_status()
                clicarBotao_avaliacoes_conexao()
                clicarBotao_avaliacoes_periodo()
                clicarBotao_avaliacoes_deAte()
                clicarBotao_avaliacoes_tipo()

            filtros_avaliacoes()

            def aplicar_e_baixar_avaliacoes():
                botao_AplicarFiltros_avaliacoes = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="stats-Evaluation-Apply-Filters"]')))
                botao_AplicarFiltros_avaliacoes.click()

                def baixar_avaliacoes():
                    botao_baixar_avaliacoes = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="stats-Evaluation-button-Export-CSV"]')))
                    botao_baixar_avaliacoes.click()
                baixar_avaliacoes()

            aplicar_e_baixar_avaliacoes()
        acessarEstatisticas_De_Avaliacoes()

        return True

    except Exception as e:
        print("❌ Algo deu errado.")
        navegador.save_screenshot("erro.png")
        print("📸 Screenshot salva como erro.png")
        print("🔍 Erro:", e)
        return False

    finally:
        time.sleep(5)
        navegador.quit()

# Tentar até 5 vezes
for tentativa in range(1, 6):
    print(f"\n🔁 Tentativa {tentativa}/5")
    sucesso = rodar_script()
    if sucesso:
        print("✅ Script finalizado com sucesso.")
        break
    elif tentativa == 5:
        print("❌ Todas as tentativas falharam.")
