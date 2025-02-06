© **VictoriaSCorreia**

# 🔎 JobScraper – Automated Job Search and Alert Scraper  

JobScraper is a Python-based scraper using Selenium to automatically search and collect job opportunities from platforms like **InfoJobs** and **Gupy**. The goal is to simplify job searching by:  

- **Organizing the collected data into a CSV file for further analysis**  
- **Sending the recent job opportunities directly via WhatsApp**  

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
- PyAutoGUI  

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
- PyAutoGUI  

### 2️⃣ Log in to WhatsApp Desktop  

### 3️⃣ Configure the recipient  
Modify the **recipient** variable in the `jobsAlert.py` file to specify the contact or group where job alerts should be sent.  

### 4️⃣ Run the scripts  

```bash
python jobsAlert.py
python jobsList_byDate.py
```

### 🖥️ Adding New Job Sites  
You can add new job sites by modifying the domains list in the code. Simply define the URL and the correct CSS selectors for the job elements (title, date, and link). Note that if the site uses pagination, there is no handling for it—you would need to manually handle pagination if required.


