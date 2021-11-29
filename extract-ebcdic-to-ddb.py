# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import sys, ebcdic, dynamodb, utils, data

log = utils.Log()
prm = utils.ParamReader(sys.argv)

#y = globals()['A']()
#InpF=open(prm.general["input"],"rb")
InpF = data.SourceFile(prm.general["input"])

ddbo = dynamodb.Batch(prm.general["ddb-tbname"], 25)

i=0
while i < prm.general["max"] or prm.general["max"] == 0:

    record = InpF.read(prm.general["lrecl"])
    
    if not record: break
    
    ddbitem = dynamodb.item()

    i+= 1
    fim=0
    if i > prm.general["skip"]:
            
        if(prm.general["print"] != 0 and i % prm.general["print"] == 0): log.Write(['Records processed', str(i)]) 
        
        ini = 0
    
        layout = prm.GetLayout(record)
        
        for transf in layout:

            fim += transf["bytes"]

            ddbitem.add(transf["name"], transf["type"],  transf["key"], prm.general["keyname"], prm.AddDecPlaces(ebcdic.unpack(record[ini:fim], transf["type"], prm.general["rem-low-values"]), transf["dplaces"]))

            ini = fim
        
        ddbo.WriteItems(ddbitem.readPutReq())

if len(ddbo.list): ddbo.WriteItems()

log.Write(['Records processed', str(i)]) 
log.Write(['Finished']) 