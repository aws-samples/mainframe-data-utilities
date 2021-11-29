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
    if dplaces == 0:
        return num
    else:
        return num[:len(num)-dplaces] + '.' + num[len(num)-dplaces:]

arg = dict(zip(sys.argv[1::2], sys.argv[2::2]))

if not '-local-json' in arg: 
    print('\nSintax: python3 extract-ebcdic-to-ascii.py -local-json path/to/layout.json \n')
    quit()

print("-----------------------------------------------------")
print("JSON Layout file           |", arg['-local-json'])
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| STARTED")

with open(arg['-local-json']) as json_file: param = json.load(json_file)

InpF=open(param["input"],"rb")
OutF=open(param["output"],"w")

i=0
while i < param["max"] or param["max"] == 0:

    linha = InpF.read(param["lrecl"])

    if not linha: break

    i+= 1
    if i > param["skip"]:
        if(param["print"] != 0 and i % param["print"] == 0): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Records processed:", i)

        layout = GetLayout(linha, param["transf-rule"])
        
        for transf in param[layout]:
            OutF.write(
                AddDecPlaces(
                    ebcdic.unpack(
                        linha[transf["offset"]:transf["offset"]+transf["bytes"]],transf["type"], param["rem-low-values"]),
                    transf["dplaces"]) + param["separator"])

        OutF.write("\n")