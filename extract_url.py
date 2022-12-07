import re
from urllib.parse import urlparse

import requests
import extract_page_title
#read the gospider webcrawler output
import extract_page_title
import webscrap_spell

file = open('crawler_output/gospider.txt', 'r')

lines_all = file.readlines()

#iterate over each line of gospider
for line in lines_all:
    url_line = re.search('[url]',line) and re.search('[dahd.nic.in]',line)
    #link =  re.search('[.pdf]', line)
    if url_line :
        try:
            #extract the  http or https URL
            url = re.search("(?P<url>https?://[^\s]+)", line).group("url")
            domain = urlparse(url).netloc
            if domain == "dahd.nic.in":
                url_get_response = requests.get(url)
                if "text/html" in url_get_response.headers["content-type"]:
                    print(url)
                    extract_page_title.extract_title(url)
                    #webscrap_spell.execute(url)
            #print(url)
            #webscrap_spell.execute(url)
        except AttributeError:
            pass


        #print(line.strip())

file.close()