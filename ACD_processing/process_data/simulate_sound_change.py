from collections import defaultdict
import re
import unicodedata
import numpy as np
import random
import os
import copy

n_iters = 500

random.seed(1234)

digraphs = ['b h', 'c h', 'd h', 'g h', 'j h', 'k h', 'l h', 'm h', 'n h', 'p h', 's h', 't h', 'v h', 'w h', 't s', 'd z']

def normalize_text(w):
    if w != '':
        w_ = list(w)
        w__ = []
        s_ = w_[0]
        for j,s in enumerate(w_):
          if j > 0:
            if s in lig_post or w_[j-1] == s or w_[j-1] in lig_pre:
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
        w___ = [re.sub(r'(.)\1+',r'\1',s) for s in w___]
        w___ = ' '.join(w___)
        for s in digraphs:
            w___ = w___.replace(s,s.replace(' ',''))
        return(w___)
    else:
        return(w)

"""N.B.: this script notes tautomorphemic IC, but not heteromorphemic"""

taxa = [l.strip('\n') for l in open('taxa_to_use.txt','r')]

"""Load the data:"""

acd = [l.strip('\n').split('\t') for l in open('acd_merged_reflex_aligned.tsv','r')]
acd = [l[1:] for l in acd]
acd = list(set([tuple(l) for l in acd]))
acd = [list(l) for l in acd]
acd = [l for l in acd if l[1] in taxa]

segs = sorted(set([s for l in acd for s in list(l[10])]))

lig_pre = ['ᵐ']

lig_post = ['ʰ', 'ʷ', 'ʸ']

for i,l in enumerate(acd):
    acd[i][9] = normalize_text(l[9])
    acd[i][10] = normalize_text(l[10])
    acd[i][11] = normalize_text(l[11])

protoform = {}
for l in acd:
    protoform[l[0]] = l[5]+' '+l[4]

formdict = defaultdict(list)

for l in acd:
    etym_id = l[0]
    lang = l[1]
    word_id = l[6]
    citation_form = l[9]
    aligned_word = l[10]
    gloss = l[3]
    aligned_morph = l[11]
    #get rid of geminates
    aligned_word = re.sub(r'(.)\1+',r'\1',citation_form)
    aligned_morph = re.sub(r'(.)\1+',r'\1',aligned_morph)
    formdict[(etym_id,lang)].append((word_id,aligned_word,gloss,aligned_morph,citation_form))

cons = ['C', 'D', 'G', 'H', 'K', 'L', 'M', 'N', 'R', 'S', 'T', 'V', 'X', 'Z', 'b', 'bh', 'bʰ', 'bʷ', 'c', 'ch', 'd', 'dh', 'dʰ', 'f', 'g', 'gh', 'gʰ', 'h', 'j', 'jh', 'k', 'kh', 'kʷ', 'kʸ', 'l', 'lh', 'lʸ', 'm', 'mh', 'mʷ', 'mʷmʷ', 'n', 'nh', 'p', 'ph', 'pʰ', 'pʷ', 'q', 'r', 's', 'sh', 't', 'th', 'tʰ', 'v', 'vh', 'w', 'wh', 'x', 'y', 'z', 'ð', 'ñ', 'č', 'đ', 'ń', 'ŋ', 'ŕ', 'ƀ', 'ƚ', 'ǥ', 'Ɂ', 'ɓ', 'ɖ', 'ɗ', 'ɣ', 'ɫ', 'ɬ', 'ɭ', 'ɮ', 'ʃ', 'ʄ', 'ʈ', 'ʔ', 'β', 'γ', 'θ', 'ϕ', 'ᵐb', 'ḍ', 'ḱ', 'ḷ', 'ṇ', 'ṕ', 'ṛ', 'ṭ']

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

#langs with more than 500 reflexes
langs = ['java1254', 'amis1246', 'iban1264', 'pamo1252', 'niue1239', 'mong1342', 'ilok1237', 'mang1405', 'mala1479', 'sasa1249', 'ivat1242', 'cala1258', 'renn1242', 'sund1252', 'sang1336', 'cebu1242', 'taga1270', 'ngaj1237', 'pamp1243', 'binu1244', 'meri1243', 'isna1241', 'hanu1241', 'taus1251', 'maka1311', 'mara1404', 'samo1305', 'maor1246', 'puyu1239', 'thao1240', 'gela1263', 'bata1289', 'kela1258', 'tont1239', 'mans1262', 'saaa1240', 'west2555', 'casi1235', 'pang1290', 'ibal1244', 'paiw1248', 'bont1247', 'tong1325', 'kava1241']

def detectIDCC(w):
    w_ = w.split()
    counter = 0
    for i,s in enumerate(w_):
        if i > 0 and s == w_[i-1]:
            counter += 1
    if counter > 0:
        return(1)
    else:
        return(0)

ratios = defaultdict(list)
for lang in langs:
    df_ = [l for l in acd if l[1] == lang]
    formdict = defaultdict(list)
    for l in df_:
        etym_id = l[0]
        lang = l[1]
        word_id = l[6]
        citation_form = l[9]
        aligned_word = l[10]
        gloss = l[3]
        aligned_morph = l[11]
        #get rid of geminates
        aligned_word = re.sub(r'(.)\1+',r'\1',citation_form)
        aligned_morph = re.sub(r'(.)\1+',r'\1',aligned_morph)
        formdict[(etym_id,lang)].append((word_id,aligned_word,gloss,aligned_morph,citation_form))
    stringdict = defaultdict(list)
    for k in formdict.keys():
        if len(formdict[k]) > 1:
            strings = []
            for v in formdict[k]:
                #normalize and strip affixes/infixes off of full word form
                w = v[1]
                w = unicodedata.normalize('NFD',w).replace('́','')
                w = re.sub('<.*>','',w)
                w = w.replace('- ','').replace('   ',' ')
                w = re.sub(r'(. )\1+',r'\1',w) #get rid of identical consonants within and across hyphens
                strings.append(w.split())
            morphs = []
            for v in formdict[k]:
                w = v[3]
                w = unicodedata.normalize('NFD',w).replace('́','')
                w = re.sub('<.*>','',w)
                #collect all consonants (geminates already removed)
                morphs.append(' '.join([s for s in w.split() if s in cons]))
            morphs = set(morphs)
            words = [v[1] for v in formdict[k]]
            substr = defaultdict(list)
            for l,string in enumerate(strings):
                string_ = ['#']+[s for s in string if s in cons]+['$']
                for i in range(len(string_)):
                    for j in range(i,len(string_)):
                        substr[' '.join(string_[i:j+1])].append(l)
            for key in substr.keys():
                substr[key] = sorted(set(substr[key]))
            substr_ = sorted([k for k in substr.keys() if substr[k] == list(range(len(strings)))],key=lambda x:len(x))
            substr_ = [s for s in substr_ if s != '#' and s != '$']
            if substr_ != []:
                longest = substr_[-1]
                for v in formdict[k]:
                    stringdict[k].append(longest)
            else:
                stringdict[k] += list(morphs)
        else:
            w = formdict[k][0][1]
            #w = re.sub(r'(.)\1+',r'\1',w)
            longest = ' '.join([s for s in w.split() if s in cons])
            stringdict[k].append(longest)
    stringdict_orig = stringdict
    IDCC_before = []
    for key in stringdict_orig.keys():
        counter = 0
        for w in stringdict_orig[key]:
            if detectIDCC(w) == 1:
                counter = 1
        IDCC_before.append(counter)
    lang_segs = sorted(set([s for l in df_ for s in l[9].split()]))
    lang_cons = [replacer[s] for s in lang_segs if s in replacer.keys()]
    lang_changes = [c for c in changelist if len([s for s in lang_cons if s in c['changes'].keys()]) > 0]
    condition = ''
    for t in range(n_iters):
        print(lang,t)
        df__ = copy.deepcopy(df_)
        #track word boundaries in aligned morpheme
        for i,l in enumerate(df__):
            new_word = l[9]
            new_morph = l[11]
            if l[11] == l[9].split(' - ')[0]:
                new_morph = '# '+new_morph
            if l[11] == l[9].split(' - ')[-1]:
                new_morph = new_morph+' $'
            new_word = '# '+new_word+' $'
            for key in replacer.keys():
                new_word = new_word.replace(key,replacer[key])
                new_morph = new_morph.replace(key,replacer[key])
            df__[i][9] = new_word
            df__[i][11] = new_morph
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
            for i,l in enumerate(df__):
                #print(condition)
                #print(l[9])
                for seg in change_curr['changes'].keys():
                    if seg in l[9]:
                        df__[i][9] = l[9].replace(seg,change_curr['changes'][seg])
                        df__[i][11] = l[11].replace(seg,change_curr['changes'][seg])
                #print(l[9])
        if condition == 'medial':
            for i,l in enumerate(df__):
                #print(condition)
                #print(l[9])
                for seg in change_curr['changes'].keys():
                    if seg in l[9]:
                        df__[i][9] = l[9].replace('# ','#').replace(' $','$').replace(' '+seg+' ',' '+change_curr['changes'][seg]+' ').replace('#','# ').replace('$',' $')
                        df__[i][11] = l[11].replace('# ','#').replace(' $','$').replace(' '+seg+' ',' '+change_curr['changes'][seg]+' ').replace('#','# ').replace('$',' $')
                #print(l[9])
        if condition == 'final':
            for i,l in enumerate(df__):
                #print(condition)
                #print(l[9])
                for seg in change_curr['changes'].keys():
                    if seg in l[9]:
                        df__[i][9] = l[9].replace(' $','$').replace(seg+'$',change_curr['changes'][seg]+'$').replace('$',' $')
                        df__[i][11] = l[11].replace(' $','$').replace(seg+'$',change_curr['changes'][seg]+'$').replace('$',' $')
                #print(l[9])
        if condition == 'initial':
            for i,l in enumerate(df__):
                #print(condition)
                #print(l[9])
                for seg in change_curr['changes'].keys():
                    if seg in l[9]:
                        df__[i][9] = l[9].replace('# ','#').replace('#'+seg,'#'+change_curr['changes'][seg]).replace('#','# ')
                        df__[i][11] = l[11].replace('# ','#').replace('#'+seg,'#'+change_curr['changes'][seg]).replace('#','# ')
                #print(l[9])
        for i,l in enumerate(df__):
            df__[i][9] = l[9].replace('# ','').replace(' $','')
            df__[i][11] = l[11].replace('# ','').replace(' $','')
        formdict = defaultdict(list)
        for l in df__:
            etym_id = l[0]
            lang = l[1]
            word_id = l[6]
            citation_form = l[9]
            aligned_word = l[10]
            gloss = l[3]
            aligned_morph = l[11]
            #get rid of geminates
            aligned_word = re.sub(r'(.)\1+',r'\1',citation_form)
            aligned_morph = re.sub(r'(.)\1+',r'\1',aligned_morph)
            formdict[(etym_id,lang)].append((word_id,aligned_word,gloss,aligned_morph,citation_form))
        stringdict = defaultdict(list)
        for k in formdict.keys():
            if len(formdict[k]) > 1:
                strings = []
                for v in formdict[k]:
                    #normalize and strip affixes/infixes off of full word form
                    w = v[1]
                    w = unicodedata.normalize('NFD',w).replace('́','')
                    w = re.sub('<.*>','',w)
                    w = w.replace('- ','').replace('   ',' ')
                    w = re.sub(r'(. )\1+',r'\1',w) #get rid of identical consonants within and across hyphens
                    strings.append(w.split())
                morphs = []
                for v in formdict[k]:
                    w = v[3]
                    w = unicodedata.normalize('NFD',w).replace('́','')
                    w = re.sub('<.*>','',w)
                    #collect all consonants (geminates already removed)
                    morphs.append(' '.join([s for s in w.split() if s in cons]))
                morphs = set(morphs)
                words = [v[1] for v in formdict[k]]
                substr = defaultdict(list)
                for l,string in enumerate(strings):
                    string_ = ['#']+[s for s in string if s in cons]+['$']
                    for i in range(len(string_)):
                        for j in range(i,len(string_)):
                            substr[' '.join(string_[i:j+1])].append(l)
                for key in substr.keys():
                    substr[key] = sorted(set(substr[key]))
                substr_ = sorted([k for k in substr.keys() if substr[k] == list(range(len(strings)))],key=lambda x:len(x))
                substr_ = [s for s in substr_ if s != '#' and s != '$']
                if substr_ != []:
                    longest = substr_[-1]
                    for v in formdict[k]:
                        stringdict[k].append(longest)
                else:
                    stringdict[k] += list(morphs)
            else:
                w = formdict[k][0][1]
                #w = re.sub(r'(.)\1+',r'\1',w)
                longest = ' '.join([s for s in w.split() if s in cons])
                stringdict[k].append(longest)
        IDCC_after = []
        for key in stringdict.keys():
            counter = 0
            for w in stringdict[key]:
                if detectIDCC(w) == 1:
                    counter = 1
            IDCC_after.append(counter)
        plus_to_minus = [i for i in range(len(IDCC_before)) if IDCC_before[i] == 1 and IDCC_after[i] == 0]
        minus_to_plus = [i for i in range(len(IDCC_before)) if IDCC_before[i] == 0 and IDCC_after[i] == 1]
        #print(plus_to_minus,minus_to_plus)
        #ratios[lang].append(len(plus_to_minus)+.001/(len(minus_to_plus)+.001))
        ratios[lang].append([str(t),str(len(plus_to_minus)),str(len(minus_to_plus)),'',str(change_curr),condition])


#text = [['Austronesian',key,str(np.mean(ratios[key]))] for key in ratios.keys()]

text = []
for lang in ratios.keys():
    for l in ratios[lang]:
            text.append(['Austronesian',lang]+l)

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

