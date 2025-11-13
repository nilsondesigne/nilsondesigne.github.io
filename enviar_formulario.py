import os
import zipfile
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import platform
import re

# --- Função para pegar a versão do Chrome ---
def get_chrome_version():
    system = platform.system()
    if system == "Windows":
        import winreg
        path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except FileNotFoundError:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
        version, _ = winreg.QueryValueEx(key, "")
        result = subprocess.run([version, "--version"], capture_output=True, text=True)
        return result.stdout.strip().split()[2]  # pega só o número
    else:
        # Linux / MacOS
        result = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
        return result.stdout.strip().split()[2]

# --- Função para baixar o ChromeDriver compatível ---
def download_chromedriver(version):
    major_version = version.split(".")[0]
    url_version = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}").text.strip()
    system = platform.system()
    if system == "Windows":
        url = f"https://chromedriver.storage.googleapis.com/{url_version}/chromedriver_win32.zip"
    elif system == "Linux":
        url = f"https://chromedriver.storage.googleapis.com/{url_version}/chromedriver_linux64.zip"
    else:
        url = f"https://chromedriver.storage.googleapis.com/{url_version}/chromedriver_mac64.zip"

    print(f"Baixando ChromeDriver versão {url_version}...")
    r = requests.get(url)
    zip_path = "chromedriver.zip"
    with open(zip_path, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")
    os.remove(zip_path)
    print("ChromeDriver pronto.")

# --- Detectar Chrome e baixar driver ---
chrome_version = get_chrome_version()
download_chromedriver(chrome_version)

# --- Caminhos do usuário ---
nome = input("Digite seu nome: ")
email = input("Digite seu email: ")
arquivo = input("Digite o caminho completo do arquivo para upload: ")

if not os.path.exists(arquivo):
    print("Arquivo não encontrado! Verifique o caminho e tente novamente.")
    exit()

# --- Inicializar Selenium ---
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfEFuYOS10FEKIrAcRRQTor--oWZQDncYkpF17iC_0voS2kzg/viewform")

    time.sleep(3)  # esperar página carregar

    # Preencher campos (ajuste os seletores conforme o formulário)
    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(nome)
    driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(email)
    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(arquivo)

    time.sleep(2)
    driver.find_element(By.XPATH, '//span[text()="Enviar"]/ancestor::button').click()

    print("Formulário enviado com sucesso!")

finally:
    time.sleep(3)
    driver.quit()
