from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless")  # opcional
driver = webdriver.Chrome(options=options)

driver.get("https://www.decolar.com/passagens-aereas/")
time.sleep(5)  # espera o JS carregar

html = driver.page_source

print(html[:2000])

driver.quit()
