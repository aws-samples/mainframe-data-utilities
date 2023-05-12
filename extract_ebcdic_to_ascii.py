# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import sys, ebcdic as ebcdic, utils as utils, datasource as datasource, os

def lambda_handler(event, context):

    bkt =  event['Records'][0]['s3']['bucket']['name']
    key =  event['Records'][0]['s3']['object']['key']
    karr = key.split('/')

    jfle = '.'.join(karr[-1:][0].replace('.txt','').split('.')[:-1]) + '.json'

    fileconvertion(['extract_ebcdic_to_ascii.py',
                    '-s3-json' , 's3://' + os.environ.get('layout') + jfle,
                    '-s3-input', 's3://' + bkt + '/'  + key
                    ],
                    tmp='/tmp/')

    return {'statusCode': 200}

def s3_obj_lambda_handler(event, context):

    request_route = event["getObjectContext"]["outputRoute"]
    request_token = event["getObjectContext"]["outputToken"]
    s3_url = event["getObjectContext"]["inputS3Url"]

    layout = event['configuration']['payload'] + '.'.join(s3_url.split('?')[0].split('/')[-1].split('.')[:-2]) + '.json'

    fileconvertion(['extract_ebcdic_to_ascii.py',
                    '-s3-json' , 's3://' + layout,
                    '-s3-input', s3_url
                    ], request_route, request_token)

    return {'statusCode': 200}

def fileconvertion(args, route='', tkn='', tmp=''):

    log = utils.Log()
    prm = utils.ParamReader(args)
    InpDS = datasource.Input(prm.general)
    OutDS = datasource.Output(prm.general, route, tkn, tmp)

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

                OutRecord.addField(transf["name"], transf["type"],  transf["part-key"], prm.general["partkname"], transf["sort-key"], prm.general["sortkname"], prm.AddDecPlaces(ebcdic.unpack(record[transf["offset"]:transf["offset"]+transf["bytes"]], transf["type"], prm.general["rem-low-values"]), transf["dplaces"]))

            OutDS.Write(OutRecord.get())
    OutDS.Write()

    log.Write(['Records processed', str(i)])
    log.Finish()

if __name__ == '__main__':
    fileconvertion(sys.argv)