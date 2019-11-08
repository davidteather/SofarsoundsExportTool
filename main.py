from selenium import webdriver
import time
import csv
import json
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

with open('settings.json', 'r') as rawjson:
    settings = json.load(rawjson)
    email = settings['email']
    password = settings['pass']

driver.get("https://www.sofarsounds.com/events/28467/print")
time.sleep(1)
driver.find_element_by_xpath('//input[@id="user_email"]').send_keys(email)
driver.find_element_by_xpath("//input[@id='user_password']").send_keys(password)
driver.find_element_by_id("gtm_auth_sign_in_page").click()
time.sleep(3)

driver.get("https://www.sofarsounds.com/london/events")
time.sleep(1)
events = driver.find_elements_by_xpath("//div[@class='events-row row']/div[@class='col-xs-12 col-sm-6 col-md-6']")

prevEmails = []

with open("editors.csv", 'w') as f:
    time.sleep(0.01)

eventID = []
for event in events:
    eventID.append(event.get_attribute('id').replace("event_", ""))

for event in eventID:
    driver.get("https://www.sofarsounds.com/events/" + event + "/print")
    time.sleep(1)
    tableT = driver.find_elements_by_xpath("//table[@class='table table-bordered print-friendly-guestlist-table']")[0]

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.findAll("table", {"class":"table table-bordered print-friendly-guestlist-table"})[0]
    rows = table.findAll("tr")
    
    with open("editors.csv", "a") as f:
        for row in rows:
            lines = row.text.strip().splitlines()
            line = lines[0]
            if "@" in line:
                if line not in prevEmails:
                    prevEmails.append(line)
                    f.write(line + "\n")

driver.quit()