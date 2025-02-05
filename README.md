By VictoriaSCorreia

# 🔎 JobScraper – Automated Job Search Scraper  

JobScraper is a Python-based scraper using Selenium to automatically search and collect job opportunities from platforms like **InfoJobs** and **Gupy**. The goal is to simplify job searching by organizing the collected data into a CSV file for further analysis.  

## 🚀 Features  

✅ **Automatic job collection** with title, posting date, and direct application link.  
✅ **Support for multiple job sites**, easily configurable via CSS selectors.  
✅ **Job filtering** based on the posting date (e.g., recent jobs only).  
✅ **Auto-scrolling** to load all available job postings.  
✅ **CSV storage** for easy data access and analysis.  

## 🛠️ Technologies Used  

- Python  
- Selenium  
- Pandas  
- WebDriver Manager  
- Logging  

## ⚙️ How to Use  

1. Install dependecies:  
   ```bash
   pip install -r requirements.txt
* selenium
* webdriver-manager
* pandas

2. Run:  
   ```bash
   python jobsAlert.py
   python jobsList_byDate.py

You can add new job sites by modifying the domains list in the code. Simply define the URL and the correct CSS selectors for the job elements (title, date, and link).
