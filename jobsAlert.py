from datetime import datetime, timedelta

import logging
import os
import pandas as pd
from JobScraper import JobScraper

domains = [
   {
        "url": "https://portal.gupy.io/job-search/term=desenvolvedor%20jr",
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

logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
yesterday = datetime.now().date() - timedelta(days=1)
all_jobs = {"title": [], "date": [], "link": []}

for domain in domains:
    scraper = JobScraper(domain['url'], domain['selectors'], yesterday)
    try:
        jobs_per_domain = scraper.scrape()
        all_jobs["title"].extend(jobs_per_domain["title"])
        all_jobs["date"].extend(jobs_per_domain["date"])
        all_jobs["link"].extend(jobs_per_domain["link"])
    finally:
        scraper.driver.quit()

# Saving in csv
arquivo = "vagas_novas.csv"
if os.path.exists(arquivo):
    os.remove(arquivo)
    
df = pd.DataFrame(all_jobs)
df.to_csv("vagas_novas.csv", encoding="utf-8", sep=";", index=False)
logging.info("Scraping concluído e arquivo salvo com sucesso! ✅")