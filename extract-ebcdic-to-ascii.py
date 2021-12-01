# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import sys, ebcdic, utils, datasource

def lambda_handler(event, context):
    fileconvertion(['-json-s3',''])

def fileconvertion(args):
        
    log = utils.Log()
    prm = utils.ParamReader(args)
    InpDS = datasource.Input(prm.general["input"])
    OutDS = datasource.Output(prm.general)

    i=0
    while i < prm.general["max"] or prm.general["max"] == 0:

        record = InpDS.read(prm.general["lrecl"])
        
        if not record: break
        
        OutRecord = datasource.item(prm.general)

        i+= 1
        if i > prm.general["skip"]:
                
            if(prm.general["print"] != 0 and i % prm.general["print"] == 0): log.Write(['Records processed', str(i)]) 
            
            layout = prm.GetLayout(record)
            
            for transf in layout:

                OutRecord.addField(transf["name"], transf["type"],  transf["key"], prm.general["keyname"], prm.AddDecPlaces(ebcdic.unpack(record[transf["offset"]:transf["offset"]+transf["bytes"]], transf["type"], prm.general["rem-low-values"]), transf["dplaces"]))
            
            OutDS.Write(OutRecord.get())
    OutDS.Write()

    log.Write(['Records processed', str(i)]) 
    log.Finish()

if __name__ == '__main__':
    fileconvertion(sys.argv)