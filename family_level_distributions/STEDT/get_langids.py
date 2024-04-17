#from urllib.request import urlopen,Request
from bs4 import BeautifulSoup

from selenium import webdriver
import numpy as np


text = []
for l in open('lang_dict.tsv','r'):
    text.append(l.strip('\n').split('\t'))



langs = [l[1] for l in text if l[1] != '']


#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


#do something about 'Tibetan (Written)'
langids = []
driver = webdriver.Firefox()
for l in langs:
    print (l)
    url = 'https://stedt.berkeley.edu/~stedt-cgi/rootcanal.pl/edit/languagenames?languagenames.language={}'.format(l)
    #req = Request(url=url, headers=headers)
    #html = urlopen(req).read()
    #html = page.read()
    #page.close()
    #soup = BeautifulSoup(html)
    driver.get(url)
    text = driver.page_source
    soup = BeautifulSoup(text)
    if len(soup.find_all('tbody')) == 3:
        records = soup.find_all('tbody')[2].find_all('a')
        records = [t for t in records if 'target' in t.attrs and t['target']=='stedt_lexicon']
        if records != []:
            langid = [t['href'].split('=')[-1] for t in records]
            counts = [int(t.text.split()[0]) for t in records]
            max_ = np.argmax(counts)
            langids.append(langid[max_])