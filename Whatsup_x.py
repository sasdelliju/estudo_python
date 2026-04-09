# Whatsup_x.py — VERSÃO QUE NUNCA CRASHA (Apple Silicon + Headless 2025)
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Import correto do ChromeType (2025)
try:
    from webdriver_manager.core.os_manager import ChromeType
except ImportError:
    from webdriver_manager.core.utils import ChromeType

# ================== CONFIGURAÇÕES ==================
mensagem = "Teste2\nMensagem enviada automaticamente por IA\nDesconsiderar."
contatos = ["+554197194288"]
# ==================================================

options = Options()
options.add_argument("--headless=chrome")  # ← A QUE FUNCIONA NO M1/M2/M3
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-data-dir=./perfil_whatsapp")
options.add_argument("--remote-debugging-port=9222")

# Remove sinais de automação (WhatsApp não detecta)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())

print("Iniciando WhatsApp Web (headless real)...")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com")

wait = WebDriverWait(driver, 60)
print("Escaneie o QR Code (60s)...")
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='side']")))
    print("Conectado com sucesso!")
except:
    print("QR Code não escaneado a tempo.")
    driver.quit()
    input("Pressione ENTER para fechar...")
    sys.exit()

# ===================== ENVIO =====================
for numero in contatos:
    try:
        print(f"\nEnviando para {numero}...")

        # Barra de busca (XPath estável 2025)
        campo_busca = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
        ))
        campo_busca.click()
        campo_busca.send_keys(Keys.COMMAND + "a")  # Mac = COMMAND
        campo_busca.send_keys(Keys.DELETE)
        campo_busca.send_keys(numero)
        time.sleep(2)

        # Abre o chat
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@data-icon='default-user']/../..")
        )).click()
        time.sleep(3)

        # Caixa de mensagem
        caixa_msg = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        ))

        # Envia com quebras de linha
        for linha in mensagem.split("\n"):
            caixa_msg.send_keys(linha)
            caixa_msg.send_keys(Keys.SHIFT + Keys.ENTER)
        caixa_msg.send_keys(Keys.ENTER)

        print(f"Enviado com sucesso para {numero}")
        time.sleep(2)

    except Exception as e:
        print(f"Falha com {numero}: {e}")

print("\nTODAS AS MENSAGENS ENVIADAS!")
input("Pressione ENTER para fechar...")
driver.quit()