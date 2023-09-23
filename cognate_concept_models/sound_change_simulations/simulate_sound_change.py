import os
from collections import defaultdict
import random
import numpy as np
import random

random.seed(1234)

def detectIDCC(w):
    w_ = w.split(' + ')
    counter = 0
    for w__ in w_:
        ss = w__.split()
        for i,s in enumerate(ss):
            if i > 0 and s == ss[i-1]:
                counter += 1
    if counter > 0:
        return(1)
    else:
        return(0)

fam_key = {
    'dravlex.csv':'Dravidian',
    'dunnielex.csv':'Indo-European',
    'sagartst.csv':'Sino-Tibetan',
    'savelyevturkic.csv':'Turkic',
    'utoaztecan.csv':'Uto-Aztecan'
}

ratios = {}
for fn in os.listdir('datasets/'):
    text = [l.strip('\n').split('\t') for l in open('datasets/{}'.format(fn),'r')]
    reflexes = defaultdict(list)
    for l in text[1:]:
        reflexes[l[0]].append('# '+l[2])
    ratios[fn] = defaultdict(list)
    for k in reflexes.keys():
        lang = k
        words = reflexes[k]
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
            ratios[fn][lang].append(len(plus_to_minus)+.001/(len(minus_to_plus)+.001))

text = [['family','lang','mean']]
for fam in ratios.keys():
    for k in ratios[fam].keys():
        text.append([fam_key[fam],k,str(np.mean(ratios[fam][k]))])

f = open('sound_change_simulations.tsv','w')
for l in text:
    print('\t'.join(l),file=f)

f.close()