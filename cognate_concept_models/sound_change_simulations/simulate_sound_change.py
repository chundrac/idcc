import os
from collections import defaultdict
import random
import numpy as np
import random
import copy

n_iters = 500

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

ratios = {}
for fn in os.listdir('datasets/'):
    text = [l.strip('\n').split('\t') for l in open('datasets/{}'.format(fn),'r')]
    reflexes = defaultdict(list)
    for l in text[1:]:
        reflexes[l[0]].append(l[2])
    ratios[fn] = defaultdict(list)
    for k in reflexes.keys():
        lang = k
        words = reflexes[k]
        lang_segs = sorted(set([s for w in words for s in w.split()]))
        lang_cons_ = lang_segs
        #lang_cons_.pop(lang_cons_.index('#'))
        #lang_cons_.pop(lang_cons_.index('$'))
        lang_changes = [c for c in changelist if len([s for s in lang_cons_ if s in c['changes'].keys()]) > 0]
        condition = ''
        for t in range(n_iters):
            words_new = copy.copy(words)
            change_curr = random.sample(lang_changes,1)[0]
            print(change_curr)
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
            #ratios[fn][lang].append(len(plus_to_minus)+.001/(len(minus_to_plus)+.001))
            ratios[fn][lang].append([str(t),str(len(plus_to_minus)),str(len(minus_to_plus)),'|'.join([words[i]+'>'+words_new[i] for i in range(len(words)) if detectIDCC(words[i]) != detectIDCC(words_new[i])]),str(change_curr),condition])

#text = [['family','lang','mean']]
#for fam in ratios.keys():
#    for k in ratios[fam].keys():
#        text.append([fam_key[fam],k,str(np.mean(ratios[fam][k]))])

text = [['family','lang','iteration','plus_to_minus','minus_to_plus','mutations','change','environment']]
for fam in ratios.keys():
    for k in ratios[fam].keys():
        for l in ratios[fam][k]:
            text.append([fam_key[fam],k]+l)

f = open('sound_change_simulations.tsv','w')
for l in text:
    print('\t'.join(l),file=f)

f.close()

