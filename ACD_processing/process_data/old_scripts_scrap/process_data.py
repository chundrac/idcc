from collections import defaultdict
import re
import unicodedata
import numpy as np

"""N.B.: this script notes tautomorphemic IC, but not heteromorphemic"""

taxa = [l.strip('\n') for l in open('taxa_to_use.txt','r')]

"""Load the data:"""

acd = [l.strip('\n').split('\t') for l in open('acd_merged_reflex_aligned.tsv','r')]
acd = [l[1:] for l in acd]
acd = list(set([tuple(l) for l in acd]))
acd = [list(l) for l in acd]
acd = [l for l in acd if l[1] in taxa]

"""We keep track of word IDs that appear to be derived forms as opposed to inherited from an earlier ancestor:"""

root_word = {}
for l in acd:
    root_word[(l[6],l[7],l[8])] = (l[0],l[4],l[5])

root_word = defaultdict(list)
for l in acd:
    root_word[(l[0],l[4],l[5])].append((l[6],l[7],l[8]))

for k in root_word.keys():
    root_word[k] = set(root_word[k])

derived = {}
for k in root_word.keys():
    for v in root_word[k]:
        if ('-' in v[1] or '<' in v[1] or ' ' in v[1]) and v[1] != k[1] and (v[1].count('-') != k[1].count('-') or v[1].count('<') != k[1].count('<') or v[1].count(' ') != k[1].count(' ')):
            derived[v[0]] = '.'.join(['D',v[0],v[2],v[1]])
        else:
            derived[v[0]] = '.'.join(['N',k[0],k[2],k[1]])

formdict = defaultdict(list)

for l in acd[1:]:
    etym_id = l[0]
    lang = l[1]
    word_id = l[6]
    form = l[9]
    gloss = l[3]
    aligned_morph = l[11]
    form = re.sub(r'(.)\1+',r'\1',form)
    aligned_morph = re.sub(r'(.)\1+',r'\1',aligned_morph)
    formdict[(etym_id,lang)].append((word_id,form,gloss,aligned_morph))

cons = ['B', 'C', 'D', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Z', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'ð', 'ñ', 'č', 'đ', 'ń', 'ņ', 'ŋ', 'ŕ', 'š', 'ž', 'ƀ', 'ƚ', 'ǥ', 'ǵ', 'Ɂ', 'ɖ', 'ɗ', 'ɣ', 'ɫ', 'ɬ', 'ɭ', 'ɮ', 'ɸ', 'ʃ', 'ʄ', 'ʈ', 'ʔ', 'ʰ', 'ʷ', 'ʸ', 'β', 'γ', 'θ', 'ϕ', 'ᵇ', 'ᵏ', 'ᵐ', 'ᵬ', 'ḍ', 'ḏ', 'ḱ', 'ḷ', 'ḿ', 'ṁ', 'ṃ', 'ṇ', 'ṕ', 'ṛ', 'ṭ']

stringdict = defaultdict(list)
reflexdict = defaultdict(list)
for k in formdict.keys():
    reflexdict[(derived[formdict[k][0][0]],k[1],formdict[k][0][0])] = [l[-1] for l in formdict[k]]
    if len(formdict[k]) > 1:
        strings = []
        for v in formdict[k]:
            w = v[1]
            w = unicodedata.normalize('NFD',w).replace('́','')
            w = re.sub('<.*>','',w)
            w = w.replace('-','').replace(' ','')
            w = re.sub(r'(.)\1+',r'\1',w) #get rid of identical consonants across hyphens
            strings.append('#'+w+'$')
        morphs = []
        for v in formdict[k]:
            w = v[3]
            w = unicodedata.normalize('NFD',w).replace('́','')
            w = re.sub('<.*>','',w)
            morphs.append(''.join([s for s in re.sub(r'(.)\1+',r'\1',w) if s in cons]))
        morphs = set(morphs)
        words = [v[1] for v in formdict[k]]
        substr = defaultdict(int)
        for string in strings:
            string_ = '#'+''.join([s for s in re.sub(r'(.)\1+',r'\1',string) if s in cons])+'$'
            for i in range(len(string_)):
                for j in range(i,len(string_)):
                    substr[string_[i:j+1]] += 1
        substr_ = sorted([k for k in substr.keys() if substr[k] >= len(strings) and len([m for m in morphs if m in k]) > 0],key=lambda x:len(x))
        if substr_ != []:
            longest = substr_[-1]
            for v in formdict[k]:
                stringdict[(derived[v[0]],k[1],v[0])].append(longest)
        else:
            longest = [''.join([s for s in w if s in cons]) for w in words if '-' not in w and ' ' not in w and '<' not in w]
            for v in formdict[k]:
                stringdict[(derived[v[0]],k[1],v[0])] += longest
    else:
        longest = ''.join([s for s in formdict[k][0][1] if s in cons])
        stringdict[(derived[formdict[k][0][0]],k[1],formdict[k][0][0])].append(longest)

for key in stringdict.keys():
    stringdict[key] = sorted(set(stringdict[key]))

#find the aligned full-word reflex for each record
wordform = {}
for l in acd:
    wordform[(l[1],l[6])] = l[10]

wholerecord = {}
for l in acd:
    wholerecord[(l[1],l[6])] = l[9]

coding = {}
for k in stringdict.keys():
    lang = k[1]
    if lang not in coding.keys():
        coding[lang] = defaultdict(list)
    for w in stringdict[k]:
        val = '0'
        word = wordform[(k[1],k[2])]
        word = re.sub(r'(.)\1+',r'\1',word)
        word = ''.join([s for s in word if s in cons])
        if re.sub(r'(.)\1+',r'\1',word) != word:
            val = 'word'
        if re.sub(r'(.)\1+',r'\1',w) != w:
            val = '1'
        if val == 'word':
            val = '0'
        coding[lang][k[0]].append(val)

#langs_to_keep = [lang for lang in coding.keys() if len(coding[lang].keys()) > 400]
langs_to_keep = [lang for lang in coding.keys() if len(coding[lang].keys()) > 500]

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

#cogs_to_keep = [k for k in coglang.keys() if len(cogvar[k]) > 1 and len(coglang[k])>4]
cogs_to_keep = [k for k in coglang.keys() if len(coglang[k])>L/8]

colnames = ['']
charvalues = []

print(L,len(cogs_to_keep))

coding_str = defaultdict()
for k in reflexdict.keys():
    if k[1] not in coding_str.keys():
        coding_str[k[1]] = defaultdict(list)
    coding_str[k[1]][k[0]] += reflexdict[k]

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

print('\t'.join(['']+[' '.join(s.split('.')[-2:]) for s in cogs_to_keep]),file=f)

for lang in langs_to_keep:
    ll = [lang]
    for cog in cogs_to_keep:
        if cog in coding_str[lang].keys():
            ll.append(', '.join(set(coding_str[lang][cog])))
        else:
            ll.append('')
    print('\t'.join(ll),file=f)

f.close()
