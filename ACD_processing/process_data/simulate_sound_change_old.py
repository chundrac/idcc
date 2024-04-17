from collections import defaultdict
import re
import unicodedata
import numpy as np
import random
import os

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

#cons = ['B', 'C', 'D', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Z', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'ð', 'ñ', 'č', 'đ', 'ń', 'ņ', 'ŋ', 'ŕ', 'š', 'ž', 'ƀ', 'ƚ', 'ǥ', 'ǵ', 'Ɂ', 'ɖ', 'ɗ', 'ɣ', 'ɫ', 'ɬ', 'ɭ', 'ɮ', 'ɸ', 'ʃ', 'ʄ', 'ʈ', 'ʔ', 'ʰ', 'ʷ', 'ʸ', 'β', 'γ', 'θ', 'ϕ', 'ᵇ', 'ᵏ', 'ᵐ', 'ᵬ', 'ḍ', 'ḏ', 'ḱ', 'ḷ', 'ḿ', 'ṁ', 'ṃ', 'ṇ', 'ṕ', 'ṛ', 'ṭ']
cons = ['D', 'G', 'H', 'K', 'L', 'M', 'N', 'R', 'S', 'T', 'V', 'X', 'Z', 'b', 'bh', 'bʰ', 'bʷ', 'c', 'ch', 'd', 'dh', 'dʰ', 'f', 'g', 'gh', 'gʰ', 'h', 'j', 'jh', 'k', 'kh', 'kʷ', 'kʸ', 'l', 'lh', 'lʸ', 'm', 'mh', 'mʷ', 'mʷmʷ', 'n', 'nh', 'p', 'ph', 'pʰ', 'pʷ', 'q', 'r', 's', 'sh', 't', 'th', 'tʰ', 'v', 'vh', 'w', 'wh', 'x', 'y', 'z', 'ð', 'ñ', 'č', 'đ', 'ń', 'ŋ', 'ŕ', 'ƀ', 'ƚ', 'ǥ', 'Ɂ', 'ɓ', 'ɖ', 'ɗ', 'ɣ', 'ɫ', 'ɬ', 'ɭ', 'ɮ', 'ʃ', 'ʄ', 'ʈ', 'ʔ', 'β', 'γ', 'θ', 'ϕ', 'ᵐb', 'ḍ', 'ḱ', 'ḷ', 'ṇ', 'ṕ', 'ṛ', 'ṭ']

cons += ['C']

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

reflexes = defaultdict(list)
for k in stringdict.keys():
    reflexes[k[1]] += stringdict[k]

reflexes = {k:reflexes[k] for k in reflexes.keys() if len(reflexes[k]) > 500}

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

text = [['Austronesian',key,str(np.mean(ratios[key]))] for key in ratios.keys()]

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