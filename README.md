© **VictoriaSCorreia**

❗ Under code maintenance

# 🔎 JobScraper – Automated Job Search and Alert Scraper  

JobScraper is a Python-based scraper using Selenium to automatically search and collect job opportunities from platforms like **InfoJobs** and **Gupy**. The goal is to simplify job searching by:  

- **Organizing the collected data into a CSV file for further analysis**  
- **Sending the recent job opportunities directly via Telegram**  

## 🚀 Features  

✅ **Automatic job collection** with title, posting date, and direct application link.  
✅ **Support for multiple job sites**, easily configurable via CSS selectors.  
✅ **Job filtering** based on the posting date (e.g., recent jobs only).  
✅ **Auto-scrolling** to load all available job postings.  
✅ **CSV storage** for easy data access and analysis.  
✅ **Auto-sending data** to a chat.  

## 🛠️ Technologies Used  

- Python  
- Selenium  
- Pandas  
- WebDriver Manager  
- Logging  
- Telegram Bot 

## ⚙️ How to Use  

### 1️⃣ Install dependencies  
Run:  

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes all necessary dependencies:  
- Selenium  
- WebDriver Manager  
- Pandas  
- Python Telegram Bot

#### 🌐 Browser Requirements
To run JobScraper, **Google Chrome must be installed** as it uses ChromeDriver for Selenium. If you prefer, you can switch to Firefox by using GeckoDriver or any other browser driver.

Headless mode is supported by uncommenting the options.add_argument("--headless") line.

### 2️⃣ 

### 3️⃣ Configure the recipient  
Modify the **RECIPIENT_ID** variable in the `jobsAlert.py` file to specify the contact or group where job alerts should be sent.  

### 4️⃣ Run the scripts  

```bash
python jobsAlert.py
python jobsList_byDate.py
```

### 🖥️ Adding New Job Sites  

You can add new job positions by modifying the "job_types" variable. 
You can add new job sites by modifying the domains list in the code. Simply define the URL and the correct CSS selectors for the job elements (title, date, and link). Note that if the site uses pagination, there is no handling for it—you would need to manually handle pagination if required.

### 🚨 Manual Usage and Task Scheduling
When using jobsAlert, there is the option to run the software manually through the terminal. However, it was designed to be integrated with a task scheduler. The "script" file is what should be referenced when creating the scheduled task action, change it based on what is written

