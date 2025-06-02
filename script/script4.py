from time import sleep

MAX_TENTATIVAS = 5

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

        # Pega a data de ontem e formata
        ontem = datetime.now() - timedelta(days=1)
        data_formatada = ontem.strftime("%d_%m_%Y")

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

        def acessarSharepoint():
            mcr365_apps = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Inicializador de aplicativos']")))
            mcr365_apps.click()

            sharepoint_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='SharePoint será aberto em uma nova guia']")))
            aba_original = navegador.current_window_handle
            sharepoint_button.click()

            wait.until(lambda driver: len(driver.window_handles) > 1)
            for aba in navegador.window_handles:
                if aba != aba_original:
                    navegador.switch_to.window(aba)
                    break
        acessarSharepoint()

        def inserindo_documentos():
            navegador.get("https://mditicombr.sharepoint.com/sites/Analisedechamados/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2FAnalisedechamados%2FDocumentos%20Compartilhados%2FBase%5Fde%5Fdados%5FChamados&viewid=bf4b0531%2D1d00%2D43a4%2Dbf1c%2D22310211d9b9")  # <== Substitua pela URL real

            carregar_pagina = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Carregar')]")))
            time.sleep(2)
            carregar_botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'text_24bde817') and contains(text(), 'Carregar')]")))
            carregar_botao.click()

            time.sleep(0.5)
            upload_arquivo_botao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automationid='uploadFileCommand']")))
            upload_arquivo_botao.click()
            time.sleep(2)

            input_upload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
            input_upload.send_keys(fr"C:\Users\RamonCorrea-MDITecno\Downloads\DB_HISTÓRICO-CHAMADOS_{data_formatada}.csv")
            time.sleep(3)
        inserindo_documentos()

        print("✅ Executado com sucesso.")
        break  # <== Se tudo der certo, para o loop

    except Exception as e:
        print("❌ Erro na tentativa", tentativa)
        try:
            navegador.save_screenshot(f"erro_tentativa_{tentativa}.png")
        except:
            pass
        print("🔍 Erro:", e)
        sleep(3)  # Espera um pouco antes de tentar de novo

    finally:
        try:
            navegador.quit()
        except:
            pass
