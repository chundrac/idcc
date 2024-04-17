import ipatok
from collections import defaultdict
import numpy as np

text = [l.strip('\n').split('\t') for l in open('processed_data.tsv','r')]

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

IDCC = defaultdict(list)
for l in text:
    IDCC[l[1]].append(int(l[3]))

langcounts = defaultdict(int)
for l in text:
    langcounts[l[1]] += 1

{k:(1-np.mean(IDCC[k]))/np.mean(IDCC[k]) for k in IDCC.keys() if langcounts[k] > 1000}