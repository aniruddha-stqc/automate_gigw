from bs4 import BeautifulSoup
import xlsxwriter
import globals
html_file = open("D:\\aniruddha\\wqc\\mea\\mea_sortsite\\map.ERR.htm")
page_soup = BeautifulSoup(html_file, 'html.parser')


issues = page_soup.find("table", {"class": "issues"})

tbody = issues.find_all("tbody")


globals.test_log = "logs/test_log_broken.xlsx"
workbook = xlsxwriter.Workbook(globals.test_log)
worksheet = workbook.add_worksheet("link_issues")
excel_row = 0
worksheet.write(excel_row, 0, "Text")
worksheet.write(excel_row, 1, "Text1")
worksheet.write(excel_row, 2, "Text2")
worksheet.write(excel_row, 3, "Text3")


row = 1
for tbody_single_row in tbody:
    print("********************************")
    #tbody is alternating
    try:
        tr = tbody[row].find_all("tr")
    except:
        pass
    tr_index = 0
    for tr_single_row in tr:
        print("--------------------------------------------------------------------")
        tr_index = tr_index + 1
        try:

            # initializing split word

            #print(tr[tr_index].text)
            broken_link_result = tr[tr_index].find_all("a", {"class", "viewsource"})
            full_string = tr[tr_index].text
            broken_url = broken_link_result[0].text

            print("Issue Description: ", full_string.partition(broken_url)[0])
            print("Issue Text 1: ", broken_url)
            print("Issue Text 2: ", broken_link_result[1].text)
            print("Issue Text 3: ", broken_link_result[2].text)

            excel_row += 1
            worksheet.write(excel_row, 0, str( full_string.partition(broken_url)[0]))
            worksheet.write(excel_row, 1,  str( broken_url))
            worksheet.write(excel_row, 2,  str( broken_link_result[1].text))
            worksheet.write(excel_row, 3,  str( broken_link_result[2].text))

        except Exception as e:
            print(e)
            pass
    #broken_link_result = tr[5].find_all("a", {"class", "viewsource"});
    #broken_link_result
    #print(broken_link_result[0].text)
    #print(broken_link_result[1].text)
    #print(broken_link_result[2].text)
    #print(tr[1].text)
    #print(tbody[5].text)
    row = row + 2

workbook.close()