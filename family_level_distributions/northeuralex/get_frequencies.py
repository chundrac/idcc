from collections import defaultdict
import numpy as np

langs = [l.strip('\n').split(',') for l in open('languages.csv','r')]

text = [l.strip('\n').split('\t') for l in open('northeuralex_merged.tsv','r')]

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

IDCC = defaultdict()

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


{k:[(1-np.mean(v))/np.mean(v) for v in IDCC[k].values()] for k in IDCC.keys()}

{k:np.median([(1-np.mean(v))/np.mean(v) for v in IDCC[k].values()]) for k in IDCC.keys()}