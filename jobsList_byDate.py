from JobScraper import JobScraper
from datetime import datetime
import logging
import pandas as pd

domains = [
    {
        "url": "https://portal.gupy.io/job-search/term=desenvolvedor%20python",
        "selectors": {
            "job": '[class*="kokxPe"]',
            "title": '[class*="dZRYPZ"]',
            "date": '[class*="iUzUdL"]',
            "link": '[class*="IKqnq"]'
        }
    },
    {
        "url": "https://www.infojobs.com.br/empregos.aspx?palabra=desenvolvedor+jr",
        "selectors": {
        "job": '[class*="js_rowCard"]',
        "title": '[class*="h3 font-weight-bold text-body mb-8"]',
        "date": '[class*="text-medium small"]',
        "link": '[class*="py-16 pl-24 pr-16 cursor-pointer js_vacancyLoad js_cardLink"]'
        }
    }
]

# Choose a limit day
while True:
    try:
        limit_date = input("A partir de qual data devem ser as vagas? (formato: ano-mês-dia): ")
        limit_date = datetime.strptime(limit_date, "%Y-%m-%d").date()
        break
    except ValueError:
        print("Data inválida. Tente novamente.")

# limit_date = datetime(2025, 1, 1).date()
# Constant variable
dateRegulatorType = 'jobs list'
all_jobs = {"title": [], "date": [], "link": []}

for domain in domains:
    scraper = JobScraper(domain['url'], domain['selectors'], limit_date, dateRegulatorType)
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
