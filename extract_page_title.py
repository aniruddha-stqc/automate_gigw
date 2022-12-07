# importing the modules
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

