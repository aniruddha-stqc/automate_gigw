from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import xlsxwriter
import globals
import time
import datetime
import os, sys

script_name = os.path.basename(sys.argv[0])
print(script_name + " : " + "Launching Color Contrast Accessibility Validator in Selenium Gecko Browser headlessly")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=globals.gecko_path)
driver.get("https://color.a11y.com/Contrast/")

driver.find_element_by_id("urltotest").clear()
driver.find_element_by_id("urltotest").send_keys(globals.target_website)
driver.find_element_by_id("submitbuttontext").click()

print(script_name + " : " + "Scanning target website "+ globals.target_website + " for Color Contrast issues")

time.sleep(globals.time_wait)
page_source = driver.page_source
#Close the webdriver
driver.close()
#Selenium hands over the page source to Beautiful Soup for WebScraping

print(script_name + " : " + "Parsing scan results using Beautiful Soup")
page_soup = BeautifulSoup(page_source, "html.parser")

print(script_name + " : " + "Parsing Color Contrast problems")
results = page_soup.find("table",{"id":"resultstable"})
contrast_problems = results.find_all("tr")
for problem in contrast_problems:
    print(problem.text)
