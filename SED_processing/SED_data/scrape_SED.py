from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

page_urls = []
for i in range(1,198):
    page = urlopen('http://sed-online.ru/reconstructions?reconstructions_page={}'.format(i))
    html = page.read()
    page.close()
    soup = BeautifulSoup(html,'lxml')
    for t in soup.find_all('span',{'class':'h3'})[1::2]:
        page_urls.append(t.find('a')['href'])

for url in page_urls:
    page = urlopen('http://sed-online.ru/{}'.format(url))
    html = page.read()
    page.close()
    f = open('html/'+url.split('/')[-1]+'.html','w')
    print(html,file=f)
    f.close()


cogsets = []
for url in page_urls:
    page = urlopen('http://sed-online.ru/{}'.format(url))
    html = page.read()
    page.close()
    #f = open('html/'+url.split('/')[-1]+'.html','w')
    #print(html,file=f)
    #f.close()
    soup = BeautifulSoup(html,'lxml')
    protolang = soup.find('div',{'class':'col-md-4 col-xs-6 h1'}).text
    reconstruction = soup.find('h1').text.split('\n')[0]
    tags = soup.find_all('span',{'class':'h3'})
    langs = tags[::2]
    forms = tags[1::2]
    for i,l in enumerate(langs):
        #print(l.find('span').text,forms[i].text.split('\n')[1])
        cogsets.append([url,protolang,reconstruction,l.find('span').text]+forms[i].text.split('\n')[1].split(' - '))

f = open('SED_cognates.tsv','w')
print('\t'.join(['ID','Protolanguage','Reconstruction','Language','Form','Gloss']),file=f)
for l in cogsets:
    print('\t'.join(l),file=f)

f.close()