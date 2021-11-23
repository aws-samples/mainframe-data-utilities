# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, sys, ebcdic, datetime, dynamodb

def GetLayout(_data, _rules):
    
    if len(_rules) == 0: return "transf"

    for r in _rules:
        if _data[r["offset"]:r["offset"]+r["size"]].hex() == r["hex"]: 
            return r["transf"]
    return "transf"

def AddDecPlaces(num,dplaces):
    if dplaces == 0:
        return num
    else:
        return num[:len(num)-dplaces] + '.' + num[len(num)-dplaces:]

print("-----------------------------------------------------","\nParameter file.............|",sys.argv[1])

with open(sys.argv[1]) as json_file: param = json.load(json_file)

InpF=open(param["input"],"rb")

if param["ddb-output"] == "":
    ddb = False
    OutF=open(param["output"],"w")
else:
    DDbF=open(param["ddb-output"],"w")
    ddb = True
    DDbF.write("{\"" + param["ddb-name"] + "\": [\n")
    sep = ""

i=0
while i < param["max"] or param["max"] == 0:

    linha = InpF.read(param["lrecl"])

    if not linha: break
    
    if ddb: ddbo = dynamodb.DDB()

    i+= 1
    fim=0
    if i > param["skip"]:
            
        layout = GetLayout(linha, param["transf-rule"])
        
        if(param["print"] != 0 and i % param["print"] == 0): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Records processed:", i)

        if(i >= param["max"]-3 and i <= param["max"]): print(linha.hex())
        
        ini = 0

        if ddb == False:
            for transf in param[layout]:

                fim += transf["bytes"]

                OutF.write(AddDecPlaces(ebcdic.unpack(linha[ini:fim],transf["type"], param["rem-low-values"]), transf["dplaces"]) + param["separator"])

                ini = fim
            OutF.write("\n")
        else:
            for transf in param[layout]:

                fim += transf["bytes"]

                ddbo.create(transf["name"], transf["type"],  transf["key"], param["keyname"], AddDecPlaces(ebcdic.unpack(linha[ini:fim],transf["type"], param["rem-low-values"]), transf["dplaces"]))

                ini = fim
            
            DDbF.write(sep + json.dumps(ddbo.readPutReq(),indent=4) + "\n")
            sep = ","
if ddb: DDbF.write("]}")