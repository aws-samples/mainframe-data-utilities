import json, sys

# FUNCTIONS TO HANDLE THE HIERARCHICAL STACK #
def fGetSetack():
    global stack, output
    tmp = output
    for k in stack:
        tmp = tmp[stack[k]]
    return tmp

def fRemStack(iStack,iLevel):
    NewStack = {}
    for k in iStack:
        if k < iLevel: NewStack[k] = iStack[k]
    return NewStack

# TYPE AND LENGTH CALCULATION #
def getLenType(atr):
    ret = {}
    FirstCh = atr[3][:1].upper()
    Picture = atr[3].upper()

    #data type
    if   'COMP-3'in atr and FirstCh=='S': ret['type'] = "pd+"
    elif 'COMP-3'in atr:                  ret['type'] = "pd"
    elif 'COMP'  in atr and FirstCh=='S': ret['type'] = "bi+"
    elif 'COMP'  in atr:                  ret['type'] = "bi"
    elif FirstCh=='S':                    ret['type'] = "zd+"
    elif FirstCh=='9':                    ret['type'] = "zd"
    else:                                 ret['type'] = "ch"

    #Total data length
    PicNum = Picture.replace("V"," ").replace("S","").replace("-","").split()
    Lgt = 0
    for x in PicNum:
        if x.find("(") > 0: 
            Lgt += int(x[x.find("(")+1:x.find(")")])
        else:
            Lgt += len(x)

    ret['length'] = Lgt

    #Data size in bytes
    #if  ret['type']     == "pd":  ret['bytes'] = round((Lgt)/2)
    if   ret['type'][:2] == "pd": ret['bytes'] = round((Lgt+1)/2)
    elif ret['type'][:2] == "bi": 
        if   Lgt <  5:             ret['bytes'] = 2
        elif Lgt < 10:             ret['bytes'] = 4
        else         :             ret['bytes'] = 8
    else:                          ret['bytes'] = Lgt

    return ret

############# DICTIONARY AND HIERARCHICAL LOGIC ###########################
def add2dict(lvl, grp, itm, stt, id):

    global cur, output, last, stack, FillerCount

    if itm.upper() == "FILLER":
        FillerCount += 1
        itm = itm + "-" + str(FillerCount)

    if lvl <= cur: stack = fRemStack(stack, lvl)

    stk = fGetSetack()
    stk[itm]= {}
    stk[itm]['id'] = id
    stk[itm]['level'] = lvl
    stk[itm]['group'] = grp

    if grp == True:
        stack[lvl] = itm
        cur = lvl
        if 'OCCURS'in stt: stk[itm]['occurs'] = stt[3]
        if 'REDEFINES'in stt: stk[itm]['redefines'] = stt[3]
    else:
        tplen = {}
        tplen = getLenType(stt)
        stk[itm]['pict'] = stt[3]
        stk[itm]['type'] = tplen['type']
        stk[itm]['length'] = tplen['length']
        stk[itm]['bytes'] = tplen['bytes']

############################### MAIN ###################################

print("-----------------------------------------------------")
print("\nInput file.............|",sys.argv[1],"\nOutput file.............|",sys.argv[2])

finp=open(sys.argv[1],"r")
fout=open(sys.argv[2],"w")

id = 0
FillerCount=0

cur=0
output={}
stack = {}

# READS, CLEANS AND JOINS LINES #
stt = ""
for line in finp.readlines(): 
    if line[6] != "*": stt += line.replace('\t', '    ')[6:72]    
finp.close()

# READS FIELD BY FIELD / SPLITS ATTRIBUTES #
for variable in stt.split("."):
    
    attribute=variable.split()

    if len(attribute) > 0:
        if attribute[0] != '88': 
            id += 1
            add2dict(int(attribute[0]), False if 'PIC'in attribute else True, attribute[1], attribute, id)

# CONVERTS DICT TO JSON #
fout.write(json.dumps(output,indent=4))
fout.close()