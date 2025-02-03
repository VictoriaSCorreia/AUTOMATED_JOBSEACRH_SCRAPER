from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

def scrape_vagas(url, seletores, data_limite):
    # Inicializa o navegador
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    dic_vagas = {"titulo": [], "data": [], "link": []}

    last_height = driver.execute_script("return document.body.scrollHeight")

    # Configuração de rolagem para carregamento infinito
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    """ time.sleep(5) """
    # Coletando as vagas
    vagas = driver.find_elements(By.CSS_SELECTOR, seletores['vaga'])

    for vaga in vagas:
        try:
            data_texto = vaga.find_element(By.CSS_SELECTOR, seletores['data']).get_attribute("textContent").strip()
            data = data_texto.split(": ")[-1]
            try:
                # Tenta converter data no formato "dd/mm/yyyy"
                data_vaga = datetime.strptime(data, "%d/%m/%Y").date()
            except ValueError:
                data_vaga = converter_data(data_texto)

            if data_vaga > data_limite:
                titulo = vaga.find_element(By.CSS_SELECTOR, seletores['titulo']).get_attribute("textContent").strip()
                link_element = vaga.find_element(By.CSS_SELECTOR, seletores['link'])
                link = link_element.get_attribute("href") or link_element.get_attribute("data-href") or "Sem link"
                
                print(titulo, data_vaga, link)

                dic_vagas["titulo"].append(titulo)
                dic_vagas["data"].append(data_vaga.strftime("%d/%m/%Y"))  # Padroniza a saída
                dic_vagas["link"].append(link)
        except Exception as e:
            print(f"Erro ao processar vaga: {e}")
            continue 

    driver.quit()
    return dic_vagas

def converter_data(data_str):
    partes = data_str.split()
    if len(partes) < 2:
        raise ValueError(f"Formato de data inesperado: {data_str}")

    dia, mes_abrev = partes[0], partes[1].lower()
    mes = meses_pt.get(mes_abrev)

    if not mes:
        raise ValueError(f"Mês não reconhecido: {mes_abrev}")

    # Se o mês for maior que o mês atual, assume que a vaga foi postada no ano passado [melhorar]
    ano_atual = datetime.now().year
    if int(mes) > datetime.now().month:
        ano_atual -= 1

    data_formatada = f"{dia}/{mes}/{ano_atual}"
    return datetime.strptime(data_formatada, "%d/%m/%Y").date()

meses_pt = {
    "jan": "01", "fev": "02", "mar": "03", "abr": "04",
    "mai": "05", "jun": "06", "jul": "07", "ago": "08",
    "set": "09", "out": "10", "nov": "11", "dez": "12"
}

# Lista de domínios e suas configurações de scraping
dominios = [
    {
        "url": "https://portal.gupy.io/job-search/term=desenvolvedor%20junior&workplaceTypes[]=remote",
        "seletores": {
            "vaga": '[class*="kokxPe"]',
            "titulo": '[class*="dZRYPZ"]',
            "data": '[class*="iUzUdL"]',
            "link": '[class*="IKqnq"]'
        }
    },
    {
        "url": "https://www.infojobs.com.br/vagas-de-emprego-desenvolvedor+junior-trabalho-home-office.aspx",
        "seletores": {
            "vaga": '[class*="js_rowCard"]',
            "titulo": '[class*="h3 font-weight-bold text-body mb-8"]',
            "data": '[class*="text-medium small"]',
            "link": '[class*="py-16 pl-24 pr-16 cursor-pointer js_vacancyLoad js_cardLink"]'
        }
    }
]

# Define a partir de que data as vagas devem ser armazenadas
data_limite = datetime(2025, 1, 1).date()

# Dicionário para armazenar as vagas de todos os domínios
all_vagas = {"titulo": [], "data": [], "link": []}

# Scraping para cada domínio
for dominio in dominios:
    print(f"Iniciando scraping para: {dominio['url']}")
    vagas_dominio = scrape_vagas(dominio['url'], dominio['seletores'], data_limite)
    
    # Adiciona as vagas coletadas ao dicionário geral
    all_vagas["titulo"].extend(vagas_dominio["titulo"])
    all_vagas["data"].extend(vagas_dominio["data"])
    all_vagas["link"].extend(vagas_dominio["link"])

# Salvando os dados em CSV
df = pd.DataFrame(all_vagas)
df.to_csv("vagas_coletadas.csv", encoding="utf-8", sep=";", index=False)

print("Scraping concluído e arquivo salvo com sucesso! ✅")
