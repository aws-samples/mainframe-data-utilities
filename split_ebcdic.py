# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

#split_ebcdic.py -local-json sample-data/COBKS05-split.json

import utils, sys, boto3, json

def run(inputfile, lrecl, split_rule, bucket = '', max = 0, skip = 0, print=0):

    log = utils.Log()

    if bucket != '':
        Input = boto3.client('s3').get_object(Bucket=bucket, Key=inputfile)['Body']
    else:
        Input=open(inputfile,"rb")

    output = {}
    ctWrit = {}
    ctRead = 0

    for rule in split_rule:
        output[rule['file']] = open(rule['file'],'wb')
        ctWrit[rule['file']] = 0

    i=0
    while max == 0 or i < max:

        record = Input.read(lrecl)
        ctRead += 1

        if not record: break

        i+= 1
        if i > skip:

            if (print != 0 and i % print == 0): 
                log.Write(['Records read', str(ctRead)]) 
                for rule in split_rule:
                    log.Write(['Records written', rule['file'], str(ctWrit[rule['file']])]) 

            if len(split_rule) == 0: 
                log.Write('no rules!')
                quit()

            for r in split_rule:
                if record[r['offset']:r['offset']+r['size']].hex() == r['hex'].lower():
                    output[r['file']].write(record)
                    ctWrit[r['file']] += 1

    for rule in split_rule:
        if rule['bucket'] != '' and rule['key'] != '':
            boto3.client('s3').put_object(Body=open(rule['file'], 'rb'), Bucket=rule['bucket'], Key=rule['key'])

    log.Write(['Records read', str(ctRead)]) 
    for rule in split_rule:
        log.Write(['Records written', rule['file'], str(ctWrit[rule['file']])]) 
        
if __name__ == '__main__':

    arg = dict(zip(sys.argv[1::2], sys.argv[2::2]))

    with open(arg['-local-json']) as json_file: param = json.load(json_file)

    run(param['input-file'],param['lrecl'],param['split-rules'], param['input-bucket'], param['max'], param['skip'],param['print'])
