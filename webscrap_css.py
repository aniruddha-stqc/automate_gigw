import datetime
import os
import time

import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import globals


def execute():
    script_name = os.path.basename(__file__)
    print(script_name + " : " + "Launching W3C CSS Validation Service in Selenium Gecko Browser headlessly")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=globals.gecko_path, service_log_path=os.devnull)

    driver.get("https://jigsaw.w3.org/css-validator/")
    driver.find_element_by_id("uri").send_keys(globals.target_website)
    driver.find_element_by_xpath(
        "(.//*[normalize-space(text()) and normalize-space(.)='Vendor Extensions:'])[1]/following::span[1]").click()

    print(script_name + " : " + "Scanning target website " + globals.target_website + " for CSS issues")
    time.sleep(globals.time_wait)
    page_source = driver.page_source
    # Close the webdriver
    driver.close()
    # Selenium hands over the page source to Beautiful Soup for WebScraping

    print(script_name + " : " + "Parsing scan results using Beautiful Soup")
    page_soup = BeautifulSoup(page_source, "html.parser")

    print(script_name + " : " + "Parsing CSS errors")

    errors = page_soup.find_all("div", {"class": "error-section"})

    globals.test_log = "logs/test_log_css.xlsx"
    workbook = xlsxwriter.Workbook(globals.test_log)
    worksheet = workbook.add_worksheet("css_checker_errors")
    excel_row = 0
    worksheet.write(excel_row, 0, "error_uri")
    worksheet.write(excel_row, 1, "error_linenumber")
    worksheet.write(excel_row, 2, "error_codeContext")
    worksheet.write(excel_row, 3, "error_parse")

    for error in errors:
        error_uri = error.h4.a["href"]
        tbody = error.table.tbody.find_all("tr")
        for tr in tbody:
            excel_row += 1
            error_linenumber = tr.find("td", {"class": "linenumber"}).text.strip()
            try:
                error_codeContext = tr.find("td", {"class": "codeContext"}).text.strip()
                if not error_codeContext:
                    error_codeContext = "Not Applicable"
            except:
                try:
                    error_codeContext = tr.find("td", {"class": "nocontext"}).text.strip()
                    if not error_codeContext:
                        error_codeContext = "Not Applicable"
                except:
                    error_codeContext = "Not Applicable"
            try:
                error_parse = ' '.join(tr.find("td", {"class": "parse-error"}).text.split())
            except:
                try:
                    error_parse = tr.find("td", {"class": "invalidparam"}).text.strip()
                except:
                    error_parse = "Not Applicable"

            worksheet.write(excel_row, 0, error_uri)
            worksheet.write(excel_row, 1, error_linenumber)
            worksheet.write(excel_row, 2, error_codeContext)
            worksheet.write(excel_row, 3, error_parse)

    print(script_name + " : " + "CSS error count " + str(excel_row))
    print(script_name + " : " + "Parsing CSS warnings")

    worksheet = workbook.add_worksheet("css_checker_warnings")
    warnings = page_soup.find_all("div", {"class": "warning-section"})

    excel_row = 0
    worksheet.write(excel_row, 0, "warning_uri")
    worksheet.write(excel_row, 1, "warning_linenumber")
    worksheet.write(excel_row, 2, "warning_codeContext")
    worksheet.write(excel_row, 3, "warning_level")
    worksheet.write(excel_row, 4, "warning_text")

    for warning in warnings:
        warning_uri = warning.h4.a["href"]
        tbody = warning.table.tbody.find_all("tr")
        for tr in tbody:
            excel_row += 1
            warning_linenumber = tr.find("td", {"class": "linenumber"}).text.strip()
            warning_codeContext = tr.find("td", {"class": "codeContext"}).text.strip()
            if not warning_codeContext:
                warning_codeContext = "Not Applicable"
            try:
                warning_level0 = ' '.join(tr.find("td", {"class": "level0"}).text.split())
            except:
                warning_level0 = "Not Applicable"
            try:
                warning_level1 = ' '.join(tr.find("td", {"class": "level1"}).text.split())
            except:
                warning_level1 = "Not Applicable"
            worksheet.write(excel_row, 0, warning_uri)
            worksheet.write(excel_row, 1, warning_linenumber)
            worksheet.write(excel_row, 2, warning_codeContext)
            if warning_level1 == "Not Applicable":
                worksheet.write(excel_row, 3, "0")
                worksheet.write(excel_row, 4, warning_level0)
            else:
                worksheet.write(excel_row, 3, "1")
                worksheet.write(excel_row, 4, warning_level1)

    print(script_name + " : " + "CSS warning count " + str(excel_row))
    workbook.close()

    print(script_name + " : " + "All results written to file " + globals.test_log)


if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    execute()
    print(script_name + " : " + "Finished in " + str(
        (datetime.datetime.now() - globals.time_start).total_seconds()) + " seconds")