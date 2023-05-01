import json, sys, core.copybook as copybook

transf = []
altlay = []
lrecl = 0
altpos = 0
partklen = 0
sortklen = 0

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

def RunParse(log, iparm):

    global transf
    global lrecl

    # Open the copybook for reading and creates the dictionary
    with open(iparm.copybook, 'r') as finp: output = copybook.toDict(finp.readlines())

    # Write the dict into a file if requested
    if iparm.json_debug != '':
        with open(iparm.json_debug,"w") as fout:
            fout.write(json.dumps(output,indent=4))

    # get the default values
    param = vars(iparm)

    partklen = iparm.part_k_len
    sortklen = iparm.sort_k_len

    CreateExtraction(output, [], partklen, sortklen)

    param['input_recl'] = lrecl
    param['transf_rule'] = []
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

    with open(iparm.json,"w") as fout: fout.write(json.dumps(param,indent=4))