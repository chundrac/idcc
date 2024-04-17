#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import re
import numpy as np
import random
import os
import copy

n_iters = 500

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
    text[i].append(' '.join(w___))
    newsegs += w___

newsegs = sorted(set(newsegs))

#cons = ['b', 'bb', 'bbʷ', 'bʷ', 'bˀ', 'bˁ', 'ḇ', 'bᵂ', 'd', 'dd', 'dˀ', 'dˁ', 'f', 'ff', 'fʷ', 'fˀ', 'fˁ', 'g', 'gg', 'ggʷ', 'gʷ', 'gʸ', 'gˀ', 'gˁ', 'g’', 'h', 'hh', 'hʷ', 'ḥ', 'k', 'kk', 'kkʷ', 'kk’', 'kʷ', 'kʸ', 'kˀ', 'k’', 'l', 'll', 'llˀ', 'lʼ', 'lʼˁ', 'lˀ', 'lˁ', 'm', 'mm', 'mmˁ', 'mʷ', 'mˀ', 'mˁ', 'm̠', 'm̱', 'm̲', 'm̲ˀ', 'n', 'nn', 'nˀ', 'nˁ', 'ñ', 'n̄', 'p', 'pp', 'pʷ', 'pˀ', 'pˁ', 'q', 'qq', 'qˁ', 'r', 'rr', 'rˀ', 'rˁ', 's', 'ss', 'sʷ', 'sˀ', 'sˁ', 's̀', 's̃', 'ṣ', 't', 'tt', 'tˁ', 'ṯ', 'w', 'ww', 'wˀ', 'wˁ', 'x', 'xʷ', 'y', 'yy', 'yʰ', 'yˀ', 'yˁ', 'z', 'zz', 'zˀ', 'zˁ', 'ẑ', 'z̃', 'z͂', 'ñ', 'ññ', 'č', 'čč', 'čč̣' ,'č̣č̣', 'č̣', 'ľ', 'ľľ', 'ň', 'ňň', 'ŝ', 'ŝŝ', 'ŝˀ', 'ŝˁ', 'ṣ̂', 'ṣ̂ˀ', 'ŝᵉ', 'š', 'šš', 'šˀ', 'šˁ', 'ṣ̌', 'ź', 'ž', 'žž', 'ǧ', 'ǯ', 'ǯǯ', 'ǯˀ', 'ǯˁ', 'ǯ', 'ʕ', 'γ', 'γγ', 'х', 'ḇ', 'ḇˀ', 'ḍ', 'ḍˁ', 'ḍḍ', 'ḏ', 'ḏ̣', 'ḥ', 'ḥḥ', 'ḫ', 'ḫʷ', 'ḫḫ', 'ḳ', 'ḳʷ', 'ḳʷˁ', 'ḳʸ', 'ḳˀ', 'ḳˁ', 'ḳ̌', 'ḳ̌ʷ', 'ḳḳ', 'ḳḳʷ', 'ḳ’', 'ḵ', 'ḵʷ', 'ḷ', 'ḷˁ', 'ṗ', 'ṣ', 'ṣˀ', 'ṣˁ', 'ṣ̂', 'ṣ̃', 'ṣ̌', 'ṣṣ', 'ṭ', 'ṭˁ', 'ṭṭ', 'ṯ', 'ṯˀ', 'ṯˁ', 'ṯ̣', 'ṯ̣ˀ', 'ṯ̣ˁ', 'ṯṯ', 'ẑ', 'ẑˁ', 'ẓ̂', 'ẑẑ', 'ẓ̂', 'ẓ̂ˁ']

cons = ["b", "bb", "bbʷ", "bʷ", "bˀ", "bˁ", "ḇ", "bᵂ", "d", "dd", "dˀ", "dˁ", "f", "ff", "fʷ", "fˀ", "fˁ", "g", "gg", "ggʷ", "gʷ", "gʸ", "gˀ", "gˁ", "g’", "h", "hh", "hʷ", "ḥ", "k", "kk", "kkʷ", "kk’", "kʷ", "kʸ", "kˀ", "k’", "l", "ll", "llˀ", "lʼ", "lʼˁ", "lˀ", "lˁ", "m", "mm", "mmˁ", "mʷ", "mˀ", "mˁ", "m̠", "m̱", "m̲", "m̲ˀ", "n", "nn", "nˀ", "nˁ", "ñ", "ññ", "n̄n̄", "p", "pp", "pʷ", "pˀ", "pˁ", "q", "qq", "qˁ", "r", "rr", "rˀ", "rˁ", "s", "ss", "sʷ", "sˀ", "sˁ", "s̀", "s̃", "ṣ", "t", "tt", "tˁ", "ṯ", "w", "ww", "wˀ", "wˁ", "x", "xʷ", "y", "yy", "yʰ", "yˀ", "yˁ", "z", "zz", "zˀ", "zˁ", "zˁzˁ", "ẑ", "z̃", "z͂", "ñ", "ññ", "č", "čč", "čč̣", "č̣", "č̣č̣", "ľ", "ľľ", "ň", "ňň", "ŝ", "ŝŝ", "ŝˀ", "ŝˁ", "ṣ̂", "ṣ̂ṣ̂", "ṣ̂ˀ", "ŝᵉ", "š", "šš", "šˀ", "šˁ", "ṣ̌", "ź", "ž", "žž", "ǧ", "ǯ", "ǯǯ", "ǯˀ", "ǯˁ", "ǯ", "ʕ", "γ", "γγ", "х", "ḇ", "ḇˀ", "ḍ", "ḍˁ", "ḍḍ", "ḏ", "ḏ̣", "ḏ̣ḏ̣", "ḥ", "ḥḥ", "ḫ", "ḫʷ", "ḫḫ", "ḳ", "ḳʷ", "ḳʷˁ", "ḳʸ", "ḳˀ", "ḳˁ", "ḳ̌", "ḳ̌ʷ", "ḳḳ", "ḳḳʷ", "ḳ’", "ḵ", "ḵʷ", "ḷ", "ḷˁ", "ṗ", "ṣ", "ṣˀ", "ṣˁ", "ṣ̂", "ṣ̃", "ṣ̌", "ṣṣ", "ṭ", "ṭˁ", "ṭṭ", "ṯ", "ṯˀ", "ṯˁ", "ṯ̣", "ṯ̣ˀ", "ṯ̣ˁ", "ṯṯ", "ẑ", "ẑˁ", "ẓ̂", "ẑẑ", "ẓ̂", "ẓ̂ˁ"]

#deal with cases where citation form is a consonantal root, and C1C1 is not a geminate

for i,l in enumerate(text):
    form = l[8].split()
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
          text[i][8] = ' '.join(w__)
    if l[7] == l[6].strip('-').split('-')[0]:
        text[i][8] = '# '+text[i][8]
    if l[7] == l[6].strip('-').split('-')[-1]:
        text[i][8] = text[i][8]+' $'

reflexes = defaultdict(list)
for l in text:
    reflexes[l[3]].append(l[8])

reflexes = {k:reflexes[k] for k in reflexes.keys() if len(reflexes[k]) > 500}

changes = [l.strip('\n').split('\t') for l in open('selected_konsonantenwandel_changes.tsv','r')]

changelist = {}
for l in changes:
    if l[0] not in changelist.keys():
        changelist[l[0]] = {}
    if 'env' not in changelist[l[0]].keys():
        changelist[l[0]]['env'] = l[1]
    if 'changes' not in changelist[l[0]].keys():
        changelist[l[0]]['changes'] = {}
    if l[3] == '0':
        l[3] = ''
    changelist[l[0]]['changes'][l[2]] = l[3]

changelist = list(changelist.values())

replacer = [l.strip('\n').split('\t') for l in open('segment_replacer.tsv','r')]
replacer = {l[0]:l[1] for l in replacer}

cons = sorted(set(cons+list(replacer.keys())+[v for s in changelist for v in s['changes'].values()]+[v for s in changelist for v in s['changes'].keys()]))

cons.pop(cons.index(''))

def detectIDCC(w):
    w_ = re.sub(r'(.)[\s]*\1+',r'\1',w)
    w_ = ' '.join([s for s in w_.split() if s in cons])
    w_ = re.sub(r'(.)\1+',r'\1',w_)
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
for lang in reflexes.keys():
    words = reflexes[lang]
    lang_segs = sorted(set([s for w in words for s in w.split()]))
    lang_cons_ = [replacer[s] for s in lang_segs if s in replacer.keys()]
    lang_changes = [c for c in changelist if len([s for s in lang_cons_ if s in c['changes'].keys()]) > 0]
    condition = ''
    for t in range(n_iters):
        print(lang,t)
        words_new = copy.copy(words)
        change_curr = random.sample(lang_changes,1)[0]
        if change_curr['env'] == '_':
            condition = 'free'
        if change_curr['env'] in ['_V', 'C_', 'V_C', '_C', 'V_', 'V_V']:
            condition = 'medial'
        if change_curr['env'] in ['V_#', '_#']:
            condition = 'final'
        if change_curr['env'] == '#_':
            condition = 'initial'
        if condition == 'free':
            for seg in change_curr['changes'].keys():
                words_new = [w.replace(seg,change_curr['changes'][seg]) for w in words_new]
        if condition == 'medial':
            for seg in change_curr['changes'].keys():
                words_new = [w.replace('# ','#').replace(' $','$').replace(' '+seg+' ',' '+change_curr['changes'][seg]+' ').replace('#','# ').replace('$',' $') for w in words_new]
        if condition == 'final':
            for seg in change_curr['changes'].keys():
                words_new = [w.replace(' $','$').replace(seg+'$',change_curr['changes'][seg]+'$').replace('$',' $') for w in words_new]
        if condition == 'initial':
            for seg in change_curr['changes'].keys():
                words_new = [w.replace('# ','#').replace('#'+seg,'#'+change_curr['changes'][seg]).replace('#','# ') for w in words_new]
        #print([(words[i],words_new[i]) for i in range(len(words)) if words[i] != words_new[i]])
        #print([(words[i],words_new[i]) for i in range(len(words)) if detectIDCC(words[i]) != detectIDCC(words_new[i])])
        IDCC_before = [detectIDCC(w) for w in words]
        IDCC_after = [detectIDCC(w) for w in words_new]
        plus_to_minus = [i for i in range(len(IDCC_before)) if IDCC_before[i] == 1 and IDCC_after[i] == 0]
        minus_to_plus = [i for i in range(len(IDCC_before)) if IDCC_before[i] == 0 and IDCC_after[i] == 1]
        #print(plus_to_minus,minus_to_plus)
        #ratios[lang].append(len(plus_to_minus)+.001/(len(minus_to_plus)+.001))
        ratios[lang].append([str(t),str(len(plus_to_minus)),str(len(minus_to_plus)),'|'.join([words[i]+'>'+words_new[i] for i in range(len(words)) if detectIDCC(words[i]) != detectIDCC(words_new[i])]),str(change_curr),condition])

#text = [['Semitic',key,str(np.mean(ratios[key]))] for key in ratios.keys()]

text = []
for lang in ratios.keys():
    for l in ratios[lang]:
        text.append(['Semitic',lang]+l)

if 'sound_change_simulations.tsv' not in os.listdir('../../cognate_models/'):
    f = open('../../cognate_models/sound_change_simulations.tsv','w')
    text = [['family','lang','iteration','plus_to_minus','minus_to_plus','mutations','change','environment']]+text
    for l in text:
        print('\t'.join(l),file=f)
    f.close()
else:
    f = open('../../cognate_models/sound_change_simulations.tsv','a')
    for l in text:
        print('\t'.join(l),file=f)
    f.close()

