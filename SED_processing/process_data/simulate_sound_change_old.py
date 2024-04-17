#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import re
import numpy as np
import random
import os

random.seed(1234)

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

reflexes = defaultdict(list)
for l in text:
    reflexes[l[3]].append(' '.join(['#']+[s for s in l[7].split() if s in cons]))


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

text = [['Semitic',key,str(np.mean(ratios[key]))] for key in ratios.keys()]

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