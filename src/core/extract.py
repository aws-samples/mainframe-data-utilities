# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3, urllib3, json
import multiprocessing as mp
from core.ebcdic        import unpack
from itertools          import cycle
from botocore.exceptions import ClientError

def FileProcess(log, ExtArgs):

    fMetaData = FileMetaData(log, ExtArgs)

    if fMetaData.inputtype == 'local':

        InpDS = open(fMetaData.general['input'],"rb")

    else:

        log.Write(['Downloading file from s3'])

        inp_temp = local_input(fMetaData.general['working_folder'], fMetaData.general['input'])

        if fMetaData.inputtype == 's3':

            with open(inp_temp, 'wb') as f:
                boto3.client('s3').download_fileobj(fMetaData.general['input_s3'], fMetaData.general['input'], f)

        else:

            if fMetaData.general['input_s3_url'].lower().startswith('http'):

                #urllib.request.urlretrieve(fMetaData.general['input_s3_url'], inp_temp) #nosec url validated above

                http = urllib3.PoolManager()
                cont = http.request('GET', fMetaData.general['input_s3_url']).data

            log.Write(['Object lambda not implemented'])

        InpDS = open(inp_temp,"rb")

    # prepare for multiprocessing
    lstFiles = []
    dctQueue = {}
    lstProce = []

    log.Write([ '# of threads' , str(fMetaData.general['output_parallelism']) ])

    for f in range(1, fMetaData.general['output_parallelism']+1):
        strOutFile = fMetaData.general['working_folder'] + fMetaData.general['output'] + (str(f) if f > 1 else '')
        lstFiles.append(strOutFile)
        dctQueue[strOutFile] = mp.Queue()
        p = mp.Process(target=process_record, args=(log, fMetaData, strOutFile, dctQueue[strOutFile]))
        p.start()
        lstProce.append(p)

    cyFiles = cycle(lstFiles)

    i=0
    while i < fMetaData.general['max'] or fMetaData.general['max'] == 0:

        record = read(InpDS, fMetaData.general['input_recfm'], fMetaData.general["input_recl"])

        if not record: break

        i+= 1
        if i > fMetaData.general["skip"]:

            if(fMetaData.general["print"] != 0 and i % fMetaData.general["print"] == 0): log.Write(['Records read', str(i)])

            nxq = next(cyFiles)
            dctQueue[nxq].put(record)

    # stop /wait for the workers
    for f in lstFiles: dctQueue[f].put(None)
    for p in lstProce: p.join()

    log.Write(['Records processed', str(i)])

def process_record(log, fMetaData, OutDs, q):

    if fMetaData.general['output_type'] in ['file', 's3_obj', 's3']:
        outfile = open(OutDs, 'w')
        newl = ''
    else:
        outfile = []

    while True:
        record = q.get()
        if record is None:
            if fMetaData.general['output_type'] in ['file', 's3_obj', 's3']:

                outfile.close()

                if fMetaData.general['output_s3'] != '':

                    if fMetaData.general['verbose']: log.Write(['Uploading to s3', OutDs])

                    try:
                        response = boto3.client('s3').upload_file(OutDs, fMetaData.general['output_s3'], OutDs)
                    except ClientError as e:
                        log.Write(e)
            else:
                if len(outfile) >= 0:
                    log.Write(['Updating DynamoDB', str(len(outfile))])
                    response = boto3.client('dynamodb').batch_write_item(RequestItems={ fMetaData.general['output'] : outfile })
            break

        OutRec = [] if fMetaData.general['output_type'] in ['file', 's3-obj', 's3'] else {}

        layout = fMetaData.GetLayout(record)

        for transf in layout:
            addField(
                fMetaData.general['output_type'],
                OutRec,
                transf['name'],
                transf['type'],
                transf['part-key'],
                fMetaData.general['part_k_name'],
                transf['sort-key'],
                fMetaData.general['sort_k_name'],
                unpack(record[transf["offset"]:transf["offset"]+transf["bytes"]], transf["type"], transf["dplaces"], fMetaData.general["rem_low_values"], False ),
                False)

        if fMetaData.general['output_type'] in ['file', 's3_obj', 's3']:
            outfile.write(newl + fMetaData.general['output_separator'].join(OutRec))
            newl='\n'
        else:
            # prepare the batchwrite
            outfile.append({'PutRequest' : { 'Item' : OutRec }})

            if len(outfile) >= fMetaData.general['req_size']:
                log.Write(['Updating DynamoDB', str(len(outfile))])
                response = boto3.client('dynamodb').batch_write_item(RequestItems={ fMetaData.general['output'] : outfile })
                outfile = []

def local_input(working_folder, key):

     return working_folder + key.split("/")[-1]

def read(input, recfm, lrecl):

    if recfm == 'fb':
        return input.read(lrecl)
    else:
        l = getRDW(input.read(4))
        return input.read(l)

def getRDW(b: bytearray):
    return int("0x" + b[:2].hex(), 0) - 4 if len(b) > 0 else 0

def addField(outtype, record, id, type, partkey, partkname, sortkey, sortkname, value, addempty = False):

    if outtype in ['file', 's3-obj', 's3']:
        record.append(value)
    else:
        if not partkey and not sortkey:
            if value != '' or addempty:
                record[id.replace('-','_')] = {}
                record[id.replace('-','_')]['S' if type == "ch" else 'N'] = value
        elif not partkey:
            if sortkname in record:
                record[sortkname]['S'] = record[sortkname]['S'] + "|" + value
            else:
                record[sortkname] = {}
                record[sortkname]['S'] = value
        else:
            if partkname in record:
                record[partkname]['S'] = record[partkname]['S'] + "|" + value
            else:
                record[partkname] = {}
                record[partkname]['S'] = value

class FileMetaData:

    def __init__(self, log, args):

        if args.json_s3 == '':
            json_local = args.working_folder + args.json

            with open(json_local) as json_file:
                self.general = json.load(json_file)
        else:
            json_local = args.working_folder + args.json.split("/")[-1]

            log.Write(['Downloading json metadata from s3'])

            #pending try / except
            self.general = json.load(boto3.client('s3').get_object(Bucket=args.json_s3, Key=args.json)['Body'])

            #with open(json_local, 'wb') as data:
            #    boto3.client('s3').download_fileobj(args.json_s3, args.json, data)

        #override and validate json parameters
        if args.input != '':        self.general['input']       = args.input

        if args.input_s3 != '':
            self.general['input_s3']    = args.input_s3
        elif 'input_s3' not in self.general:
            self.general['input_s3']    = ''

        if args.output_s3 != '':
            self.general['output_s3']   = args.output_s3
        elif 'output_s3' not in self.general:
            self.general['output_s3']   = ''

        if args.working_folder != '':
            self.general['working_folder']     = args.working_folder
        elif 'working_folder' not in self.general:
            self.general['working_folder']     = ''

        if args.input_s3_url != '':
            self.general['input_s3_url'] = args.input_s3_url

        # new parameter to define parallelism
        if 'output_parallelism' not in self.general:
            self.general['output_parallelism'] = 1

        #identify the input file source
        if  self.general['input_s3_url']    !=  '':
            self.inputtype                  =   's3_url'
        elif self.general['input_s3']       !=  '':
            self.inputtype                  =   's3'
        else:
            self.inputtype = 'local'

        self.rules = []

        for paramrule in self.general["transf_rule"]:
            self.rules.append(TransformationRule(paramrule["offset"],paramrule["size"],paramrule["hex"],paramrule["transf"]))

    def GetLayout(self, _data):
        if len(self.rules) == 0: return self.general['transf']

        for r in self.rules:
            if _data[r.offset:r.end].hex() == r.hexv.lower():
                return self.general[r.transf]

        return self.general['transf']

class TransformationRule:
    def __init__(self, _offset, _size, _hex, _transf):
        self.offset = _offset
        self.size = _size
        self.end = _offset + _size
        self.hexv = _hex
        self.transf = _transf