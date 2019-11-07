from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

driver.get("https://www.sofarsounds.com/events/28467/print")
time.sleep(1)
driver.find_element_by_xpath('//input[@id="user_email"]').send_keys("yonndoh@gmail.com")
driver.find_element_by_xpath("//input[@id='user_password']").send_keys("helpineedhelp")
driver.find_element_by_id("gtm_auth_sign_in_page").click()
time.sleep(3)

returnString = "Guest, Additional Guests"

tableT = driver.find_elements_by_xpath("//table[@class='table table-bordered print-friendly-guestlist-table']")[0]

soup = BeautifulSoup(driver.page_source, "html.parser")
table = soup.findAll("table", {"class":"table table-bordered print-friendly-guestlist-table"})[0]
rows = table.findAll("tr")

with open("editors.csv", "w+") as f:
    f.write("Guest,Additional Guests\n")
    for row in rows:
        lines = row.text.strip().splitlines()

        line = lines[0]
        if "@" in line:
            try:
                lines[3]
                f.write(line + "," + lines[3].replace("+", "") + "\n")
            except:
                f.write(line + ",0\n")

driver.quit()