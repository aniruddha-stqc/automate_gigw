import datetime
import os
import time
import re
import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service


import globals


def execute():
    script_name = os.path.basename(__file__)
    print(script_name + " : " + "Launching Color Contrast Accessibility Validator in Selenium Gecko Browser headlessly")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,
                               executable_path=globals.gecko_path,
                               service_log_path=os.devnull)
    driver.get("https://color.a11y.com/Contrast/")

    driver.find_element("id", "urltotest").clear()
    driver.find_element("id", "urltotest").send_keys(globals.target_website)
    driver.find_element("id", "submitbuttontext").click()

    print(script_name + " : " + "Scanning target website " + globals.target_website + " for Color Contrast issues")

    time.sleep(globals.time_wait)
    page_source = driver.page_source
    # Close the webdriver
    driver.close()
    # Selenium hands over the page source to Beautiful Soup for WebScraping

    print(script_name + " : " + "Parsing scan results using Beautiful Soup")
    page_soup = BeautifulSoup(page_source, "html.parser")
    if re.search("Congratulations!", page_soup.text):
        print(script_name + " : " + "Congratulations! No issues found" )
    if re.search("We had trouble getting content from web page URL", page_soup.text):
        print(script_name + " : " + "We had trouble getting content from web page URL")
    if re.search("Problems Detected!", page_soup.text):
        print(script_name + " : " + "Parsing Color Contrast problems")
        results = page_soup.find("table", {"id": "resultstable"})
        contrast_problems = results.tbody.find_all("tr")

        globals.test_log = "logs/test_log_contrast.xlsx"
        workbook = xlsxwriter.Workbook(globals.test_log)
        worksheet = workbook.add_worksheet("contrast_issues")
        excel_row = 0
        worksheet.write(excel_row, 0, "background_color")
        worksheet.write(excel_row, 1, "text_color")
        worksheet.write(excel_row, 2, "content_text")
        worksheet.write(excel_row, 3, "current_ratio")
        worksheet.write(excel_row, 4, "fix_remarks")

        for problem in contrast_problems:
            excel_row += 1
            column_bgcolor = problem.find("div", {"class": "smalltext"})
            column_content = problem.find("textarea")
            column_textcolor = problem.td.findNext('td').find("div", {"class": "smalltext"})
            column_remarks = problem.find("div", {"style": "margin-top:1rem;"})
            column_ratio = problem.td.findNext('td').findNext('td').findNext('td').findNext('td').div.div.findNext(
                "div").find(
                "span", {"class": "inblock fright"})
            worksheet.write(excel_row, 0, column_bgcolor.text)
            worksheet.write(excel_row, 1, column_textcolor.text)
            worksheet.write(excel_row, 2, column_content.text.strip())
            worksheet.write(excel_row, 3, column_ratio.text)
            worksheet.write(excel_row, 4, column_remarks.text)

        print(script_name + " : " + "Color Contrast issue count " + str(excel_row))
        workbook.close()
        print(script_name + " : " + "All results written to file " + globals.test_log)




if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    execute()
    print(script_name + " : " + "Finished in " + str(
        (datetime.datetime.now() - globals.time_start).total_seconds()) + " seconds")
