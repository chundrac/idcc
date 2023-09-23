#!/usr/bin/python
# -*- coding: utf8 -*-

from collections import defaultdict
import re
import numpy as np
import random
import os

random.seed(1234)

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
    text[i].append(' '.join(form))

reflexes = defaultdict(list)
for l in text:
    reflexes[l[2]].append(' '.join(['#']+[s for s in l[9].split()]))


reflexes = {k:reflexes[k] for k in reflexes.keys() if len(reflexes[k]) > 500}

def detectIDCC(w):
    w_ = re.sub(r'(.)\1+',r'\1',w)
    w_ = w_.split()
    counter = 0
    for i,s in enumerate(w_):
        if i > 0 and s == w_[i-1]:
            counter += 1
    if counter > 0:
        return(1)
    else:
        return(0)

ratios = defaultdict(list)
for k in reflexes.keys():
  lang = k
  words = reflexes[k]
  for i,w in enumerate(words):
    if not w.startswith('#'):
      words[i] = '# '+w
  segs = sorted(set([s for w in words for s in w.split() if s != '#' and s != '$']))
  for t in range(5000):
    seg1 = random.sample(segs,1)[0]
    seg2 = random.sample(segs+[''],1)[0]
    condition = random.sample(['free','initial','medial'],1)[0]
    if condition == 'free':
        if seg2 == '':
            seg2 = random.sample(segs,1)[0]
        words_new = [w.replace(seg1,seg2) for w in words]
    if condition == 'initial':
        words_new = [w.replace('# ','#').replace('#'+seg1,'#'+seg2).replace('#','# ') for w in words]
    if condition == 'medial':
        words_new = [w.replace('# ','#').replace(' '+seg1,' '+seg2).replace('#','# ') for w in words]
    IDCC_before = [detectIDCC(w) for w in words]
    IDCC_after = [detectIDCC(w) for w in words_new]
    plus_to_minus = [i for i in range(len(IDCC_before)) if IDCC_before[i] == 1 and IDCC_after[i] == 0]
    minus_to_plus = [i for i in range(len(IDCC_before)) if IDCC_before[i] == 0 and IDCC_after[i] == 1]
    ratios[lang].append(len(plus_to_minus)+.001/(len(minus_to_plus)+.001))

#text = [['family','language','ratio']]

text = [['Uralic',key,str(np.mean(ratios[key]))] for key in ratios.keys()]

if 'sound_change_simulations.tsv' not in os.listdir('../../cognate_models/'):
    f = open('../../cognate_models/sound_change_simulations.tsv','w')
    text = [['family','language','ratio']]+text
    for l in text:
        print('\t'.join(l),file=f)
    f.close()
else:
    f = open('../../cognate_models/sound_change_simulations.tsv','a')
    for l in text:
        print('\t'.join(l),file=f)
    f.close()