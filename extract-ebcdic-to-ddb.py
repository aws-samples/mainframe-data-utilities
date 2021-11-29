# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import sys, ebcdic, dynamodb, utils, datasource

log = utils.Log()
prm = utils.ParamReader(sys.argv)

InpF = datasource.Input(prm.general["input"])

ddbo = dynamodb.Batch(prm.general["ddb-tbname"], 25)
 
i=0
while i < prm.general["max"] or prm.general["max"] == 0:

    record = InpF.read(prm.general["lrecl"])
    
    if not record: break
    
    ddbitem = dynamodb.item()

    i+= 1
    if i > prm.general["skip"]:
            
        if(prm.general["print"] != 0 and i % prm.general["print"] == 0): log.Write(['Records processed', str(i)]) 
        
        layout = prm.GetLayout(record)
        
        for transf in layout:

            ddbitem.add(transf["name"], transf["type"],  transf["key"], prm.general["keyname"], prm.AddDecPlaces(ebcdic.unpack(record[transf["offset"]:transf["offset"]+transf["bytes"]], transf["type"], prm.general["rem-low-values"]), transf["dplaces"]))
        
        ddbo.WriteItems(ddbitem.readPutReq())

if len(ddbo.list): ddbo.WriteItems()

log.Write(['Records processed', str(i)]) 
log.Finish()