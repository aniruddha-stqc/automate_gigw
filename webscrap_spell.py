from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import xlsxwriter
import globals
import time
import datetime
import os, sys


script_name = os.path.basename(sys.argv[0])
print(script_name + " : " + "Launching W3C Spell Checker in Selenium Gecko Browser headlessly")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options,executable_path= globals.gecko_path)

driver.get("https://www.w3.org/2002/01/spellchecker")
driver.find_element_by_name("uri").clear()
driver.find_element_by_name("uri").send_keys(globals.target_website)
driver.find_element_by_xpath( "(.//*[normalize-space(text()) and normalize-space(.)='Presents possible corrections:'])[1]/following::input[1]").click()

print(script_name + " : " + "Scanning target website " + globals.target_website + " for Spelling issues")
time.sleep(globals.time_wait)
page_source = driver.page_source
#Close the webdriver
driver.close()
#Selenium hands over the page source to Beautiful Soup for WebScraping
print(script_name + " : " + "Parsing scan results using Beautiful Soup")
page_soup = BeautifulSoup(page_source, "html.parser")
print(script_name + " : " + "Parsing Spelling issues")

#Parse the results section
results = page_soup.find("ol")
try:
    spell_issues = results.find_all("li")
except:
    spell_issues = []

workbook = xlsxwriter.Workbook(globals.test_log)
worksheet = workbook.add_worksheet("spell_checker")

excel_row = 0
worksheet.write(excel_row, 0, "spelling_issue")
for issue in spell_issues:
    excel_row += 1
    worksheet.write(excel_row, 0, issue.text.strip())

print(script_name + " : " + "Spelling issue count " + str (excel_row) )
workbook.close()

print(script_name + " : " + "All results written to file " + globals.test_log )
print(script_name + " : " + "Finished in " + str ( (datetime.datetime.now() - globals.time_start ).total_seconds() ) +" seconds")
