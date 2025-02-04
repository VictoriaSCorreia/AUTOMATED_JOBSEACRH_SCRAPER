import logging
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JobScraper:
    def __init__(self, url, selectors, limit_date):
        """
        Class responsible for performing job scraping.

        Parameters:
        - url (str): URL of the job page
        - selectors (dict): Dictionary containing the CSS selectors for the page elements
        - limit_date (datetime.date): The limit date for considering the jobs
        """
        self.url = url
        self.selectors = selectors 
        self.limit_date = limit_date  
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Chrome driver config to execute Selenium"""
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Executa sem abrir o navegador
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox") # Linux config
        options.add_argument("--disable-dev-shm-usage") # Linux config
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
        
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def _scroll_page(self):
        """Scrolling the whole page to load the data (jobs)"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) # It has to be improved
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _convert_date(self, date_str):
        """
        Converts a date in textual format to a datetime.date object.

        Parameter:
        - date_str (str): Date extracted from the page in textual format.

        Return:
        - datetime.date: Date formatted in the dd/mm/yyyy format.
        """
        months_pt = {
            "jan": "01", "fev": "02", "mar": "03", "abr": "04",
            "mai": "05", "jun": "06", "jul": "07", "ago": "08",
            "set": "09", "out": "10", "nov": "11", "dez": "12"
        }
        parts = date_str.split()
        if len(parts) < 2:
            raise ValueError(f"Formato de data inesperado: {date_str}")

        day, month_abbr = parts[0], parts[1].lower()
        month = months_pt.get(month_abbr)
        if not month:
            raise ValueError(f"Mês não reconhecido: {month_abbr}")

        # If the month is greater than the current month, it assumes that the job was posted last year [improvement needed].
        current_year = datetime.now().year
        if int(month) > datetime.now().month:
            current_year -= 1

        formatted_date = f"{day}/{month}/{current_year}"
        return datetime.strptime(formatted_date, "%d/%m/%Y").date()

    def scrape(self):
        """
        Performs the scraping of the page and returns a dictionary with the collected data.

        Return:
        - dict: Dictionary containing the titles, dates, and links of the jobs.
        """
        logging.info(f"Iniciando scraping: {self.url}")
        self.driver.get(self.url)
        self._scroll_page()

        job_dict = {"title": [], "date": [], "link": []}
        try:
            jobs = self.driver.find_elements(By.CSS_SELECTOR, self.selectors["job"])
        except Exception as e:
            logging.error(f"Erro ao encontrar vagas em {self.url}: {e}")
            return job_dict

        for job in jobs:
            try:
                text_date = job.find_element(By.CSS_SELECTOR, self.selectors['date']).get_attribute("textContent").strip() 
                date = text_date.split(": ")[-1]
                try:
                    job_date = datetime.strptime(date, "%d/%m/%Y").date()
                except ValueError:
                    # For infojobs date format
                    job_date = self._convert_date(text_date)
                
                if job_date >= self.limit_date:
                    title = job.find_element(By.CSS_SELECTOR, self.selectors['title']).get_attribute("textContent").strip()
                    element_link = job.find_element(By.CSS_SELECTOR, self.selectors['link'])
                    link = element_link.get_attribute("href") or f"https://www.infojobs.com.br/{element_link.get_attribute('data-href')}" or "Sem link"

                    print(title, job_date, link)

                    job_dict["title"].append(title)
                    job_dict["date"].append(job_date.strftime("%d/%m/%Y"))
                    job_dict["link"].append(link)
            except Exception as e:
                continue 
        return job_dict

# Pages
domains = [
    {
        "url": "https://portal.gupy.io/job-search/term=desenvolvedor&workplaceTypes[]=remote",
        "selectors": {
            "job": '[class*="kokxPe"]',
            "title": '[class*="dZRYPZ"]',
            "date": '[class*="iUzUdL"]',
            "link": '[class*="IKqnq"]'
        }
    },
    {
        "url": "https://www.infojobs.com.br/vagas-de-emprego-desenvolvedor+junior-trabalho-home-office.aspx",
        "selectors": {
            "job": '[class*="js_rowCard"]',
            "title": '[class*="h3 font-weight-bold text-body mb-8"]',
            "date": '[class*="text-medium small"]',
            "link": '[class*="py-16 pl-24 pr-16 cursor-pointer js_vacancyLoad js_cardLink"]'
        }
    }
]

limit_date = datetime(2025, 1, 1).date()
all_jobs = {"title": [], "date": [], "link": []}

for domain in domains:
    scraper = JobScraper(domain['url'], domain['selectors'], limit_date)
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
