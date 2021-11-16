import json, sys, copybook

###### Create the extraction parameter file
def CreateExtraction(obj, alt={}):
    global lrecl
    for k in obj:
        if type(obj[k]) is dict:

            t = 1 if 'occurs' not in obj[k] else obj[k]['occurs']

            iTimes = 0
            while iTimes < t:
                iTimes +=1

                if 'redefines' not in obj[k]:
                    if k in alt:
                        CreateExtraction(alt[k], alt)
                    elif obj[k]['group'] == True:
                        CreateExtraction(obj[k], alt)
                    else:
                        item = {}
                        item['type'] = obj[k]['type']
                        item['bytes']  = obj[k]['bytes']
                        item['name'] = k
                        transf.append(item)
                        lrecl = lrecl + obj[k]['bytes']
                elif not alt:
                    red = {}
                    red[obj[k]['redefines']] = obj[k]
                    red[obj[k]['redefines']]['newname'] = k
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
param['input'] = iparm['-ebcdic'] if '-ebcdic'in iparm else 'ebcdicfile.txt'
param['output'] = iparm['-ascii'] if '-ascii'in iparm else 'asciifile.txt'
param['max'] = 0
param['skip'] = 0
param['print'] = int(iparm['-print']) if '-print'in iparm else 0
param['lrecl'] = lrecl
param['rem-low-values'] = True
param['separator'] = '|'
param['transf-rule'] = {}
param['transf'] = transf

ialt = 0
for r in altlay:
    transf = []
    CreateExtraction(output,r)
    ialt += 1
    param['transf' + str(ialt)] = transf

with open(iparm['-output'],"w") as fout:
    fout.write(json.dumps(param,indent=4))

print("-----------------------------------------------------------------------")