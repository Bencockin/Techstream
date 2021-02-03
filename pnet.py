from selenium import webdriver
from bs4 import BeautifulSoup as soup
import time
from random import randint
import requests
import smtplib
from email.message import EmailMessage

# Creates File(csv) to store scraped data
filename = "capetown_pnet.csv"
f = open(filename, "w")
header = "Date Posted, Company , Job, Location, Link \n"
f.write(header)

# Webdriver Set Up
DRIVER_PATH = '/PathToWebdriver/webdriver' #This is the local path to the webdriver that will grab the site

driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# Go to webpage
url = "https://www.pnet.co.za/5/job-search-detailed.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=[]&cityid=0&ke=%22C%23.NET%22%20OR%20C%23&ws=Cape%20Town&radius=30&suid=b4d81819-aa55-4e28-b307-2ee4e55e711f&of="

for page in range(0,150,25):

    driver.get(url + str(page))

    time.sleep(3)

    html = driver.page_source

    page_soup = soup(html,"html.parser")

    containers = page_soup.findAll('article' , {'data-at' : 'job-item'})

        # Find all data needed
    for container in containers:

        # Scrapes the job title       
        job = container.h2.text

        # Scrapes the company name
        company = container.find('div' , {'data-at':'job-item-company-name'}).text

        # Scrapes the location of the company
        location = container.find('li', {'data-at':'job-item-location'}).text.strip()

        # Extracts HTML link to advert
        link_extract = container.find('a',{'data-at': 'job-item-title'}).get('href')
        link =('https://www.pnet.co.za'+link_extract)

        date = container.find('time').text

        f.write(date.replace(","," ") + "," + company.replace(",", " ") + "," + job.replace(",", " ") + "," + location.replace(",", " | ") + "," + link + "\n")

        print(f"{date}, {company}, {job}, {location}")
        print(f"{link}")

driver.close()
f.close()


EMAIL_AD = 'python@email.com' #Enter the sending email address here
EMAIL_PW = '123456' #Enter Password here

msg = EmailMessage()
msg['Subject'] = '[Automated] PNet Job Board'
msg['From'] = EMAIL_AD
msg['To'] = 'email@email.com' #Enter the recieving email address(s) here
msg.set_content("This is an automated message. PLEASE DO NOT RESPOND. \n\nPlease speak to Ben directly for feedback")

with open('capetown_pnet.csv', 'rb') as f:
    file_data = f.read()

msg.add_attachment(file_data, maintype='application', subtype='csv', filename='capetown_pnet.csv')    

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_AD, EMAIL_PW)
    smtp.send_message(msg)
