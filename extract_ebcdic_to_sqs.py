# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, sys, ebcdic, datetime, dynamodb, utils, sqs

print("-----------------------------------------------------","\nParameter file.............|",sys.argv[1])
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Script started")

with open(sys.argv[1]) as json_file: prm = utils.Param(json.load(json_file))

InpF=open(prm.input,"rb")

q = sqs.Batch(10,'LoadDDB')

i=0
while i < prm.max or prm.max == 0:

    record = InpF.read(prm.lrecl)

    if not record: break
    
    ddbo = dynamodb.item()
    
    i+= 1
    fim=0
    if i > prm.skip:

        if(prm.print != 0 and i % prm.print == 0): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,"| Records processed:", i)

        ini = 0

        layout = prm.GetLayout(record)

        for transf in layout:

            fim += transf["bytes"]

            ddbo.create(transf["name"], transf["type"], transf["key"], prm.keyname, prm.AddDecPlaces(ebcdic.unpack(record[ini:fim],transf["type"], prm.remlval), transf["dplaces"]))

            ini = fim
        
        q.send_message(json.dumps(ddbo.read()),i)

if len(q.entries) > 0: q.send_message()