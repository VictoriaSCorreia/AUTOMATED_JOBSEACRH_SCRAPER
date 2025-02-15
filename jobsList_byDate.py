from JobScraper import JobScraper
from datetime import datetime
import logging
import pandas as pd

domains = [
    {
        "base_url": "https://www.infojobs.com.br/empregos.aspx?palabra={}{}",
        "join_char": "+",
        "remote_format": "-trabalho-home-office.aspx",
        "selectors": {
            "job": '//div[@data-href]', # * will be improved
            "title": './/h2[contains(@class, "mb-8")]',
            "date": './/div[contains(@class, "text-medium small")]',
            "link": '//div[@data-href]'
        }
    },
    {
        "base_url": "https://portal.gupy.io/job-search/term={}{}",
        "join_char": "%20",
        "remote_format": "&workplaceTypes[]=remote",
        "selectors": {
            "job": '//a[@href]', # * will be improved
            "title": './/h3[contains(@class, "dZRYPZ")]',
            "date": './/p[contains(@class, "iUzUdL")]',
            "link": '//a[@href]'
        }
    }
]

DATE_REGULATOR_TYPE = 'jobs list'

# jobs to search
job_types = ["desenvolvedor java"]
remote = True
# Choose a limit day
limit_date = datetime(2025, 1, 1).date()

all_jobs = {"title": [], "date": [], "link": []} # * will be improved
for job_type in job_types:
    for domain in domains:
        formatted_keywords = domain["join_char"].join(job_type.split())
        search_url = domain["base_url"].format(formatted_keywords, domain["remote_format"] if remote else "")

        scraper = JobScraper(search_url, domain['selectors'], limit_date, DATE_REGULATOR_TYPE)
        try:
            jobs_per_domain = scraper.scrape()
            all_jobs["title"].extend(jobs_per_domain["title"])
            all_jobs["date"].extend(jobs_per_domain["date"])
            all_jobs["link"].extend(jobs_per_domain["link"])
        finally:
            scraper.driver.quit()

# Saving in csv
df = pd.DataFrame(all_jobs)
df.to_csv("vagas_coletadas.csv", encoding="utf-8", sep=";", index=False)
logging.info("Scraping concluído e arquivo salvo com sucesso! ✅")

""" key_words = input("Tipo de vaga: ").split()

url_terms_infojobs = "+".join(key_words)
url_terms_gupy = "%20".join(key_words)

domains = [
    {
        "url": f"https://www.infojobs.com.br/empregos.aspx?palabra={url_terms_infojobs}",
        "selectors": {
            "job": '//div[@data-href]',  # Seleciona todos os cards de vagas
            "title": './/h2[contains(@class, "mb-8")]',  # Busca o título dentro do card
            "date": './/div[contains(@class, "text-medium small")]',  # Encontra a data da vaga
            "link": '//div[@data-href]'  # Captura o link da vaga
        }
    },
    {
        "url": f"https://portal.gupy.io/job-search/term={url_terms_gupy}",
        "selectors": {
            "job": '//a[@href]',
            "title": './/h3[contains(@class, "dZRYPZ")]',
            "date": './/p[contains(@class, "iUzUdL")]',
            "link": '//a[@href]'
        }
    }
] 
while True:
    try:
        limit_date = input("Vagas a partir de qual data? (formato: ano-mês-dia): ")
        limit_date = datetime.strptime(limit_date, "%Y-%m-%d").date()
        break
    except ValueError:
        print("Data inválida. Tente novamente.")
"""