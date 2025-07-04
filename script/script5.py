from time import sleep
from datetime import datetime, timedelta
import pyautogui

MAX_TENTATIVAS = 8

for tentativa in range(1, MAX_TENTATIVAS + 1):
    try:
        print(f"🟡 Tentativa {tentativa} de {MAX_TENTATIVAS}")

        from dotenv import load_dotenv
        import os
        from pathlib import Path
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        import time

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

        # Verifica se hoje é segunda-feira (0 = segunda, 6 = domingo)
        hoje = datetime.now()
        if hoje.weekday() == 0:
            # Se for segunda, usa a data da sexta-feira passada
            data_ref = hoje - timedelta(days=3)
        else:
            # Caso contrário, usa a data de ontem
            data_ref = hoje - timedelta(days=1)

        # Data formatada para o nome do arquivo
        data_formatada = data_ref.strftime("%d-%m-%Y")

        # Caminho do arquivo a ser inserido
        caminho_arquivo = fr"C:\Users\RamonCorrea-MDITecno\Downloads\DB_NPS_{data_formatada}.csv"

        def acessarLogin():
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
        time.sleep(2)
        # Ir direto para a URL do SharePoint
        navegador.get("https://mditicombr.sharepoint.com/sites/BasededadosNPS/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2FBasededadosNPS%2FDocumentos%20Compartilhados%2FBase%5Fde%5Fdados%5FNPS&viewid=bf4b0531%2D1d00%2D43a4%2Dbf1c%2D22310211d9b9")

        def inserindo_documentos():
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Carregar')]")))
            time.sleep(2)

            carregar_botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'container_cb8e3e55') and .//span[text()='Carregar']]")))
            carregar_botao.click()
            time.sleep(0.5)

            upload_arquivo_botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ms-ContextualMenu-linkContent')]//span[text()='Arquivos']")))
            upload_arquivo_botao.click()
            time.sleep(2)

            # Usando apenas pyautogui para preencher o caminho do arquivo
            pyautogui.write(caminho_arquivo)
            pyautogui.press('enter')
            time.sleep(3)

        inserindo_documentos()

        print("✅ Executado com sucesso.")
        break

    except Exception as e:
        print("❌ Erro na tentativa", tentativa)
        try:
            navegador.save_screenshot(f"erro_tentativa_{tentativa}.png")
        except:
            pass
        print("🔍 Erro:", e)
        sleep(3)

    finally:
        try:
            navegador.quit()
        except:
            pass
