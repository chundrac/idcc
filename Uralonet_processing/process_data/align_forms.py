"""This script aligns etyma in Uralonet with the portions of their reflexes most likely to descend from them. In many cases, reflexes consist of multi-word and other expressions of which only a portion descends from the etymon of interest. We use the alignment algorithm of Jäger (2013) to isolate the truly homologous form.

For reflexes displaying variant forms delimited with ', ' or ' ~ ', we split the records into duplicates."""

from collections import defaultdict
import csv
import numpy as np
import re

def EM_segs(lang):
    sub_df = [l for l in acd_data if l[2]==lang]
    segs = sorted(set([s for l in sub_df for s in list(re.sub('\W','',l[3]))]))
    followsegs = segs+['#']
    prevsegs = ['#']+segs
    prev = np.zeros([len(segs),len(followsegs)])
    foll = np.zeros([len(segs),len(followsegs)])
    for l in sub_df:
        w = list(re.sub('\W','',l[3]))+['#']
        for i,s in enumerate(w):
            if i < len(w)-1:
                foll[segs.index(s),followsegs.index(w[i+1])] += 1
        w = ['#']+list(re.sub('\W','',l[3]))
        for i,s in enumerate(w):
            if i > 0:
                prev[segs.index(s),prevsegs.index(w[i-1])] += 1
    K = 2
    curr_z = {}
    pi_prev = {k:np.ones(len(followsegs)) for k in range(K)}
    pi_foll = {k:np.ones(len(prevsegs)) for k in range(K)}
    for s in segs:
        curr_z[s] = np.random.binomial(1,.5)
        pi_prev[curr_z[s]] += prev[segs.index(s),]
        pi_foll[curr_z[s]] += foll[segs.index(s),]
    lliks = []
    idx = np.arange(len(segs))
    for t in range(100):
        np.random.shuffle(idx)
        llik = 0
        for i in idx:
            s = segs[i]
            pi_prev[curr_z[s]] -= prev[segs.index(s),]
            pi_foll[curr_z[s]] -= foll[segs.index(s),]
            p = np.array([np.dot(prev[segs.index(s),],np.log(pi_prev[k]/sum(pi_prev[k]))) + np.dot(foll[segs.index(s),],np.log(pi_foll[k]/sum(pi_foll[k]))) for k in range(K)])
            z = np.argmax(p)
            curr_z[s] = z
            llik += p[z]
            pi_prev[curr_z[s]] += prev[segs.index(s),]
            pi_foll[curr_z[s]] += foll[segs.index(s),]
        lliks.append(llik)
        if t > 0 and llik == lliks[t-1]:
            break
    langsegs[lang] = {}
    counter = 0
    if 'a' in curr_z.keys():
        if curr_z['a'] == 1:
            counter = 1
    elif 'e' in curr_z.keys():
        if curr_z['e'] == 1:
            counter = 1
    for k in curr_z.keys():
        if counter == 1:
            langsegs[lang][k] = abs(curr_z[k]-1)
        else:
            langsegs[lang][k] = curr_z[k]

def init_sim():
    S = {}
    for s in segs:
        for t in segs:
            if s == t:
                S[(s,t)] = 1
            else:
                S[(s,t)] = -1
    return(S)

def gensim(pmi):
    S = {}
    for s in segs:
        for t in segs:
            S[(s,t)] = pmi[(s,t)]
    return(S)

def NW(S,a,b): #needleman wunsch
    d = -5
    m=len(a)
    n=len(b)
    F = np.zeros([m+1,n+1])
#    print F
    for i in range(0,m+1):
        F[i,0] = int(d*i)
    for j in range(0,n+1):
        F[0,j] = int(d*j)
#    print F
    for i in range(1,m+1):
        for j in range(1,n+1):
#            print i,j
            match = F[i-1,j-1] + S[(a[i-1],b[j-1])]
            delete = F[i-1,j] + d
            insert = F[i,j-1] + d
#            print max(match,delete,insert)
            F[i,j] = max(match,delete,insert)
#    print F
    alignA = []
    alignB = []
    i = m
    j = n
    while i > 0 or j > 0:
#        print alignA,alignB
        if i > 0 and j > 0 and F[i,j] == F[i-1,j-1] + S[(a[i-1],b[j-1])]:
            alignA.insert(0,a[i-1])
            alignB.insert(0,b[j-1])
            i,j = i-1,j-1
        elif i > 0 and F[i,j] == F[i-1,j] + d:
            alignA.insert(0,a[i-1])
            alignB.insert(0,'-')
            i = i-1
        else:
            alignA.insert(0,'-')
            alignB.insert(0,b[j-1])
            j = j-1
    return(tuple(alignA),tuple(alignB))

def NWscore(S,a,b): #needleman wunsch score
    """align string a with string b on the basis of similarity values in S"""
    d = -5
    m=len(a)
    n=len(b)
    F = np.zeros([m+1,n+1])
    for i in range(0,m+1):
        F[i,0] = int(d*i)
    for j in range(0,n+1):
        F[0,j] = int(d*j)
    for i in range(1,m+1):
        for j in range(1,n+1):
            match = F[i-1,j-1] + S[(a[i-1],b[j-1])]
            delete = F[i-1,j] + d
            insert = F[i,j-1] + d
            F[i,j] = max(match,delete,insert)
    alignA = []
    alignB = []
    i = m
    j = n
    score = F[i,j]
    while i > 0 or j > 0:
        if i > 0 and j > 0 and F[i,j] == F[i-1,j-1] + S[(a[i-1],b[j-1])]:
            alignA.insert(0,a[i-1])
            alignB.insert(0,b[j-1])
            i,j = i-1,j-1
        elif i > 0 and F[i,j] == F[i-1,j] + d:
            alignA.insert(0,a[i-1])
            alignB.insert(0,'-')
            i = i-1
        else:
            alignA.insert(0,'-')
            alignB.insert(0,b[j-1])
            j = j-1
        score += F[i,j]
    return(score)


def getPMI(etyma,reflexes):
  similarities = []
  S = init_sim()
  for t in range(10):
    align_counts = []
    for i in range(len(etyma)):
        #print(etyma[i])
        reflex_split = re.split(r'[ |-]',''.join(reflex[i]))
        scores = []
        for seg in reflex_split:
            scores.append(NWscore(S,etymon[i],list(seg)))
        j = np.argmax(scores)
        aligned = NW(S,etyma[i],list(reflex_split[j]))
        for i in range(len(aligned[0])):
            align_counts.append((aligned[0][i],aligned[1][i]))
    bi_counts = defaultdict(int)
    etym_counts = defaultdict(int)
    ref_counts = defaultdict(int)
    for x in segs:
        for y in segs:
            bi_counts[(x,y)] += .001
            etym_counts[x] += .001
            ref_counts[y] += .001
    for e in align_counts:
        if '-' not in e:
            bi_counts[e] += 1
            etym_counts[e[0]] += 1
            ref_counts[e[1]] += 1
    pmi = defaultdict(float)
    for k in bi_counts.keys():
        pxy = bi_counts[k]/sum(bi_counts.values())
        px = etym_counts[k[0]]/sum(etym_counts.values())
        py = ref_counts[k[1]]/sum(ref_counts.values())
        pmi[k] = np.log(pxy/(px*py))
    similarities.append(S)
    S = gensim(pmi)
    print(t)
    if len(similarities) >= 4 and sum(np.array(list(similarities[-1].values()))-np.array(list(similarities[-2].values())))==0:
        break
  return(S)

uralonet_data = [l.strip('\n').split('\t') for l in open('../Uralonet_data/Uralonet_cogsets.tsv','r')]

for i,l in enumerate(uralonet_data):
    uralonet_data[i][0] = uralonet_data[i][0].split('=')[-1]
    uralonet_data[i][1] = uralonet_data[i][1].split()[0]

uralonet_data = [l for l in uralonet_data if l[4] != '']

#for l in uralonet_data:
#    w = l[4]
#    w = re.sub(' \(.*\)','',w)
#    w_ = re.split(r', | ~ | : |-|',w)

uralonet_split = defaultdict(list)
for l in uralonet_data:
    w = l[4]
    w = re.sub(r'.+-: ','',w)
    w = re.sub('\(.*\)','',w)
    w = re.sub('\[.*\]','',w)
    w_ = re.split(r', |~|:',w)
    for s in w_:
        uralonet_split[tuple(l)].append(s)

uralonet_data = []
for key in uralonet_split.keys():
    l = list(key)
    for v in uralonet_split[key]:
        uralonet_data.append(l+[v])

uralonet_data = [l for l in uralonet_data if l[6] != '']

segs_to_strip = ['(', ')', '*', ',', '-', '/', '<', '>', '?','₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉','-',' ']

reflex = [list(l[6]) for l in uralonet_data]

etymon = [list(re.sub('['+'|'.join(segs_to_strip)+']','',re.sub(r'\([^\)]*\)','',l[1]))) for l in uralonet_data]

#etymon = [list(l[1]) for l in uralonet_data]

etymon_segs = sorted(set([s for l in etymon for s in l]))
reflex_segs = sorted(set([s for l in reflex for s in l]))
segs = sorted(set(etymon_segs+reflex_segs))

S = getPMI(etymon,reflex)

for i in range(len(etymon)):
    reflex_split = re.split(r'[ |-]',''.join(reflex[i]))
    reflex_split = [s for s in reflex_split if s != '']
    scores = []
    for seg in reflex_split:
        scores.append(NWscore(S,etymon[i],list(seg)))
    j = np.argmax(scores)
    uralonet_data[i].append(reflex_split[j])

f = open('uralonet_merged_reflex_aligned.tsv','w')
for l in uralonet_data:
    print('\t'.join(l),file=f)

f.close()