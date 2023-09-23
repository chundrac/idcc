# -*- coding: utf-8 -*-

import ipatok
from collections import defaultdict
import numpy as np

###STEDT stuff
###
###

text = [l.strip('\n').split('\t') for l in open('STEDT/processed_data.tsv','r')]

unigrams = []
bigrams = []
trigrams = []

for l in text:
    w = l[0]
    w = ipatok.tokenise(w,replace=True)
    for s in w:
        unigrams.append(s)
    for i in range(len(w)-1):
        bigrams.append(tuple(w[i:i+2]))
    for i in range(len(w)-2):
        trigrams.append(tuple(w[i:i+3]))


unigrams = sorted(set(unigrams))
bigrams = sorted(set(bigrams))
trigrams = sorted(set(trigrams))

ngrams = [
    ('t', 'ɕ', 'h'),
    ('t', 'ʂ', 'h'),
    ('t', 'ʃ', 'h'),
    ('t', 's', 'h'),
    ('d', 'z', 'h'),
    ('b', 'h'),
    ('c', 'h'),
    ('d', 'h'),
    ('k', 'h'),
    ('p', 'h'),
    ('t', 'h'),
    ('ṭ', 'h'),
    ('t̥', 'h'),
    ('ɡ', 'h'),
    ('t', 'sʰ')
]

for i,l in enumerate(text):
    w = l[0]
    w = ipatok.tokenise(w,replace=True)
    w = ' '.join(w)
    for ngram in ngrams:
        w = w.replace(' '.join(ngram),''.join(ngram))
    text[i].append(w)

cons = ['C', 'D','F', 'G','J', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Wː', 'X', 'Y', 'Z', 'b', 'bʼ', 'bˤ', 'b̥', 'c', 'cʰ', 'd', 'dʼ', 'dˤ', 'ḍ', 'f', 'h', 'hʼ', 'hˍ', 'h˜', 'j', 'jː', 'k', 'kʰ', 'kʰˤ', 'kʷ', 'kʷʰ', 'kʷʰˤ', 'kʷˤ', 'kʼ', 'kˍ', 'kˤ', 'l', 'lʼ', 'lˍ', 'lː', 'lˤ', 'l̥', 'l̥ˤ', 'm', 'mʼ', 'mˍ', 'mˤ', 'ṁ', 'ṁʼ', 'm̥', 'm̥ˤ', 'm̩', 'n', 'nʼ', 'nˍ', 'nˤ', 'ñ', 'ñʼ', 'ṅ', 'ṇ', 'n̥', 'n̥ˤ', 'n̩', 'p', 'pʰ', 'pʰˤ', 'pʼ', 'pˍ', 'pː', 'pˤ', 'p̃', 'q', 'qʰ', 'qʰˤ', 'qʷ', 'qʷʰ', 'qʷʰˤ', 'qʷˤ', 'qˤ', 'qˤʰ', 'r', 'r^', 'rʼ', 'rˍ', 'rˤ', 'r̥', 'r̥ˤ', 'r̥̥ˤ', 's', 'sʰ', 'sʰˤ', 'sʼ', 'sˍ', 'sː', 'sˤ', 'ṣ', 't', 'tʰ', 'tʰˤ', 'tʼ', 'tˍ', 'tː', 'tˤ', 'ṭ', 't̥', 'v', 'v̩', 'w', 'x', 'xˤ', 'z', 'zˤ', 'ç', 'ŋ', 'ŋʷ', 'ŋʷˤ', 'ŋʼ', 'ŋˍ', 'ŋˤ', 'ŋ̇', 'ŋ̊', 'ŋ̊ˤ', 'ȵ', 'ȵ̥', 'ȶ', 'ɕ', 'ɕʰ', 'ɟ', 'ɡ', 'ɡʷ', 'ɡʷˤ', 'ɡʼ', 'ɡː', 'ɡˤ', 'ɢ', 'ɢʷ', 'ɢʷˤ', 'ɢˤ', 'ɣ', 'ɤ', 'ɤ̃', 'ɦ', 'ɬ', 'ɮ', 'ɱ', 'ɲ', 'ɲ̇', 'ɲ̊', 'ɳ', 'ɴ', 'ɸ', 'ɹ', 'ɾ', 'ɿ', 'ʁ', 'ʂ', 'ʂʰ', 'ʂ̩', 'ʃ', 'ʈ', 'ʐ', 'ʑ', 'ʑ̩', 'ʒ', 'ʔ', 'ʔʷˤ', 'ʔˍ', 'ʔˤ', 'ʼ', 'ˑ', 'ˤ', '̃', 'β', 'θ', 'χ']

cons += [''.join(ngram) for ngram in ngrams]

for j,l in enumerate(text):
    w = l[2].split()
    w_ = [w[0]]
    for i in range(1,len(w)):
        if w[i] != w[i-1]:
            w_.append(w[i])
    w_ = [s for s in w_ if s in cons]
    counter = 0
    for i in range(1,len(w_)):
        if w_[i] == w_[i-1]:
            counter += 1
    if counter > 0:
        text[j].append('1')
    else:
        text[j].append('0')

langcounts = defaultdict(int)
for l in text:
    langcounts[l[1]] += 1

IDCC = defaultdict()

IDCC['Sino-Tibetan'] = defaultdict(list)

for l in text:
    if langcounts[l[1]] > 1000:
        IDCC['Sino-Tibetan'][l[1]].append(int(l[3]))

###NorthEuraLex stuff
###
###

langs = [l.strip('\n').split(',') for l in open('northeuralex/languages.csv','r')]

text = [l.strip('\n').split('\t') for l in open('northeuralex/northeuralex_merged.tsv','r')]

families = defaultdict(list)
family_ID = {}

for l in langs[1:]:
    families[l[3]].append(l[1])
    family_ID[l[1]] = l[3]

segs = []
for l in text[1:]:
    if l[2] in families['Indo-European'] or l[2] in families['Turkic'] or l[2] in families['Dravidian']:
        w = l[5].split()
        for s in w:
            segs.append(s)


segs = sorted(set(segs))

cons = ['_', 'b', 'bʰ', 'bʲ', 'bʼ', 'bˠ', 'c', 'cʰ', 'c͡ç', 'd', 'dʰ', 'dʲ', 'dʼ', 'dˠ', 'd͡z', 'd͡ʑ', 'd͡ʒ', 'f', 'fʲ', 'fˠ', 'h', 'j', 'jˀ', 'j̃', 'k', 'kʰ', 'kʲ', 'kʷ', 'kʼ', 'kʼʷ', 'l', 'lʲ', 'lˀ', 'lˠ', 'm', 'mʲ', 'mʼ', 'mˀ', 'mˠ', 'n', 'nʲ', 'nˀ', 'nˠ', 'p', 'pʰ', 'pʲ', 'pʼ', 'pˠ', 'p͡f', 'q', 'qʷ', 'r', 'rʲ', 'rʼ', 's', 'sʲ', 'sˠ', 't', 'tʰ', 'tʲ', 'tʼ', 'tˠ', 't͡s', 't͡ɕ', 't͡ʃ', 'v', 'vʲ', 'vˠ', 'w', 'wˀ', 'x', 'y', 'ỹ', 'z', 'zʲ', 'zʼ', 'ç', 'ð', 'ðˀ', 'ŋ', 'ŋˀ', 'ɕ', 'ɖ', 'ɖʰ', 'ɖ͡ʐ', 'ɟ', 'ɡ', 'ɡʰ', 'ɡʲ', 'ɡʷ', 'ɡʷ̃', 'ɡˀ', 'ɣ', 'ɥ', 'ɦ', 'ɫ', 'ɬ', 'ɭ', 'ɱ', 'ɲ', 'ɳ', 'ɴ', 'ɹ', 'ɺ', 'ɽ', 'ɽʰ', 'ɾ', 'ɾʲ', 'ɾˠ', 'ʀ', 'ʀˀ', 'ʁ', 'ʁʷ', 'ʁˀ', 'ʂ', 'ʃ', 'ʃʲ', 'ʈ', 'ʈʰ', 'ʈ͡ʂ', 'ʋ', 'ʋʲ', 'ʎ', 'ʐ', 'ʑ', 'ʒ', 'ʒʲ', 'ʔ', 'ʘ', 'ʝ', 'β', 'θ', 'χ', 'χʷ']

IDCC['Indo-European'] = defaultdict(list)
IDCC['Turkic'] = defaultdict(list)
IDCC['Dravidian'] = defaultdict(list)

for l in text[1:]:
    if l[2] in families['Indo-European'] or l[2] in families['Turkic'] or l[2] in families['Dravidian']:
      if l[5] != '':
        w = l[5].split()
        w_ = [w[0]]
        for i,s in enumerate(w):
            if i > 0 and s != w[i-1] and s in cons:
                w_.append(s)
        counter = 0
        for i in range(1,len(w_)):
            if w_[i] == w_[i-1]:
                counter += 1
        if counter > 0:
            IDCC[family_ID[l[2]]][l[2]].append(1)
        else:
            IDCC[family_ID[l[2]]][l[2]].append(0)


UtoAztecan = defaultdict(list)

text = [l.strip('\n') for l in open('UtoAztecan/Yaqui_wordlist.txt','r')]

UtoAztecan['Yaqui'] = text

text = [l.strip('\n') for l in open('UtoAztecan/Northern_Paiute_wordlist.txt','r')]

UtoAztecan['Paiute'] = text

text = [l.strip('\n') for l in open('UtoAztecan/Nahuatl_wordlist.txt','r')]

UtoAztecan['Nahuatl'] = text

text = [[k,s] for k in UtoAztecan.keys() for s in UtoAztecan[k]]

unigrams = []
bigrams = []
trigrams = []

for l in text:
    w = l[1]
    w = ipatok.tokenise(w,replace=True)
    for s in w:
        unigrams.append(s)
    for i in range(len(w)-1):
        bigrams.append(tuple(w[i:i+2]))
    for i in range(len(w)-2):
        trigrams.append(tuple(w[i:i+3]))

unigrams = sorted(set(unigrams))
bigrams = sorted(set(bigrams))
trigrams = sorted(set(trigrams))

ngrams = [
    ('t', 's'),
    ('c', 'h'),
    ('d', 'z')
]

segs = []
for i,l in enumerate(text):
    w = l[1]
    w = ipatok.tokenise(w.replace('-','Q'),replace=False)
    w = ' '.join(w)
    for ngram in ngrams:
        w = w.replace(' '.join(ngram),''.join(ngram))
    w = w.replace('Q','-')
    segs += w.split()
    text[i].append(w)

segs = sorted(set(segs))

cons = ['B', 'D', 'H', 'K', 'M', 'N', 'P', 'S', 'T', 'W', 'Y', 'b', 'c', 'ch', 'c̷', 'd', 'dz', 'h', 'j', 'k', 'kʷ', 'l', 'm', 'n', 'p', 'pʷ', 'r', 's', 't', 'ts', 'w', 'y', 'z', 'ɡ', 'ʼ', 'β', '-']

for j,l in enumerate(text):
    w = l[2].split()
    w_ = [w[0]]
    for i in range(1,len(w)):
        if w[i] != w[i-1]:
            w_.append(w[i])
    w_ = [s for s in w_ if s in cons]
    counter = 0
    for i in range(1,len(w_)):
        if w_[i] == w_[i-1]:
            counter += 1
    if counter > 0:
        text[j].append('1')
    else:
        text[j].append('0')

IDCC['Uto-Aztecan'] = defaultdict(list)

for l in text:
    IDCC['Uto-Aztecan'][l[0]].append(int(l[3]))

longform = [['Family','Language','IDCC','NoIDCC']]

for fam in IDCC.keys():
    for lang in IDCC[fam].keys():
        #longform.append([lang,fam,str(np.mean(IDCC[fam][lang]))])
        longform.append([fam,lang,str(IDCC[fam][lang].count(1)),str(IDCC[fam][lang].count(0))])

f = open('IDCC_counts_by_family.tsv','w')
for l in longform:
    print('\t'.join(l),file=f)

f.close()