from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
from datetime import datetime

class JobScraper:
    def __init__(self, url, selectors, dateRegulator, DATE_REGULATOR_TYPE):
        """
        Parameters:
        - url (str): URL of the job page
        - selectors (dict): Dictionary containing the CSS selectors for the page elements
        - dateRegulator (datetime.date): The kind of regulator (limit_date or yesterday)
        """
        self.url = url
        self.selectors = selectors 
        self.dateRegulator = dateRegulator
        self.DATE_REGULATOR_TYPE = DATE_REGULATOR_TYPE
        self.driver = self._setup_driver()

    def _setup_driver(self):
        # Chrome driver config to execute Selenium
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Execute without opening Chrome
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox") # Linux config
        options.add_argument("--disable-dev-shm-usage") # Linux config
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
        
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def _scroll_page(self):
        # Scrolling the whole page to load the data (jobs)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5) # * It has to be improved
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
        - datetime.date: Date formatted in the dd-mm-yyyy format.
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

        formatted_date = f"{day}-{month}-{current_year}"
        return datetime.strptime(formatted_date, "%d-%m-%Y").date()

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
            jobs = self.driver.find_elements(By.XPATH, self.selectors["job"])
        except Exception as e:
            logging.error(f"Erro ao encontrar vagas em {self.url}: {e}")
            return job_dict

        for job in jobs:
            try:
                text_date = job.find_element(By.XPATH, self.selectors['date']).get_attribute("textContent").strip() 
                date = text_date.split(": ")[-1]
                try:
                    job_date = datetime.strptime(date, "%d/%m/%Y").date()
                except ValueError:
                    # For infojobs date format
                    if text_date == "Ontem" or text_date == "Hoje":
                        job_date = text_date
                    else:
                        job_date = self._convert_date(text_date)

                element_link = job.find_element(By.XPATH, self.selectors['link'])
                link = element_link.get_attribute("href") or f"https://www.infojobs.com.br/{element_link.get_attribute('data-href')}" or "Sem link"
                if self.DATE_REGULATOR_TYPE == 'jobs list':
                    if job_date != "Hoje" and job_date != "Ontem" and job_date < self.dateRegulator:
                        continue
                elif self.DATE_REGULATOR_TYPE == 'alert':
                    if job_date != "Ontem" and job_date != self.dateRegulator:
                        continue
                else:
                    raise Exception()
                
                title = job.find_element(By.XPATH, self.selectors['title']).get_attribute("textContent").strip()
                job_dict["title"].append(title)
                job_dict["date"].append(job_date)
                job_dict["link"].append(link)
            except Exception as e:
                continue 
        return job_dict
        