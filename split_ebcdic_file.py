# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# How to run: split_ebcdic.py -local-json sample-data/COBKS05-split.json

import utils as utils, sys, boto3, json

log = utils.Log()

def getRDW(b: bytearray):
    return int("0x" + b[:2].hex(), 0) - 4 if len(b) > 0 else 0

def stats(reads, rules, writes):

    log.Write(['Records read', str(reads)])

    for rule in rules:
        log.Write(['Records written', rule['file'], str(writes[rule['file']])])

def run(inputfile, lrecl, split_rule, bucket = '', max = 0, skip = 0, print=0, recfm='fb'):

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

        if recfm == 'fb':
            rdw = bytearray()
            record = Input.read(lrecl)
        else:
            l = getRDW(rdw:= Input.read(4))
            record = Input.read(l)

        if not record: break

        ctRead += 1

        i+= 1
        if i > skip:

            if (print != 0 and i % print == 0): stats(ctRead, split_rule, ctWrit)

            if len(split_rule) == 0: raise Exception('Please define split rules')

            for r in split_rule:
                if utils.cond[r['cond']](record[r['offset']:r['offset']+r['size']].hex() , r['hex'].lower()):
                    output[r['file']].write(rdw + record)
                    ctWrit[r['file']] += 1

    for rule in split_rule:
        if rule['bucket'] != '' and rule['key'] != '':
            boto3.client('s3').put_object(Body=open(rule['file'], 'rb'), Bucket=rule['bucket'], Key=rule['key'])

    stats(ctRead, split_rule, ctWrit)

if __name__ == '__main__':

    arg = dict(zip(sys.argv[1::2], sys.argv[2::2]))

    if not '-local-json' in arg:
        raise Exception('Error! Sintax must be: python3 ' + sys.argv[0] + ' -local-json path/to/layout.json')

    with open(arg['-local-json']) as json_file: param = json.load(json_file)

    run(param['input-file'],param['lrecl'],param['split-rules'], param['input-bucket'], param['max'], param['skip'],param['print'],param['recfm'])