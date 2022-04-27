# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

#split_ebcdic.py -local-json sample-data/COBKS05-split.json

import utils, sys, boto3, json

log = utils.Log

def getOutPutFile(rules, data):

    if len(rules) == 0: 
        log.Write('no rules!')
        quit()

    for r in rules:
        if data[r['offset']:r['offset']+r['size']].hex() == r['hex'].lower():
            return r['file']

    return False

def run(inputfile, lrecl, split_rule, bucket = '', max = 0, skip = 0, print=0):

    if bucket != '':
        Input = boto3.client('s3').get_object(Bucket=bucket, Key=inputfile)['Body']
    else:
        Input=open(inputfile,"rb")

    output = {}
    for rule in split_rule:
        output[rule['file']] = open(rule['file'],'wb')

    i=0
    while max == 0 or i < max:

        record = Input.read(lrecl)
        
        if not record: break

        i+= 1
        if i > skip:

            if (print != 0 and i % print == 0): log.Write(['Records processed', str(i)]) 
            
            ofilename = getOutPutFile(split_rule, record)

            if ofilename:
                output[ofilename].write(record)
    
if __name__ == '__main__':

    arg = dict(zip(sys.argv[1::2], sys.argv[2::2]))

    with open(arg['-local-json']) as json_file: param = json.load(json_file)

    run(param['input-file'],param['lrecl'],param['split-rules'])

def lambda_handler(event, context):

    bkt =  event['Records'][0]['s3']['bucket']['name']
    key =  event['Records'][0]['s3']['object']['key']
    
    jfld = ('/' + '/'.join(karr[:-1]) if len(karr := key.split('/')) > 1 else '') + '/layout/'
    jfle = '.'.join(karr[-1:][0].replace('.txt','').split('.')[:-1]) + '.json'

    run(['extract_ebcdic_to_ascii.py',
                    '-s3-json' , 's3://' + bkt + jfld + jfle,
                    '-s3-input', 's3://' + bkt + '/'  + key
                    ])

    return {'statusCode': 200}


