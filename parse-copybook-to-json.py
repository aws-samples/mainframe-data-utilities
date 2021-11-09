import json, sys, copybook

###### Create the extraction parameter file
def CreateExtraction(obj):
    global lrecl
    for k in obj:
        if k != "id" and k != "level" and k != "group" and k != "occurs" and k != "redefines":
            if 'occurs' not in obj[k]:
                t = 1
            else: 
                t = obj[k]['occurs']

            if 'redefines' not in obj[k]:
                if obj[k]['group'] == True:
                    iTimes = 0
                    while iTimes < t:
                        iTimes +=1
                        CreateExtraction(obj[k])
                else:
                    item = {}
                    item['type'] = obj[k]['type']
                    item['bytes']  = obj[k]['bytes']
                    item['name'] = k
                    transf.append(item)
                    lrecl = lrecl + obj[k]['bytes']
                
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

transf = []
lrecl = 0

with open(iparm['-copybook'], "r") as finp:
    output = copybook.toDict(finp.readlines())

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
param['transf'] = transf

fout=open(iparm['-output'],"w")
fout.write(json.dumps(param,indent=4))
fout.close()

if '-dict' in iparm:
    fout=open(iparm['-dict'],"w")
    fout.write(json.dumps(output,indent=4))
    fout.close()

print("-----------------------------------------------------------------------")