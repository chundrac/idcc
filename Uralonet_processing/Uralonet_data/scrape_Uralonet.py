from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

counter = 1
url = 'http://uralonet.nytud.hu/eintrag.cgi?locale=en_GB&id_eintrag=1'
page = urlopen(url)

cogsets = []
while counter == 1:
    html = page.read()
    page.close()
    soup = BeautifulSoup(html,'lxml')
    lang = ''
    cogsets_ = []
    etym = soup.find('a',{'class':'l'}).text.split('\n')[1]
    for tag in soup.find_all('tr'):
        dialect = ''
        form = ''
        meaning = ''
        if len(tag.find_all('td',{'class':'SPRACHEFIRST'})) != 0:
            lang = tag.find('td',{'class':'SPRACHEFIRST'}).text
        for tag_ in tag.find_all('td'):
            if 'class' in tag_.attrs and tag_['class'] == ['vergleich', 'BELEG_AB']:
                dialect = tag_.text
            for t in tag_.find_all('span'):
                if len(t.find_all('i')) != 0:
                    form = t.find('i').text
                if 'class' in t.attrs and t['class'] == ['bed']:
                    meaning = t.text
                    cogsets_.append(tuple([url,etym,lang,dialect,form,meaning]))
    button = [t for t in soup.find_all('a') if 'Next ' in t.text]
    if len(button) == 0:
        counter = 0
        break
    else:
        button = button[0]
        href = button['href'][1:]
        url = 'http://uralonet.nytud.hu/eintrag.cgi?locale=en_GB&'+href
        page = urlopen(url)
    cogsets += set(cogsets_)


f = open('Uralonet_cogsets.tsv','w')
for l in cogsets:
    print('\t'.join(l),file=f)

f.close()


#for tag in soup.find_all('tr'):
#    lang = ''
#    dialect = ''
#    form = ''
#    meaning = ''
#    if len(tag.find_all('td',{'class':'SPRACHEFIRST'})) != 0:
#        lang = tag.find('td',{'class':'SPRACHEFIRST'}).text
#        for tag_ in tag.find_all('td'):
#            if 'class' in tag_.attrs and tag_['class'] == ['vergleich', 'BELEG_AB']:
#                dialect = tag_.text
#            for t in tag_.find_all('span'):
#                if len(t.find_all('i')) != 0:
#                    form = t.find('i').text
#                    print(lang,dialect,form,meaning)
#                if 'class' in t.attrs and t['class'] == ['bed']:
#                    meaning = t.text
#                    print(lang,dialect,form,meaning)
                



