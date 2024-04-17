

lang_dict = {}
for l in open('lang_dict2.tsv','r'):
    lang_dict[l.split('\t')[2].strip()] = l.split('\t')[0]



text = []
for l in open('all_forms.tsv','r'):
    text.append(l.strip().split('\t'))



data = []
for l in text:
    form = l[4]
    lang = lang_dict[l[8]]
    data.append([form,lang])



f = open('processed_data.tsv','w')
for l in data:
    print('\t'.join(l),file=f)



f.close()