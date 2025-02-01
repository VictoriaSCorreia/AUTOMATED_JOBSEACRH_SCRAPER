from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

# Define um user-agent customizado para evitar ser bloqueado por sistemas de anti-bot
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"

# Inicializa as opções do Chrome
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")  # Se descomentado, roda o navegador em modo headless (sem interface gráfica), mas pode contribuir para um bloqueio
options.add_argument("--disable-gpu")  # Desabilita o uso de GPU, útil quando em modo headless

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL da página acessada
url = "https://portal.gupy.io/job-search/term=desenvolvedor%20junior"
driver.get(url)

dic_vagas = {"titulo": [], "data": [], "link": []}

# Define a partir de que data a vaga deve ser armazenada
data_limite = datetime(2025, 1, 1) 

# Configuração de rolagem de uma página com carregamento infinito
# Altura inicial para controlar o momento em que chegou ao final da rolagem
last_height = driver.execute_script("return document.body.scrollHeight")

# Laço para carregar todas as vagas
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Rola até o final da página
    time.sleep(3)  # Espera 5s para novos vagas carregarem
    
    # Verifica a altura da página novamente após a rolagem
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # Se a altura não mudou, significa que a página chegou ao fim
        break
    last_height = new_height  # Atualiza a altura para a próxima verificação

# Coletando os vagas após o carregamento completo
vagas = driver.find_elements(By.CSS_SELECTOR, '[class*="kokxPe"]')

for vaga in vagas:
    try:
        # Extraindo as informações de cada vaga
        data_texto = vaga.find_element(By.CSS_SELECTOR, '[class*="iUzUdL"]').text.strip()
        data = data_texto.split(": ")[-1]
        # Vagas apenas após a data estipulada
        data_vaga = datetime.strptime(data, "%d/%m/%Y")  
        if data_vaga > data_limite:
            titulo = vaga.find_element(By.CSS_SELECTOR, '[class*="dZRYPZ"]').text.strip()
            link_element = vaga.find_element(By.CSS_SELECTOR, '[class*="IKqnq"]')
            link = link_element.get_attribute("href") if link_element else "Sem link"

            print(titulo, data, link)

            # Adiciona as informações ao dicionário
            dic_vagas["titulo"].append(titulo)
            dic_vagas["data"].append(data)
            dic_vagas["link"].append(link)
    except Exception as e:
            print(f"Erro ao processar vaga: {e}")  
            continue

# Fechando o navegador
driver.quit()

# Salvando os dados em CSV
df = pd.DataFrame(dic_vagas)
df.to_csv("vagas_gupy.csv", encoding="utf-8", sep=";", index=False)

print("Scraping concluído e arquivo salvo com sucesso! ✅")