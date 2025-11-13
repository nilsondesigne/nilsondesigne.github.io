import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# --- DADOS DO USUÁRIO ---
nome = input("Digite seu nome: ")
email = input("Digite seu email: ")

# --- CONFIGURAÇÃO DE PASTA DE IMAGENS ---
pasta_imagens = "C:/site/imagens"

# Seleciona o último arquivo modificado na pasta
arquivos = [os.path.join(pasta_imagens, f) for f in os.listdir(pasta_imagens) 
            if os.path.isfile(os.path.join(pasta_imagens, f))]
if not arquivos:
    print("Não há arquivos na pasta de imagens!")
    exit()

arquivo = max(arquivos, key=os.path.getmtime)
print(f"Arquivo selecionado automaticamente: {arquivo}")

# --- INICIALIZAÇÃO DO SELENIUM ---
chromedriver_path = "C:/site/chromedriver.exe"  # Caminho do chromedriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

try:
    # Abre o formulário
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfEFuYOS10FEKIrAcRRQTor--oWZQDncYkpF17iC_0voS2kzg/viewform")
    time.sleep(3)  # espera a página carregar

    # --- PREENCHER FORMULÁRIO ---
    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(nome)
    driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(email)
    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(arquivo)

    time.sleep(2)
    driver.find_element(By.XPATH, '//span[text()="Enviar"]/ancestor::button').click()
    print("Formulário enviado com sucesso!")

finally:
    time.sleep(3)
    driver.quit()
