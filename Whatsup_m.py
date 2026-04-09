import os
os.environ['PATH'] += ':/usr/local/bin:/usr/bin:/Library/Frameworks/Python.framework/Versions/3.13/bin'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import messagebox
import time
    

# ======== CONFIGURAÇÕES =========
mensagem = "Bom dia. Preciso de lenço umedecido. Obg."
# mensagem = "Teste2\nMensagem enviada automaticamente por IA\nDesconsiderar."
# mensagem = "Olá, comunidade escolar! Sou Marcos Rafael e estou concorrendo à consulta para diretor(a) no Ceep Para receber meu folder, ter acesso ao plano de gestão completo e ficar por dentro das nossas propostas, entre no nosso grupo de campanha no WhatsApp! Será um prazer conversar com vocês por lá."


contatos = [
"+554197194288",
# "+554384998870",
# "+554195997928",
# "+5521994948553",
# "+554391061306",
# "+554391202426",
# "+554396966771",
# "+554396436750",
"+554391801082",
# "+554391262202",
]

# ======== CHROME ========

options = Options()
options.add_argument("--headless=new")    # invisível (reativar quando terminar de testar)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-data-dir=./perfil_whatsapp")
options.add_argument("--window-size=1600,1200")

# from selenium.webdriver.chrome.service import Service

# service = Service("/opt/homebrew/bin/chromedriver")
# driver = webdriver.Chrome(service=service, options=options)


driver = webdriver.Chrome(
service=Service(ChromeDriverManager().install()),
options=options
)

print(">>> Abrindo WhatsApp Web...")
driver.get("https://web.whatsapp.com")

wait = WebDriverWait(driver, 50)

# Aguarda carregamento do WhatsApp

wait.until(
EC.presence_of_element_located(
(By.XPATH, "//div[@id='side'] | //canvas[contains(@aria-label,'QR')]")
)
)

print(">>> WhatsApp carregado!")

# ========== PROCESSA CONTATOS ==========

for numero in contatos:

    try:
        print(f"\n📞 Enviando para {numero}...")

        # Localiza barra de busca
        campo_busca = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='side']//div[@contenteditable='true']")
            )
        )

        # limpa busca anterior
        campo_busca.click()
        campo_busca.send_keys(Keys.CONTROL, "a")
        campo_busca.send_keys(Keys.DELETE)

        # digita o número
        campo_busca.send_keys(numero)
        time.sleep(1)
        campo_busca.send_keys(Keys.ENTER)

        # aguarda abrir o chat
        caixa_msg = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//footer//div[@contenteditable='true']")
            )
        )

        time.sleep(1)

        # envia mensagem
        for linha in mensagem.split("\n"):
            caixa_msg.send_keys(linha)
            caixa_msg.send_keys(Keys.SHIFT + Keys.ENTER)

        driver.execute_script(
            "arguments[0].innerHTML = arguments[1];",
            caixa_msg,
            mensagem.replace("\n", "<br>")
        )

        caixa_msg.send_keys(Keys.ENTER)

        print(f"✔ Mensagem enviada para {numero}")
        time.sleep(1)
        campo_busca.send_keys(Keys.DELETE)

    except Exception as e:
        print(f"❌ Falha com {numero}: {e}")


campo_busca.send_keys(Keys.DELETE)
print("\n>>> Finalizado.")
driver.quit()
