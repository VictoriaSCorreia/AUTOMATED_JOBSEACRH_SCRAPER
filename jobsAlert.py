import asyncio
from telegram import Bot
from JobScraper import JobScraper
from datetime import datetime, timedelta

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

def scraperJobsDict(dateRegulator, DATE_REGULATOR_TYPE, job_types, remote, domains):
    all_jobs = {"title": [], "date": [], "link": []}
    for job_type in job_types:
        for domain in domains:
            # URL format
            formatted_keywords = domain["join_char"].join(job_type.split())
            search_url = domain["base_url"].format(formatted_keywords, domain["remote_format"] if remote else "")

            scraper = JobScraper(search_url, domain['selectors'], dateRegulator, DATE_REGULATOR_TYPE)
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

DATE_REGULATOR_TYPE = 'alert'
BOT_TOKEN = ""
RECIPIENT_ID = ""

# jobs to search
job_types = ["desenvolvedor java"]
remote = True
# to catch yesterday jobs
yesterday = datetime.now().date() - timedelta(days=1)

jobs = scraperJobsDict(yesterday, DATE_REGULATOR_TYPE, job_types, remote, domains) # * will be improved
message = createMessage(jobs)

bot = Bot(BOT_TOKEN)
try:
    asyncio.run(bot.send_message(chat_id=RECIPIENT_ID, text=message))
    print("Mensagem enviada com sucesso! ✅")
except:
    print("Não foi possível enviar a mensagem, verifique o id do chat.")
