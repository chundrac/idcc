import os
text=[]
for fn in os.listdir('scraped_tables'):
  if fn.startswith('lexicon'):
    f = open('scraped_tables/{}'.format(fn),'r')
    text_=f.read()
    f.close()
    text_=text_.split('\n')
    text+=text_[1:-1]


f = open('all_forms.tsv','w')
for l in text:
    print(l,file=f)


f.close()
