#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import re
import numpy as np

text = [l.strip('\n').split('\t') for l in open('SED_merged_reflex_aligned.tsv','r')]

langcount = defaultdict(int)
for l in text:
    langcount[l[3]] +=1

langs = list(langcount.keys())

taxa = ['Mehri', 'Harsusi', 'Soqotri', 'Jibbali', 'Tigrinya', 'Tigre', 'Geez', 'Mesqan', 'Geto', 
'Chaha', 'Mesmes', 'Innemor', 'Soddo', 'Harari', 'Zway', 'Walani', 'Argobba', 'Amharic', 'Gafat', 
'Aramaic', "'Moroccan.Arabic'", "'Ogaden.Arabic'", 'Ugaritic', 'Hebrew', 'Akkadian']

[l for l in taxa if l not in langs]

[(l,langcount[l]) for l in langs if l not in taxa]

converter = {
    'Masqan':'Mesqan',
    'Gyeto':'Geto',
    'Ennemor':'Innemor',
    'Wolane':'Walani',
    'Endegen':'Mesmes', #proxy
    'Arabic':"'Moroccan.Arabic'", #proxy
}

for i,l in enumerate(text):
    if l[3] in converter.keys():
        text[i][3] = converter[l[3]]

text = [l for l in text if l[3] in taxa]

for i,l in enumerate(text):
    text[i][7] = text[i][7].lower()
    text[i][7] = text[i][7].replace('ﬁ','fi')

protoform = {}
for l in text:
    protoform[l[0].split('/')[-1]] = l[1]+' '+l[2]

segs = sorted(set([s for l in text for s in list(l[7])]))

ligatures = ['ʰ', 'ʷ', 'ʸ', 'ʼ', 'ʾ', 'ˀ', 'ˁ', 'ˇ', '̣', '̀', '́', '̂', '̃', '̄', '̅', '̆', '̇', '̈', '̌', '̠', '̢', '̣', '̱', '̲', '͂', 'ᵂ', 'ᵉ', 'ᵗ', '’', 'ⁿ', '₄']

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

#cons = ['b', 'bb', 'bbʷ', 'bʷ', 'bˀ', 'bˁ', 'ḇ', 'bᵂ', 'd', 'dd', 'dˀ', 'dˁ', 'f', 'ff', 'fʷ', 'fˀ', 'fˁ', 'g', 'gg', 'ggʷ', 'gʷ', 'gʸ', 'gˀ', 'gˁ', 'g’', 'h', 'hh', 'hʷ', 'ḥ', 'k', 'kk', 'kkʷ', 'kk’', 'kʷ', 'kʸ', 'kˀ', 'k’', 'l', 'll', 'llˀ', 'lʼ', 'lʼˁ', 'lˀ', 'lˁ', 'm', 'mm', 'mmˁ', 'mʷ', 'mˀ', 'mˁ', 'm̠', 'm̱', 'm̲', 'm̲ˀ', 'n', 'nn', 'nˀ', 'nˁ', 'ñ', 'n̄', 'p', 'pp', 'pʷ', 'pˀ', 'pˁ', 'q', 'qq', 'qˁ', 'r', 'rr', 'rˀ', 'rˁ', 's', 'ss', 'sʷ', 'sˀ', 'sˁ', 's̀', 's̃', 'ṣ', 't', 'tt', 'tˁ', 'ṯ', 'w', 'ww', 'wˀ', 'wˁ', 'x', 'xʷ', 'y', 'yy', 'yʰ', 'yˀ', 'yˁ', 'z', 'zz', 'zˀ', 'zˁ', 'ẑ', 'z̃', 'z͂', 'ñ', 'ññ', 'č', 'čč', 'čč̣' ,'č̣č̣', 'č̣', 'ľ', 'ľľ', 'ň', 'ňň', 'ŝ', 'ŝŝ', 'ŝˀ', 'ŝˁ', 'ṣ̂', 'ṣ̂ˀ', 'ŝᵉ', 'š', 'šš', 'šˀ', 'šˁ', 'ṣ̌', 'ź', 'ž', 'žž', 'ǧ', 'ǯ', 'ǯǯ', 'ǯˀ', 'ǯˁ', 'ǯ', 'ʕ', 'γ', 'γγ', 'х', 'ḇ', 'ḇˀ', 'ḍ', 'ḍˁ', 'ḍḍ', 'ḏ', 'ḏ̣', 'ḥ', 'ḥḥ', 'ḫ', 'ḫʷ', 'ḫḫ', 'ḳ', 'ḳʷ', 'ḳʷˁ', 'ḳʸ', 'ḳˀ', 'ḳˁ', 'ḳ̌', 'ḳ̌ʷ', 'ḳḳ', 'ḳḳʷ', 'ḳ’', 'ḵ', 'ḵʷ', 'ḷ', 'ḷˁ', 'ṗ', 'ṣ', 'ṣˀ', 'ṣˁ', 'ṣ̂', 'ṣ̃', 'ṣ̌', 'ṣṣ', 'ṭ', 'ṭˁ', 'ṭṭ', 'ṯ', 'ṯˀ', 'ṯˁ', 'ṯ̣', 'ṯ̣ˀ', 'ṯ̣ˁ', 'ṯṯ', 'ẑ', 'ẑˁ', 'ẓ̂', 'ẑẑ', 'ẓ̂', 'ẓ̂ˁ']

cons = ["b", "bb", "bbʷ", "bʷ", "bˀ", "bˁ", "ḇ", "bᵂ", "d", "dd", "dˀ", "dˁ", "f", "ff", "fʷ", "fˀ", "fˁ", "g", "gg", "ggʷ", "gʷ", "gʸ", "gˀ", "gˁ", "g’", "h", "hh", "hʷ", "ḥ", "k", "kk", "kkʷ", "kk’", "kʷ", "kʸ", "kˀ", "k’", "l", "ll", "llˀ", "lʼ", "lʼˁ", "lˀ", "lˁ", "m", "mm", "mmˁ", "mʷ", "mˀ", "mˁ", "m̠", "m̱", "m̲", "m̲ˀ", "n", "nn", "nˀ", "nˁ", "ñ", "ññ", "n̄n̄", "p", "pp", "pʷ", "pˀ", "pˁ", "q", "qq", "qˁ", "r", "rr", "rˀ", "rˁ", "s", "ss", "sʷ", "sˀ", "sˁ", "s̀", "s̃", "ṣ", "t", "tt", "tˁ", "ṯ", "w", "ww", "wˀ", "wˁ", "x", "xʷ", "y", "yy", "yʰ", "yˀ", "yˁ", "z", "zz", "zˀ", "zˁ", "zˁzˁ", "ẑ", "z̃", "z͂", "ñ", "ññ", "č", "čč", "čč̣", "č̣", "č̣č̣", "ľ", "ľľ", "ň", "ňň", "ŝ", "ŝŝ", "ŝˀ", "ŝˁ", "ṣ̂", "ṣ̂ṣ̂", "ṣ̂ˀ", "ŝᵉ", "š", "šš", "šˀ", "šˁ", "ṣ̌", "ź", "ž", "žž", "ǧ", "ǯ", "ǯǯ", "ǯˀ", "ǯˁ", "ǯ", "ʕ", "γ", "γγ", "х", "ḇ", "ḇˀ", "ḍ", "ḍˁ", "ḍḍ", "ḏ", "ḏ̣", "ḏ̣ḏ̣", "ḥ", "ḥḥ", "ḫ", "ḫʷ", "ḫḫ", "ḳ", "ḳʷ", "ḳʷˁ", "ḳʸ", "ḳˀ", "ḳˁ", "ḳ̌", "ḳ̌ʷ", "ḳḳ", "ḳḳʷ", "ḳ’", "ḵ", "ḵʷ", "ḷ", "ḷˁ", "ṗ", "ṣ", "ṣˀ", "ṣˁ", "ṣ̂", "ṣ̃", "ṣ̌", "ṣṣ", "ṭ", "ṭˁ", "ṭṭ", "ṯ", "ṯˀ", "ṯˁ", "ṯ̣", "ṯ̣ˀ", "ṯ̣ˁ", "ṯṯ", "ẑ", "ẑˁ", "ẓ̂", "ẑẑ", "ẓ̂", "ẓ̂ˁ"]

#deal with cases where citation form is a consonantal root, and C1C1 is not a geminate

for i,l in enumerate(text):
    form = l[7].split()
    if len([s for s in form if s in cons])==len(form):
        w = l[6]
        if w != '':
          w_ = list(w)
          w__ = []
          s_ = w_[0]
          for j,s in enumerate(w_):
            if j > 0:
              if s in ligatures:
                  s_ += s
              else:
                  w__.append(s_)
                  s_ = s
          if s_ != '':
              w__.append(s_)
          text[i][7] = ' '.join(w__)

for i,l in enumerate(text):
    form = l[7]
    form = re.sub(r'(.)\1+',r'\1',form)
    form = form.split()
    form = [s for s in form if s in cons]
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
    if l[3] not in coding.keys():
        coding[l[3]] = defaultdict(list)
        coding_string[l[3]] = defaultdict(list)
    coding[l[3]][l[0].split('/')[-1]].append(l[-1])
    coding_string[l[3]][l[0].split('/')[-1]].append(l[4])

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
    #w = ' '.join(protoform[cog].split()[1:])
    if '*' in protoform[cog]:
        w = protoform[cog].split('*')[1]
    else:
       w = ' '.join(protoform[cog].split()[1:])
    w = w.split('/')[0]
    w = w.replace('(','').replace(')','')
    if not len([s for s in list(w) if s in cons])==len(list(w)):
        w = re.sub(r'(.)\1+',r'\1',w)
    w_ = [s for s in list(w) if s in cons]
    coding = '0'
    counter = 0
    for i,s in enumerate(w_):
        if i > 0 and s == w_[i-1]:
            counter += 1
    if counter > 0:
        coding = '1'
    print('\t'.join([cog,protoform[cog],coding]),file=f)
    #print('\t'.join([cog,protoform[cog],coding]))

f.close()