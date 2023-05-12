import json, sys, copybook as copybook

def DisParam(arg):
    desc = {
        '-copybook'    : 'REQUIRED: Copybook file name',
        '-output'      : 'REQUIRED: Parsed copybook (JSON List)',
        '-ebcdic'      : 'EBCDIC file (to be converted)',
        '-ascii'       : 'ASCII output',
        '-part-k-len'  : 'Partition key length',
        '-sort-k-len'  : 'Sort key length',
        '-part-k-name' : 'Partition key name',
        '-sort-k-name' : 'Sort key name',
        '-output-s3key': 'S3 Output key',
        '-output-s3bkt': 'S3 Output Bucket',
        '-output-type' : 'Output resource type (file, ddb or s3)',
        '-req-size'    : 'Itens sent per request',
        '-print'       : 'Display after',
        '-dict'        : 'Generate dict json file',
        '-recfm'       : 'Record format (FB/VB)'
        }

    for a in arg:
        if a in desc:
            print(a.ljust(12, ' '), ' | ', desc[a].ljust(40, ' '), '|', arg[a])
        else:
            print(a.ljust(12, ' '), ' | ', '>>>Unknown argument<<<'.ljust(40, ' '), '|', arg[a])

###### Create the extraction parameter file
def CreateExtraction(obj, altstack=[], partklen=0, sortklen=0):
    global lrecl
    global altpos
    for k in obj:
        if type(obj[k]) is dict:
            t = 1 if 'occurs' not in obj[k] else obj[k]['occurs']

            iTimes = 0
            while iTimes < t:
                iTimes +=1

                if 'redefines' not in obj[k]:
                    if obj[k]['group'] == True:
                        altstack.append(k)
                        CreateExtraction(obj[k], altstack, partklen, sortklen)
                        altstack.remove(k)
                    else:
                        item = {}
                        item['type'] = obj[k]['type']
                        item['bytes']  = obj[k]['bytes']
                        item['offset']  = lrecl
                        item['dplaces']  = obj[k]['dplaces']
                        item['name'] = k
                        item['part-key'] = True if (lrecl + obj[k]['bytes']) <= partklen else False
                        item['sort-key'] = True if (lrecl + obj[k]['bytes']) <= (sortklen + partklen) and (lrecl + obj[k]['bytes']) > partklen else False
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
                        altpos+=1
                        altlay.insert(altpos,red)

############################### MAIN ###################################
print("--------------------------------------------------------------------------------------")

iparm = dict(zip(sys.argv[1::2], sys.argv[2::2]))

DisParam(iparm)

if '-copybook' not in iparm or '-output' not in iparm:
    print('Error! The basic sintax is: python3 parse_copybook_to_json.py -copybook <copybookfile.cpb> -output <jsonfile.json>\n')
    quit()

with open(iparm['-copybook'], "r") as finp: output = copybook.toDict(finp.readlines())

if '-dict' in iparm:
    with open(iparm['-dict'],"w") as fout:
        fout.write(json.dumps(output,indent=4))

partklen = int(iparm['-part-k-len']) if '-part-k-len' in iparm else 0
sortklen = int(iparm['-sort-k-len']) if '-sort-k-len' in iparm else 0
altlay = []
transf = []
lrecl = 0
altpos = 0
CreateExtraction(output, [], partklen, sortklen)

param = {}
param['input']       = iparm['-ebcdic']        if '-ebcdic'       in iparm else 'ebcdicfile.txt'
param['output']      = iparm['-ascii']         if '-ascii'        in iparm else 'asciifile.txt'
param['partkname']   = iparm['-part-k-name']   if '-part-k-name'  in iparm else ''
param['sortkname']   = iparm['-sort-k-name']   if '-sort-k-name'  in iparm else ''
param['output-type'] = iparm['-output-type']   if '-output-type'  in iparm else 'file'
param['output-s3key']= iparm['-output-s3key']  if '-output-s3key' in iparm else ''
param['output-s3bkt']= iparm['-output-s3bkt']  if '-output-s3bkt' in iparm else ''
param['recfm']       = iparm['-recfm'].lower() if '-recfm'        in iparm else 'fb'
param['req-size']    = int(iparm['-req-size']) if '-req-size'     in iparm else 10
param['print']       = int(iparm['-print'])    if '-print'        in iparm else 0
param['max'] = 0
param['skip'] = 0
param['lrecl'] = lrecl
param['partklen'] = partklen
param['sortklen'] = sortklen
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

    altpos = ialt
    CreateExtraction(output, [], partklen, sortklen)
    ialt += 1
    param['transf' + str(ialt)] = transf

with open(iparm['-output'],"w") as fout: fout.write(json.dumps(param,indent=4))

print("--------------------------------------------------------------------------------------")