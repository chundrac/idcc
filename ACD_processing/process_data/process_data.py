from collections import defaultdict
import re
import unicodedata
import numpy as np

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

for key in stringdict.keys():
    stringdict[key] = sorted(set(stringdict[key]))

for key in stringdict.keys():
    print(key,formdict[key],stringdict[key])

coding = {}
for k in stringdict.keys():
    lang = k[1]
    etymon = k[0]
    if lang not in coding.keys():
        coding[lang] = defaultdict(list)
    for w in stringdict[k]:
        w_ = w.split()
        val = '0'
        counter = 0
        for i,s in enumerate(w_):
            if i > 0 and s == w_[i-1]:
                counter += 1
        if counter > 0:
            val = '1'
        print (w,val)
        coding[lang][etymon].append(val)

langs_to_keep = [lang for lang in coding.keys() if len(coding[lang].keys()) > 250]

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

cogs_to_keep = [k for k in coglang.keys() if len(coglang[k])>L/10]

colnames = ['']
charvalues = []

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
        if (cog,lang) in formdict.keys():
            form = ', '.join([l[4] for l in formdict[(cog,lang)]])
            ll.append(form)
        else:
            ll.append('')
    print('\t'.join(ll),file=f)

f.close()

f = open('../data/etymon_data.tsv','w')
for cog in cogs_to_keep:
    w = ' '.join(protoform[cog].split()[1:])
    w_ = [s for s in list(w) if s in cons]
    coding = '0'
    counter = 0
    for i,s in enumerate(w_):
        if i > 0 and s == w_[i-1]:
            counter += 1
    if counter > 0:
        coding = '1'
    print('\t'.join([cog,protoform[cog],coding]),file=f)

f.close()