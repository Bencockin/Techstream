from bs4 import BeautifulSoup as soup
from selenium import webdriver
import numpy as np
import time
from random import randint
import requests


# Creates a header to make sure that websites can be accessed ("Robot Check")
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'}

def pnet_scrape(): 
    
	url = "https://www.pnet.co.za/5/job-search-detailed.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=[]&cityid=0&ke=%22C%23.NET%22%20OR%20C%23&ws=Cape%20Town&radius=30&suid=b4d81819-aa55-4e28-b307-2ee4e55e711f&of="
	
	for page in range(0,400,25):
        
		response = requests.get(url + str(page), headers=headers)
		page_soup = soup(response.text,"html.parser")
		containers = page_soup.findAll('article' , {'data-at':'job-item'})

		# Find all data needed
		for container in containers:

		    # Scrapes the job title       
		    job = container.h2.text

		    # Scrapes the comapany name
		    company = container.find('div' , {'data-at':'job-item-company-name'}).text

		    # Scrapes the location of the company
		    location = container.find('li', {'data-at':'job-item-location'}).text.strip()

		    # Extracts HTML link to advert
		    link_extract = container.find('a',{'data-at': 'job-item-title'}).get('href')
		    link =('https://www.stepstone.de'+link_extract)
		    
		    date_posted = date_posted = container.find('time').text
		    
		    #f.write(date_posted.replace(","," ") + "," + company.replace(",", " ") + "," + job.replace(",", " ") + "," + location.replace(",", " | ") + "," + link + "\n")

		    # Not needed but gives an indication that the programme is still running / scraping
		    print('PNet ', company)
		    

		# Randomly pauses between 2 - 10 seconds (Help avoid "Robot Check")
		time.sleep(randint(2,10))

# Creates File(csv) to store scraped data
#filename = "Job_Board_PNet.csv"
#f = open(filename, "w")
#header = "Date Posted, Company , Job, Location, Link \n"
#f.write(header)

pnet_scrape()

#f.close()