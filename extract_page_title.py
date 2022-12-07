# importing the modules
import os

import requests
from bs4 import BeautifulSoup


def extract_title(url):
    # target url
    #url = 'https://dahd.nic.in/division/administration/vigilance-apar-cell'
    # making requests instance
    reqs = requests.get(url)
    # using the BeautifulSoup module
    soup = BeautifulSoup(reqs.text, 'html.parser')
    # displaying the title
    print("Title of the page is : ")
    for title in soup.find_all('title'):
        print(title.get_text())
    # Finding all meta tags present, stored in a list format 
    # meta_tag = soup.findAll('meta')
    # Looping the meta tag list 
    # print(meta_tag)
    # for x in meta_tag:
    # print(x.attrs['keywords'])
    # print('-----------------')

if __name__ == '__main__':
    #script_name = os.path.basename(__file__)
    urls_file = open('crawler_output/url_list.txt', 'r')
    urls_all = urls_file.readlines()
    for url in urls_all:
        print(url)
        extract_title(url.strip())
    urls_file.close()

