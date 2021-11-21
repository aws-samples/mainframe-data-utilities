import json, sys, copybook

###### Create the extraction parameter file
def CreateExtraction(obj, altstack=[]):
    global lrecl
    for k in obj:
        if type(obj[k]) is dict:
            t = 1 if 'occurs' not in obj[k] else obj[k]['occurs']

            iTimes = 0
            while iTimes < t:
                iTimes +=1

                if 'redefines' not in obj[k]:
                    if obj[k]['group'] == True:
                        altstack.append(k)
                        CreateExtraction(obj[k], altstack)
                        altstack.remove(k)
                    else:
                        item = {}
                        item['type'] = obj[k]['type']
                        item['bytes']  = obj[k]['bytes']
                        item['dplaces']  = obj[k]['dplaces']
                        item['name'] = k
                        transf.append(item)
                        lrecl = lrecl + obj[k]['bytes']
                else:
                    add2alt = True
                    for x in altlay:
                        if x[list(x)[0]]['newname'] == k:
                            add2alt = False
                    if add2alt:
                        red = {}
                        red[obj[k]['redefines']] = obj[k].copy()
                        red[obj[k]['redefines']]['newname'] = k
                        red[obj[k]['redefines']]['stack'] = altstack.copy()
                        altlay.append(red)
                
############################### MAIN ###################################
print("-----------------------------------------------------------------------")

iparm = dict(zip(sys.argv[1::2], sys.argv[2::2]))

if '-copybook' not in iparm or '-output' not in iparm:
    print('Sintax: python parse-copybook-to json -copybook <copybookfile.cpb> -output <jsonfile.json>\n')
    quit()

print("Copybook file...............|", iparm['-copybook'])
print("Parsed copybook (JSON List).|", iparm['-output'])

if '-dict'   in iparm: print("JSON Dict (documentation)...|", iparm['-dict'])
if '-ascii'  in iparm: print("ASCII file..................|", iparm['-ascii'])
if '-ebcdic' in iparm: print("EBCDIC file.................|", iparm['-ebcdic'])
if '-print'  in iparm: print("Print each..................|", iparm['-print'])

with open(iparm['-copybook'], "r") as finp:
    output = copybook.toDict(finp.readlines())

if '-dict' in iparm:
    with open(iparm['-dict'],"w") as fout:
        fout.write(json.dumps(output,indent=4))

altlay = []
transf = []
lrecl = 0
CreateExtraction(output)

param = {}
param['input']  = iparm['-ebcdic'] if '-ebcdic' in iparm else 'ebcdicfile.txt'
param['output'] = iparm['-ascii']  if '-ascii'  in iparm else 'asciifile.txt'
param['max'] = 0
param['skip'] = 0
param['print'] = int(iparm['-print']) if '-print'in iparm else 0
param['lrecl'] = lrecl
param['rem-low-values'] = True
param['separator'] = '|'
param['transf-rule'] = []
param['transf'] = transf

ialt = 0
for r in altlay:
    transf = []
    redfkey = list(r.keys())[0]

    #POSITIONS ON REDEFINES
    newout = output
    for s in r[redfkey]['stack']:
        newout = newout[s]

    newout[redfkey] = r[redfkey].copy()
    newout[redfkey].pop('redefines')
    
    CreateExtraction(output)
    ialt += 1
    param['transf' + str(ialt)] = transf

with open(iparm['-output'],"w") as fout:
    fout.write(json.dumps(param,indent=4))

print("-----------------------------------------------------------------------")