import re
from urllib.parse import urlparse

import requests
import extract_page_title
#read the gospider webcrawler output
import extract_page_title
import globals
import webscrap_spell

crawler_urls_file = open('crawler_output/gospider_original.txt', 'r')
crawler_urls_all = crawler_urls_file.readlines()
url_list = []
website_domain = urlparse(globals.target_website).netloc

#iterate over each line of gospider
for line in crawler_urls_all:
    #only select those with url tag
    url_tag_flag = re.search('[url]', line)

    if url_tag_flag :
        try:
            #extract the  http or https URL
            url = re.search("(?P<url>https?://[^\s]+)", line).group("url")
            # only select those with website domain under test
            url_domain = urlparse(url).netloc
            if website_domain == url_domain:
                url_get_response = requests.get(url)
                # only select html type pages
                if "text/html" in url_get_response.headers["content-type"]:
                    print(url)
                    url_list.append(url)
                    extract_page_title.extract_title(url)
                    #webscrap_spell.execute(url)

        except AttributeError:
            pass


crawler_urls_file.close()


unique_url_file = open('crawler_output/url_list.txt', 'w')
#remove duplicates
url_list_unique = [*set(url_list)]
for line in url_list_unique:
    unique_url_file.write("%s\n" % line.strip())

unique_url_file.close()