from JobScraper import JobScraper
from datetime import datetime, timedelta
import pyautogui
import os
import time

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
        "url": "https://www.infojobs.com.br/empregos.aspx?palabra=desenvolvedor+jr",
        "selectors": {
        "job": '[class*="js_rowCard"]',
        "title": '[class*="h3 font-weight-bold text-body mb-8"]',
        "date": '[class*="text-medium small"]',
        "link": '[class*="py-16 pl-24 pr-16 cursor-pointer js_vacancyLoad js_cardLink"]'
        }
    }
]

def scraperJobsDict(dateRegulator, dateRegulatorType):
    all_jobs = {"title": [], "date": [], "link": []}
    for domain in domains:
        scraper = JobScraper(domain['url'], domain['selectors'], dateRegulator, dateRegulatorType)
        try:
            jobs_per_domain = scraper.scrape()
            all_jobs["title"].extend(jobs_per_domain["title"])
            all_jobs["date"].extend(jobs_per_domain["date"])
            all_jobs["link"].extend(jobs_per_domain["link"])
        finally:
            scraper.driver.quit()
    print("Varredura de dados concluída! ✅")
    return all_jobs

def createMessage(jobs):
    message = "NOVAS VAGAS:\n\n"
    if not jobs["title"]:
        message = "Nenhuma vaga encontrada nas últimas 24 horas."
    else:
        for i in range(len(jobs["title"])):
            message += f"{jobs['title'][i]} ({jobs['date'][i]})\n> {jobs['link'][i]}\n\n"
    return message

# Must be logged in on WhatsApp Desktop
def findContact(recipient):
    try:
        cmd = 'start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App'
        os.system(cmd)
        time.sleep(7)
    except:
        print("Não foi possível abrir o app")

    pyautogui.hotkey('ctrl', 'f')  # Opens search bar
    time.sleep(1)
    pyautogui.write(recipient)
    time.sleep(5)
    pyautogui.press('down') # Goes to the first contact
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(1)
    
def sendMessage(message):
    jobsNum = 0
    for line in message.split("\n"):
        pyautogui.write(line)
        if "https://" in line:
            jobsNum += 1
            if jobsNum == 10: # to avoid exceeding the character limit
                jobsNum = 0
                pyautogui.press('enter')
                continue
        time.sleep(1)
        pyautogui.hotkey('shift', 'enter') # skip a line
    pyautogui.press('enter')
    print("Mensagem enviada com sucesso! ✅")

yesterday = datetime.now().date() - timedelta(days=1)
# Constant variable
dateRegulatorType = 'alert'

jobs = scraperJobsDict(yesterday, dateRegulatorType)
message = createMessage(jobs)
recipient = "" # * contact or group to send the messages

findContact(recipient)
sendMessage(message)
