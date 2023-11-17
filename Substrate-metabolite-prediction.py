import codecs
import nltk

dirtory = input('Enter the directory of the file where the texts are stored')
file = codecs.open(dirtory, 'r', encoding = 'utf-8')
lines = file.readlines()
file.close()
texts = []
for line in lines:
    line = line.replace('\r', '')
    line = line.replace('\n', '')
    if line.isdigit():
        pmid = line
    else:
        texts.append({'pmid': pmid, 'text': line})

dirtory = input('Enter the directory of the file where the chemical named entitiy annotations are stored')
file = codecs.open(dirtory, 'r', encoding = 'utf-8')
lines = file.readlines()
file.close()
nl = []
for line in lines:
    line = line.replace('\r', '')
    line = line.replace('\n', '')
    mid = line.split('\t')
    nl.append(mid)
print('Finished reading the file')

newt = texts
texts = []
i=0
while i<len(newt):
    midann = []
    j=len(nl)-1
    while j>=0:
        if nl[j][0]==newt[i]['pmid']:
            if nl[j][1] not in midann:
                midann.append(nl[j][1])
            nl.pop(j)
        j=j-1
    newt[i].update({'entities': midann})
    texts.append(newt[i])
    i=i+1
print('Finished reading chemical named entities from file')

## <PP> <S>, sigle scheme
KP1 = ["biotransformation of", "degradation rate of", "metabolite of", "metabolites of", "derivative of", "derivatives of",
        "metabolic product of", "metabolic products of", "metabolism of", 'disposition of', 'the parent compound ,' 'elimination of',
        'reduction of', 'cleavage of']
## <S><PP>, single scheme
KP2=["was metabolized", "is metabolized"]
## <PP><M>, single scheme
KP3=["metabolite is", "metabolite was", 'formation of']
## <PP><M>, plural scheme
KP4=["metabolites are", "metabolites were", "metabolized to", 'excretion of', 'metabolized into', 'oxidation to',
        'metabolic formation of', 'rate of formation of']
## <M><PP>, single scheme
KP5=["is metabolite", "was metabolite", 'a metabolite of', 'a major metabolite', 'a minor metabolite',
        'a major urinary metabolite', 'a minor urinary metabolite', 'the metabolite of']
## <M><PP>, plural scheme
KP6=["are metabolites", "were metabolites"]
##reactions
dirtory = input('Enter the directory of the file where the list of reaction named entities is stored')
f = codecs.open(dirtory, 'r', encoding = 'utf-8')
lines = f.readlines()
file.close()
KP7 = []
for line in lines:
    line = line.replace('\r', '')
    line = line.replace('\n', '')
    line = line.lower()
    KP7.append(line)
midrec = ['methylation', 'amination', 'conjugation', 'alkylation', 'phosphorylation', 'protein binding', 'glucuronidation',
        'covalent binding', 'demethylation', 'acetylation', 'dealkylation', 'resolution', 'esterification', 'rearrangement',
        'protonation', 'dealkylation', 'demethylation', 'condensation', 'dimerization', 'dephosphorylation', 'oxygenation',
        'oxidation', 'hydrolysis', 'hydroxylation', 'deethylation']
for elem in midrec:
    if elem not in KP7:
        KP7.append(elem)
print('Finihed reading the rules')

count = 1
pairs = []
for text in texts:
    print(count, '/', len(texts))
    count+=1
    snt = nltk.sent_tokenize(text['text'])
    for elem in snt:
        mident = []
        for e in text['entities']:
            if e in elem:
                mident.append(e)
        sntann = []
        if mident!=[]:
            for p in KP1:
                if p in elem.lower():
                    start = elem.find(p)
                    pcmid = []
                    for e in mident:
                        if e in elem[start+len(p):]:
                            se = elem[start+len(p):].find(e)
                            pcmid.append([se, e])
                    m = len(elem)
                    ann = []
                    for e in pcmid:
                        if e[0]<m:
                            m = e[0]
                            ann = [e[1], 'S']
                    if ann not in sntann:
                        sntann.append(ann)
            for p in KP2:
                if p in elem.lower():
                    start = elem.find(p)
                    pcmid = []
                    for e in mident:
                        if e in elem[:start]:
                            se = elem[:start].find(e)
                            pcmid.append([se, e])
                    m=0
                    ann = []
                    for e in pcmid:
                        if e[0]>m:
                            m = e[0]
                            ann = [e[1], 'S']
                    if ann not in sntann:
                        sntann.append(ann)
            for p in KP3:
                if p in elem.lower():
                    start = elem.find(p)
                    pcmid = []
                    for e in mident:
                        if e in elem[start+len(p):]:
                            se = elem[start+len(p):].find(e)
                            pcmid.append([se, e])
                    m = len(elem)
                    ann = []
                    for e in pcmid:
                        if e[0]<m:
                            m = e[0]
                            ann = [e[1], 'M']
                    if ann not in sntann:
                        sntann.append(ann)
            for p in KP5:
                if p in elem.lower():
                    start = elem.find(p)
                    pcmid = []
                    for e in mident:
                        if e in elem[:start]:
                            se = elem[:start].find(e)
                            pcmid.append([se, e])
                    m=0
                    ann = []
                    for e in pcmid:
                        if e[0]>m:
                            m = e[0]
                            ann = [e[1], 'M']
                    if ann not in sntann:
                        sntann.append(ann)
            for p in KP4:
                if p in elem.lower():
                    start = elem.find(p)
                    for e in mident:
                        if e in elem[start+len(p):]:
                            if [e,'M'] not in sntann:
                                sntann.append([e,'M'])
            for p in KP6:
                if p in elem.lower():
                    start = elem.find(p)
                    for e in mident:
                        if e in elem[:start]:
                            if [e,'M'] not in sntann:
                                sntann.append([e,'M'])
            for p in KP7:
                if p in elem.lower():
                    start = elem.find(p)
                    if elem[start+len(p)+1:start+len(p)+2]=='of':
                        pcmid = []
                        for e in mident:
                            if e in elem[start+len(p):]:
                                se = elem[start+len(p):].find(e)
                                pcmid.append([se, e])
                        m = len(elem)
                        ann = []
                        for e in pcmid:
                            if e[0]<m:
                                m = e[0]
                                ann = [e[1], 'S']
                        if ann not in sntann:
                            sntann.append(ann)
                    else:
                        pcmid = []
                        for e in mident:
                            if e in elem[:start]:
                                se = elem[:start].find(e)
                                pcmid.append([se, e])
                        m=0
                        ann = []
                        for e in pcmid:
                            if e[0]>m:
                                m = e[0]
                                ann = [e[1], 'S']
                        if ann not in sntann:
                            sntann.append(ann)
        metabolites = []
        parents = []
        i=len(sntann)-1
        while i>=0:
            if sntann[i]==[]:
                sntann.pop(i)
            i=i-1
        for ne in sntann:
            if ne[1]=='M':
                metabolites.append(ne[0])
            if ne[1]=='S':
                parents.append(ne[0])
        midp = []
        if metabolites!=[] and parents!=[]:
            for p in parents:
                for m in metabolites:
                    if p!=m:
                        midp.append(p+'//'+m)
        midents = []
        for p in parents:
            if p in metabolites:
                midents.append(p + ' (S, M)')
            else:
                midents.append(p + ' (S)')
        for m in metabolites:
            if m in parents:
                pass
            else:
                midents.append(m + ' (M)')
        if midp==[]:
            midp = ['-']
        if midents == []:
            midents = ['-']
        pairs.append([text['pmid'], elem, midp, midents])

dirtory = input('Enter the directory of the file where results to be stores')
filew = codecs.open(dirtory, 'a', encoding = 'utf-8')
for pair in pairs:
    filew.write(pair[0] + '\t' + pair[1] + '\t' + '; '.join(pair[2]) + '\t' + '; '.join(pair[3]) + '\n')
filew.close()














