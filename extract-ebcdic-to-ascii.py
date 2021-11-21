# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, sys, ebcdic, datetime

def GetLayout(_data, _rules):
    
    if len(_rules) == 0: return "transf"

    for r in _rules:
        if _data[r["offset"]:r["offset"]+r["size"]].hex() == r["hex"]: 
            return r["transf"]
    return "transf"

def AddDecPlaces(num,dplaces):
    return num[:len(num)-dplaces] + '.' + num[len(num)-dplaces:]

print("-----------------------------------------------------","\nParameter file.............|",sys.argv[1])

with open(sys.argv[1]) as json_file: param = json.load(json_file)

InpF=open(param["input"],"rb")
OutF=open(param["output"],"w")

i=0
while i < param["max"] or param["max"] == 0:

    linha = InpF.read(param["lrecl"])

    if not linha: break
    
    i+= 1
    fim=0
    if i > param["skip"]:
            
        layout = GetLayout(linha, param["transf-rule"])
        
        if(param["print"] != 0 and i % param["print"] == 0): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Records processed:", i)

        if(i >= param["max"]-3 and i <= param["max"]): print(linha.hex())

        ini = 0
        for transf in param[layout]:

            fim += transf["bytes"]

            if transf["dplaces"] == 0:
                OutF.write((ebcdic.unpack(linha[ini:fim],transf["type"], param["rem-low-values"]) + param["separator"]))
            else:
                OutF.write((AddDecPlaces(ebcdic.unpack(linha[ini:fim],transf["type"], param["rem-low-values"]), transf["dplaces"]) + param["separator"]))
            
            ini = fim

        OutF.write("\n")