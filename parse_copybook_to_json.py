import json, sys, copybook

def DisParam(arg):
    desc = {
        '-copybook'    : '* Copybook file name',
        '-output'      : '* Parsed copybook (JSON List)',
        '-ebcdic'      : 'EBCDIC file (to be converted)',
        '-ascii'       : 'ASCII output',
        '-keylen'      : 'Length of the key',
        '-keyname'     : 'Name of the key (for ddb)',
        '-output-type' : 'Output resource type (file, ddb or sqs)',
        '-req-size'    : 'Itens sent per request',
        '-print'       : 'Display after',
        '-dict'        : 'Generate dict json file',
        }

    for a in arg:
        if a in desc:
            print(a.ljust(12, ' '), ' | ', desc[a].ljust(40, ' '), '|', arg[a])
        else:
            print(a.ljust(12, ' '), ' | ', '>>>Unknown argument<<<'.ljust(40, ' '), '|', arg[a])

###### Create the extraction parameter file
def CreateExtraction(obj, altstack=[], keylength=0):
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
                        CreateExtraction(obj[k], altstack, keylength)
                        altstack.remove(k)
                    else:
                        item = {}
                        item['type'] = obj[k]['type']
                        item['bytes']  = obj[k]['bytes']
                        item['offset']  = lrecl
                        item['dplaces']  = obj[k]['dplaces']
                        item['name'] = k
                        item['key'] = True if (lrecl + obj[k]['bytes']) <= keylength else False
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
print("--------------------------------------------------------------------------------------")

iparm = dict(zip(sys.argv[1::2], sys.argv[2::2]))

if '-copybook' not in iparm or '-output' not in iparm:
    print('Basic sintax: python3 parse-copybook-to-json -copybook <copybookfile.cpb> -output <jsonfile.json>\n')
    quit()

DisParam(iparm)

with open(iparm['-copybook'], "r") as finp: output = copybook.toDict(finp.readlines())

if '-dict' in iparm:
    with open(iparm['-dict'],"w") as fout:
        fout.write(json.dumps(output,indent=4))

keylen = int(iparm['-keylen']) if '-keylen' in iparm else 0
altlay = []
transf = []
lrecl = 0
CreateExtraction(output, [], keylen)

param = {}
param['input']       = iparm['-ebcdic']        if '-ebcdic'      in iparm else 'ebcdicfile.txt'
param['output']      = iparm['-ascii']         if '-ascii'       in iparm else 'asciifile.txt'
param['keyname']     = iparm['-keyname']       if '-keyname'     in iparm else ''
param['output-type'] = iparm['-output-type']   if '-output-type' in iparm else 'file'
param['req-size']    = int(iparm['-req-size']) if '-req-size'   in iparm else 10
param['print']       = int(iparm['-print'])    if '-print'       in iparm else 0
param['max'] = 0
param['skip'] = 0
param['lrecl'] = lrecl
param['keylen'] = keylen
param['rem-low-values'] = True
param['separator'] = '|'
param['transf-rule'] = []
param['transf'] = transf

ialt = 0
for r in altlay:
    transf = []
    lrecl = 0
    redfkey = list(r.keys())[0]

    #POSITIONS ON REDEFINES
    newout = output
    for s in r[redfkey]['stack']:
        newout = newout[s]

    newout[redfkey] = r[redfkey].copy()
    newout[redfkey].pop('redefines')
    
    CreateExtraction(output, [], keylen)
    ialt += 1
    param['transf' + str(ialt)] = transf

with open(iparm['-output'],"w") as fout: fout.write(json.dumps(param,indent=4))

print("--------------------------------------------------------------------------------------")