import datetime
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import globals


def execute():
    script_name = os.path.basename(__file__)
    print(script_name + " : " + "Launching Link Checker in Selenium Gecko Browser headlessly")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=globals.gecko_path, service_log_path=os.devnull)

    driver.get("https://validator.w3.org/checklink?uri=")
    time.sleep(30)
    driver.find_element("id","uri_1").send_keys(globals.target_website)
    driver.find_element("name","check").click()

    print(script_name + " : " + "Scanning target website " + globals.target_website + " for Broken Links")
    #time.sleep(globals.time_wait)
    time.sleep(300)
    page_source = driver.page_source
    # Close the webdriver
    driver.close()
    # Selenium hands over the page source to Beautiful Soup for WebScraping
    print(script_name + " : " + "Parsing scan results using Beautiful Soup")
    page_soup = BeautifulSoup(open("logs/broken/links.html"), "html.parser")
    print(script_name + " : " + "Parsing Broken Links")

    print(page_soup.prettify)

    main = page_soup.body.find("div", {"id": "main"})
    report = main.find("dl", {"class": "report"})
    print(report.prettify)
    """
    # Parse the results section
    results = page_soup.find("ol")
    try:
        spell_issues = results.find_all("li")
    except:
        spell_issues = []

    globals.test_log = "logs/test_log_spell.xlsx"
    workbook = xlsxwriter.Workbook(globals.test_log)
    worksheet = workbook.add_worksheet("spell_checker")

    excel_row = 0
    worksheet.write(excel_row, 0, "spelling_issue")
    for issue in spell_issues:
        excel_row += 1
        worksheet.write(excel_row, 0, issue.text.strip())

    print(script_name + " : " + "Spelling issue count " + str(excel_row))
    workbook.close()

    print(script_name + " : " + "All results written to file " + globals.test_log)
"""


if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    execute()
    print(script_name + " : " + "Finished in " + str(
        (datetime.datetime.now() - globals.time_start).total_seconds()) + " seconds")
