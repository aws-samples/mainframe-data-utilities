# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3, urllib.request, json
import multiprocessing as mp
from core.ebcdic        import unpack
from core.arg           import ExtractArgs
from itertools          import cycle

def FileProcess(log, ExtArgs: ExtractArgs):

    fMetaData = FileMetaData(log, ExtArgs)

    if fMetaData.inputtype == 'local':

        InpDS = open(fMetaData.general['input'],"rb")

    else:

        log.Write(['Downloading file from s3'])

        inp_temp = local_input(fMetaData.general['wfolder'], fMetaData.general['input'])

        if fMetaData.inputtype == 's3':

            with open(inp_temp, 'wb') as f:
                boto3.client('s3').download_fileobj(fMetaData.general['input-s3'], fMetaData.general['input'], f)

        else:

            urllib.request.urlretrieve(fMetaData.general['input-s3-url'], inp_temp)

            log.Write(['Object lambda not implemented'])

        InpDS = open(inp_temp,"rb")

    # prepare for multiprocessing
    lstFiles = []
    dctQueue = {}
    lstProce = []

    for f in range(1, fMetaData.general['output-parallelism']+1):
        strOutFile = fMetaData.general['wfolder'] + fMetaData.general['output'] + (str(f) if f > 1 else '')
        lstFiles.append(strOutFile)
        dctQueue[strOutFile] = mp.Queue()
        p = mp.Process(target=process_record, args=(fMetaData, strOutFile, dctQueue[strOutFile]))
        p.start()
        lstProce.append(p)

    cyFiles = cycle(lstFiles)

    i=0
    while i < fMetaData.general['max'] or fMetaData.general['max'] == 0:

        record = read(InpDS, fMetaData.general['recfm'], fMetaData.general["lrecl"])

        if not record: break

        i+= 1
        if i > fMetaData.general["skip"]:

            if(fMetaData.general["print"] != 0 and i % fMetaData.general["print"] == 0): log.Write(['Records read', str(i)])

            nxq = next(cyFiles)
            dctQueue[nxq].put(record)

            #process_record(fMetaData, record, OutDs, NewLine)
            #NewLine = '\n'

    # stop /wait for the workers
    for f in lstFiles: dctQueue[f].put(None)
    for p in lstProce:
        p.join()

    log.Write(['Records processed', str(i)])

def process_record(fMetaData, OutDs, q):

    outfile = open(OutDs, 'w')
    newl = ''

    while True:
        record = q.get()
        if record is None:
            outfile.close()
            break

        OutRec = [] if fMetaData.general['output-type'] in ['file', 's3-obj', 's3'] else {}

        layout = fMetaData.GetLayout(record)

        for transf in layout:
            addField(
                fMetaData.general['output-type'],
                OutRec,
                transf['name'],
                transf['type'],
                transf['part-key'],
                fMetaData.general['partkname'],
                transf['sort-key'],
                fMetaData.general['sortkname'],
                unpack(record[transf["offset"]:transf["offset"]+transf["bytes"]], transf["type"], transf["dplaces"], fMetaData.general["rem-low-values"], False ),
                False)

        if fMetaData.general['output-type'] in ['file', 's3-obj', 's3']:

            outfile.write(newl + fMetaData.general['separator'].join(OutRec))
            newl='\n'
        else:
            OutDs.write(str(OutRec) + '\n')

def local_input(wfolder, key):

     return wfolder + key.split("/")[-1]

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
                record[id] = {}
                record[id]['S' if type == "ch" else 'N'] = value
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

    def __init__(self, log, args: ExtractArgs):

        if args.json_s3 == False:
            json_local = (args.wfolder if args.wfolder else '') + args.json

        else:
            log.Write(['Downloading json metadata from s3'])

            json_local = args.wfolder + args.json.split("/")[-1]

            with open(json_local, 'w') as f: boto3.client('s3').download_fileobj(args.json_s3, args.json, f)

        with open(json_local) as json_file:
            self.general = json.load(json_file)

        #override and validate json parameters
        if args.inp:        self.general['input']       = args.inp

        if args.inp_s3:
            self.general['input-s3']    = args.inp_s3
        elif 'input-s3' not in self.general:
            self.general['input-s3']    = False

        if args.out_s3:
            self.general['output-s3']   = args.out_s3
        elif 'output-s3' not in self.general:
            self.general['output-s3']   = False

        if args.wfolder:
            self.general['wfolder']     = args.wfolder
        elif 'wfolder' not in self.general:
            self.general['wfolder']     = ''

        self.general['input-s3-url'] = args.inp_s3url   if args.inp_s3url else False

        # new parameter to define parallelism
        if 'output-parallelism' not in self.general:
            self.general['output-parallelism'] = 1

        #identify the input file source
        if self.general['input-s3-url'] != False and self.general['input-s3-url']   != '':
            self.inputtype = 's3-url'
        if self.general['input-s3']     != False and self.general['input-s3']       != '':
            self.inputtype = 's3'
        else:
            self.inputtype = 'local'

        self.rules = []

        for paramrule in self.general["transf-rule"]:
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