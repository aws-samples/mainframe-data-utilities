# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, sys, ebcdic, datetime

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
            
        if(i % param["print"] == 0): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Records processed:", i)

        if(i >= param["max"]-3 and i <= param["max"]): print(linha.hex())

        ini = 0
        for transf in param["transf"]:

            fim += transf["val"]

            OutF.write((ebcdic.unpack(linha[ini:fim],transf["type"],transf["name"]) + param["separator"]))

            ini = fim

        OutF.write("\n")