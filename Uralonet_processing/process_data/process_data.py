#!/usr/bin/python
# -*- coding: utf8 -*-

from collections import defaultdict
import re
import numpy as np

text = [l.strip('\n').split('\t') for l in open('uralonet_merged_reflex_aligned.tsv','r')]

for i,l in enumerate(text):
    text[i][2] = l[2].replace('? ','')

langcount = defaultdict(int)
for l in text:
    langcount[l[2]] +=1
    #langcount[(l[2],l[3])] +=1

langs = list(langcount.keys())

taxa = ['Estonian', 'Finnish', 'Hungarian', 'Karelian', 'Khanty', 'Komi', 'Livonian', 'Mansi', 'Mari', 'Mordvin', 'Nenets', 'Northern_Sami', 'Selkup', 'Skolt_Sami', 'Udmurt', 'Ume_Sami', 'Veps']

converter = {
    'Komi/Zyryan':'Komi',
    'Udmurt/Votyak':'Udmurt',
    'Mari/Cheremis':'Mari',
    'Khanty/Ostyak':'Khanty',
    'Mansi/Vogul':'Mansi',
    'Saami/Lappish':'Northern_Sami',
    'Enets':'Nenets',
    'Nenets/Yurak':'Nenets'  
}

for i,l in enumerate(text):
    if l[2] in converter.keys():
        text[i][2] = converter[l[2]]

text = [l for l in text if l[2] in taxa]

protoform = {}
for l in text:
    protoform[l[0]] = l[1]

hungarian_converter = {
    'cs':'C',
    'gy':'G',
    'ly':'L',
    'ny':'N',
    'sz':'S',
    'ty':'T',
    'zs':'Z'
}

general_converter = {
    'ts':'C'
}

for i,l in enumerate(text):
    w = l[-1]
    w = w.lower()
    if l[2] == 'Hungarian':
        for k in hungarian_converter.keys():
            w = w.replace(k,hungarian_converter[k])
    for k in general_converter.keys():
        w = w.replace(k,general_converter[k])
    text[i].append(w)

segs = sorted(set([s for l in text for s in list(l[-1])]))

ligatures = ['`', '°', '´', '·', 'ʹ', 'ʼ', 'ʽ', 'ˆ', 'ˈ', 'ˉ', 'ˊ', 'ˋ', '˘', '˙', '̨', '˚', "'", '˯', '˰', '˳', '˴', '̀', '́', '̂', '̃', '̄', '̆', '̇', '̈', '̊', '̌', '̍', '̑', '̔', '̕', '̖', '̜', '̣', '̤', '̥', '̨', '̬', '̭', '̮', '̯', '̰', '́', 'ͅ', '͑', '͔', '͕', 'ͤ', '΄', 'ъ', 'ь']

newsegs = []
for i,l in enumerate(text):
  w = l[-1]
  if w != '':
    w_ = list(w)
    w__ = []
    s_ = w_[0]
    for j,s in enumerate(w_):
      if j > 0:
        if s in ligatures or w_[j-1] == s:
            s_ += s
        else:
            w__.append(s_)
            s_ = s
    if s_ != '':
        w__.append(s_)
    w___ = []
    s_ = w__[0]
    for j,s in enumerate(w__):
      if j > 0:
        if w__[j-1] == s:
            s_ += s
        else:
            w___.append(s_)
            s_ = s
    if s_ != '':
        w___.append(s_)
    text[i][-1] = ' '.join(w___)
    newsegs += w___

newsegs = sorted(set(newsegs))

#cons = ['C', 'G', 'L', 'N', 'S', 'T', 'Z', 'b', 'bb', 'bˈ', 'b́', 'c', 'cc', 'cˈ', 'c̀', 'č', 'č́', 'd', 'dd', 'dˈ', 'd́', 'd̍', 'f', 'ff', 'g', 'g`', 'gg', 'gˈ', 'ǵ', 'g̑', 'g̜', 'g̬', 'h', 'h˘', 'h̄ˈ', 'h̭', 'j', 'jj', 'j˴', 'j̀', 'j̆', 'j̮', 'k', 'k`', 'kk', 'kḱ͔', 'kʽ', 'kˈ', 'kˋ', 'k˳', 'k̀', 'k̀́', 'k͕̀', 'ḱ', 'ḱ͕', 'k̄', 'k͕̄', 'k̆', 'k͔̕', 'ḳ', 'k̨', 'k͔', 'k͕', 'l', 'll', 'lˈ', 'ĺ', 'ĺ̨', 'l̄', 'l̨̄', 'l͔̄', 'l͔̑', 'l̔', 'ḷ', 'l̥', 'l̨', 'l͑', 'l͔', 'm', 'mm', 'mˈ', 'm̀', 'ḿ', 'm̄', 'm̥', 'n', 'n`', 'nn', 'ń', 'ń̄', 'n̄', 'n̨̄', 'n̆', 'ṇ', 'n̨', 'p', 'p`', 'pp', 'p°', 'pˈ', 'p̀', 'ṕ', 'p̄', 'p̆', 'q', 'qq', 'r', 'r`', 'rr', 'rʽ', 'rˈ', 'r˴', 'r̀', 'ŕ', 'ŕ̭', 'r̄', 'r̨̄', 'r͔̄', 'r̆', 'r̖', 'r̨', 'r̀ͅ', 'r͔', 'r΄', 's', 's`', 'ss', 'sˈ', 's̀', 's̨̀', 'ś', 's̄', 's̨̄', 's̨̄ˈ', 's̮̄', 'š', 'š́', 'š́ˋ', 'š́̆', 'š̨́', 'š̄', 'š̨̄', 'ṣ̌', 'š̨', 's̨', 't', 'tt', 'ttt', 'tˈ', 'tˊˋ', 'tˋ', 't̀', 't̀́', 't̨̀', 't́', 't̨́', 't̄', 'ṭ̄', 't̨̄', 't̆', 't̨̆', 't̍', 't̕', 't̨', 'u', 'uu', 'uuˈ', 'uū̯', 'uu̯', 'u·', 'uˈ', 'ù', 'ṷ̀', 'ù͕', 'û', 'ū', 'ū́', 'ū̯', 'ŭ', 'ŭ͔', 'ŭ͕', 'u̇', 'ü', 'u̬', 'u̯', 'ṵ', 'u͔', 'u͕', 'u͕˴', 'v', 'vv', 'vˈ', 'vˋ', 'v̄', 'w', 'wˈ', 'w̆', 'w̮̆', 'x', 'x̄', 'y', 'yy', 'ȳ', 'z', 'zz', 'ź', 'ž', 'ž́', 'ð', 'ñ', 'ññ', 'ć', 'ćć', 'č', 'čč', 'čˈ', 'ď', 'ďď', 'đ', 'đđ', 'đˈ', 'ľ', 'ľľ', 'ľ́', 'ľ̄́', 'ł', 'łł', 'ń', 'ńń', 'ńʽ', 'ŋ', 'ŋŋ', 'ŋˈ', 'ŋ˳', 'ŋ́', 'ŋ̄', 'ŋ̥', 'ŕ', 'ř', 'ś', 'śś', 'š', 'šš', 'šˈ', 'š́', 'ť', 'ŧ', 'ŧŧ', 'ŧˈ', 'ź', 'ž', 'ƞ', 'ƞˉ͔', 'ƞ̄', 'ƞ͔', 'ƞ͕̄', 'ǥ', 'ǯ', 'ǯ´', 'ǯǯ', 'ǯˈ', 'ǯ́', 'ǵ', 'ɢ', 'ɢ̀', 'ɢ͕̀́ˈ', 'ɢ̄', 'ɢ͕̆', 'ɢ͕', 'ʃ', 'ʃʃ', 'ʋ', 'ʒ', 'ʒʒ', 'ʒˈ', 'ʒ́', 'ʔ', 'ʙ', 'ʙ̀', 'ʙ̄', 'ʜ', 'ʜ`', 'ʜ̆', 'ʟ', 'ʟ́', 'ʧ', 'ʫ', 'β', 'γ', 'γˊ', 'γˋ', 'γ˳', 'γ̄', 'δ', 'δˉ', 'δ̄', 'δ̕', 'δδ', 'ν', 'ν́', 'φ', 'χ', 'χˉ͔', 'χ˳', 'χ́', 'χ̄', 'χ̤', 'χ̤́', 'χ̥', 'ϑ', 'б', 'в', 'г', 'гъ', 'д', 'ж', 'з', 'к', 'л', 'л˴', 'л̄', 'лл', 'лъ', 'м', 'мъ', 'н', 'п', 'пъ', 'р', 'рр', 'рь', 'с', 'съ', 'сь', 'т', 'тъ', 'х', 'хъ', 'ч', 'чь', 'ш', 'ш̆', 'щ', 'ѕ', 'ӡ̌́', 'ᴅ', 'ᴅ̀', 'ᴅ̀́', 'ᴅ̨̀', 'ᴅ́', 'ᴅ́̀', 'ᴅ̨́', 'ᴅ̄', 'ᴅ̨̄', 'ᴅ̆', 'ᴅ̌', 'ᴅ̨', 'ᴅᴅ', 'ᴋ', 'ᴘ', 'ᴛ', 'ᴢ', 'ᴢ̌́']

cons = ['C', 'C̀', 'C̄', 'C̨̄', 'Č', 'Č́', 'Č̄', 'C̨', 'G', 'L', 'N', 'S', 'T', 'Z', 'b', "b'", 'bb', 'bˈ', 'b́', 'c', "c'", 'cc', 'cˈ', 'c̀', 'č', 'č́', 'č́č́', 'ć', 'd', "d'", 'dd', 'dˈ', 'd́', 'd̍', 'f', 'ff', 'g', "g'", 'g`', 'gg', 'gˈ', 'ǵ', 'g̑', 'g̜', 'g̬', 'h', "h'", 'h˘', 'h̄ˈ', 'h̭', 'j', 'jj', 'j˴', 'j̀', 'j̆', 'j̮', 'k', "k'", 'k`', 'kk', 'kḱ͔', 'kʽ', 'kˈ', 'kˋ', 'k˳', 'k̀', 'k̀́', 'k͕̀', 'ḱ', 'ḱ͕', 'ḱ͕ḱ͕', 'k̄', 'k͕̄', 'k̆', 'k͔̕', 'ḳ', 'k̨', 'k͔', 'k͔k͔', 'k͕', 'k͕k͕', 'l', "l'", 'll', 'lˈ', 'ĺ', 'l̄', 'l̨̄', 'l͔̄', 'l͔̑', 'l̔', 'ḷ', 'l̥', 'l̨', 'l̨l̨', 'l͑', 'l͔', 'm', 'mm', 'mˈ', 'm̀', 'ḿ', 'm̄', 'm̥', 'n', "n'", 'n`', 'nn', 'ń', 'ń̄', 'n̄', 'n̨̄', 'n̆', 'ṇ', 'n̨', 'n̨n̨', 'p', "p'", 'p`', 'pp', 'p°', 'pˈ', 'p̀', 'ṕ', 'p̄', 'p̆', 'q', 'qq', 'r', "r'", 'r`', 'rr', 'rʽ', 'rˈ', 'r˴', 'r̀', 'ŕ', 'r̄', 'r̨̄', 'r͔̄', 'r̆', 'r̖', 'r̨', 'r͔', 'r΄', 's', "s'", 's`', 'ss', 'sˈ', 's̀', 's̨̀', 'ś', 's̄', 's̨̄', 's̨̄ˈ', 's̮̄', 'š', 'š́', 'š́ˋ', 'š́̆', 'š̨́', 'š̄', 'š̨̄', 'ṣ̌', 'š̨', 'š̨š̨', 's̨', 's̨s̨', 't', "t'", 'tt', 'ttt', 'tˈ', 'tˊˋ', 'tˋ', 't̀', 't̀́', 't̨̀', 't́', "t́'", 't́t́', 't̨́', 't̄', 'ṭ̄', 't̨̄', 't̆', 't̨̆', 't̍', 't̕', 't̨', 't̨t̨', 'v', 'vv', 'vˈ', 'v̄', 'w', "w'", 'wˈ', 'w̆', 'w̮̆', 'x', 'x̄', 'y', 'yy', 'ȳ', 'z', 'zz', 'ź', 'ž', 'ž́', 'ð', 'ñ', 'ññ', 'ć', 'ćć', 'č', "č'", 'čč', 'čˈ', 'ď', 'ďď', 'đ', "đ'", 'đđ', 'đˈ', 'ľ', 'ľľ', 'ľ́', 'ľ̄́', 'ł', 'łł', 'ń', 'ńń', 'ńʽ', 'ŋ', "ŋ'", 'ŋŋ', 'ŋˈ', 'ŋ˳', 'ŋ́', 'ŋ̄', 'ŋ̥', 'ŕ', 'ř', 'ś', 'śś', 'š', "š'", 'šš', 'šˈ', 'š́', 'ť', 'ŧ', "ŧ'", 'ŧŧ', 'ŧˈ', 'ź', 'ž', 'ƞ', 'ƞˉ͔', 'ƞ̄', 'ƞ͔', 'ƞ͕̄', 'ǯ', 'ǯ´', 'ǯ´ǯ´', 'ǯǯ', 'ǯˈ', 'ǯ́', 'ǵ', 'ɢ', 'ɢ̀', 'ɢ͕̀́ˈ', 'ɢ̄', 'ɢ͕̆', 'ɢ͕', 'ɴ', 'ʃ', 'ʃʃ', 'ʋ', 'ʒ', "ʒ'", 'ʒʒ', 'ʒˈ', 'ʒ́', 'ʒ́ʒ́', 'ʔ', 'ʙ', 'ʙ̀', 'ʙ̄', 'ʜ', 'ʜ`', 'ʜ̆', 'ʟ', 'ʟ́', 'ʧ', 'ʫ', '·', 'β', 'γ', 'γˊ', 'γˋ', 'γ˳', 'γ̄', 'δ', 'δˉ', 'δ̄', 'δ̕', 'δδ', 'ν', 'ν́', 'φ', 'χ', 'χˉ͔', 'χ˳', 'χ́', 'χ̄', 'χ̤', 'χ̤́', 'χ̥', 'ϑ', 'б', 'в', 'г', 'гъ', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'л˴', 'л̄', 'лл', 'лъ', 'м', 'мъ', 'н', 'о', 'п', 'пъ', 'р', 'рр', 'рь', 'с', 'съ', 'сь', 'т', 'тъ', 'х', 'хъ', 'ч', 'чь', 'ш', 'ш̆', 'щ', 'ѕ', 'ӡ̌́', 'ᴅ', 'ᴅ̀', 'ᴅ̀́', 'ᴅ̨̀', 'ᴅ́', 'ᴅ́̀', 'ᴅ̄', 'ᴅ̨̄', 'ᴅ̆', 'ᴅ̨', 'ᴅ̨ᴅ̨', 'ᴅᴅ', 'ᴘ', 'ᴛ', 'ᴢ', 'ᴢ̌́']

langs = set([l[2] for l in text])

lang_cons = defaultdict(list)

for lang in langs:
    lang_cons[lang] = cons

lang_cons['Finnish'].pop(lang_cons['Finnish'].index('y'))
lang_cons['Finnish'].pop(lang_cons['Finnish'].index('yy'))

for i,l in enumerate(text):
    form = l[-1]
    form = form.split()
    form = [re.sub(r'(.)\1+',r'\1',s) for s in form if s in lang_cons[l[2]]]
    counter = 0
    for j,s in enumerate(form):
        if j > 0 and s == form[j-1]:
            counter += 1
    text[i].append(' '.join(form))
    if counter > 0:
        #text[i].append('TRUE')
        text[i].append('1')
    else:
        #text[i].append('FALSE')
        text[i].append('0')

f = open('data_coded.tsv','w')
for l in text:
  print('\t'.join(l),file=f)

f.close()

coding = {}
coding_string = defaultdict()
for l in text:
    if l[2] not in coding.keys():
        coding[l[2]] = defaultdict(list)
        coding_string[l[2]] = defaultdict(list)
    coding[l[2]][l[0]].append(l[-1])
    coding_string[l[2]][l[0]].append(l[4])

langs_to_keep = [lang for lang in coding.keys()]

L = len(langs_to_keep)

coding_ = {}
for lang in coding.keys():
    if lang in langs_to_keep:
        coding_[lang] = coding[lang]

coding = coding_

cogvar = defaultdict(list)
for lang in coding.keys():
    for k in coding[lang].keys():
        cogvar[k] += coding[lang][k]

for k in cogvar.keys():
    cogvar[k] = sorted(set(cogvar[k]))

coglang = defaultdict(list)
for lang in coding.keys():
    for k in coding[lang].keys():
        coglang[k].append(lang)

#cogs_to_keep = [k for k in coglang.keys() if len(coglang[k])>1]
#cogs_to_keep = [k for k in coglang.keys() if len(cogvar[k]) > 1 and len(coglang[k])>1]
cogs_to_keep = [k for k in coglang.keys() if len(coglang[k])>L/10]

colnames = ['']
charvalues = []
L = len(langs_to_keep)

print(L,len(cogs_to_keep))

for cog in cogs_to_keep:
    names = ['absent','0','1']
    vals = np.zeros([L,len(names)])
    for lang in langs_to_keep:
        if cog in coding[lang].keys():
            for v in coding[lang][cog]:
                vals[langs_to_keep.index(lang),names.index(v)] = 1
        else:
            vals[langs_to_keep.index(lang),names.index('absent')] = 1
    colnames += [cog+':'+''.join(n) for n in names]
    charvalues.append(vals)

charvalues = np.concatenate(charvalues,-1)

f = open('../data/character_data.tsv','w')
print('\t'.join(colnames),file=f)
for i,lang in enumerate(langs_to_keep):
    print('\t'.join([lang]+[str(s) for s in list(charvalues[i,])]),file=f)

f.close()

f = open('../data/character_data_string.tsv','w')

print('\t'.join(['']+[protoform[s] for s in cogs_to_keep]),file=f)

for lang in langs_to_keep:
    ll = [lang]
    for cog in cogs_to_keep:
        if cog in coding_string[lang].keys():
            form = ', '.join(set(coding_string[lang][cog]))
            ll.append(form)
        else:
            ll.append('')
    print('\t'.join(ll),file=f)

f.close()

f = open('../data/etymon_data.tsv','w')
for cog in cogs_to_keep:
    w = protoform[cog]
    w = w.replace('(','').replace(')','')
    w_ = list(w)
    w__ = []
    s_ = w_[0]
    for j,s in enumerate(w_):
      if j > 0:
        if s in ligatures or w_[j-1] == s:
            s_ += s
        else:
            w__.append(s_)
            s_ = s
    if s_ != '':
        w__.append(s_)
    w___ = []
    s_ = w__[0]
    for j,s in enumerate(w__):
      if j > 0:
        if w__[j-1] == s:
            s_ += s
        else:
            w___.append(re.sub(r'(.)\1+',r'\1',s_))
            s_ = s
    if s_ != '':
        w___.append(re.sub(r'(.)\1+',r'\1',s_))
    w_ = [s for s in w___ if s in cons]
    coding = '0'
    counter = 0
    for i,s in enumerate(w_):
        if i > 0 and s == w_[i-1]:
            counter += 1
    if counter > 0:
        coding = '1'
    print('\t'.join([cog,protoform[cog],coding]),file=f)

f.close()