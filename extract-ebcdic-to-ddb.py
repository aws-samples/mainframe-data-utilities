# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, sys, ebcdic, datetime, dynamodb, utils

print("-----------------------------------------------------","\nParameter file.............|",sys.argv[1])
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| STARTED")

with open(sys.argv[1]) as json_file: param = json.load(json_file)

prm = utils.Param(param)

InpF=open(param["input"],"rb")

ddbo = dynamodb.Batch(param["ddb-tbname"], 25)

i=0
while i < param["max"] or param["max"] == 0:

    linha = InpF.read(param["lrecl"])

    if not linha: break
    
    ddbitem = dynamodb.item()

    i+= 1
    fim=0
    if i > param["skip"]:
            
        if(param["print"] != 0 and i % param["print"] == 0): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Records processed:", i)
        
        ini = 0
    
        layout = prm.GetLayout(linha)
        
        for transf in layout:

            fim += transf["bytes"]

            ddbitem.create(transf["name"], transf["type"],  transf["key"], param["keyname"], prm.AddDecPlaces(ebcdic.unpack(linha[ini:fim],transf["type"], param["rem-low-values"]), transf["dplaces"]))

            ini = fim
        
        ddbo.WriteItems(ddbitem.readPutReq())
if len(ddbo.list): ddbo.WriteItems()
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Records processed:", i)
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| FINISHED")