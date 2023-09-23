from bs4 import BeautifulSoup

f = open('northern_paiute_bridgeport_source.html','r')
html = f.read()
f.close()

soup = BeautifulSoup(html)

f = open('Northern_Paiute_wordlist.txt','w')

for w in [s.text for s in soup.find_all('strong')][:-2]:
    print(w,file=f)

f.close()