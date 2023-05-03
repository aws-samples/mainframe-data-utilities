# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3, urllib3
import multiprocessing as mp
from core.filemeta      import FileMetaData
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

                http = urllib3.PoolManager()
                cont = http.request('GET', fMetaData.general['input_s3_url']).data

            log.Write(['Object lambda not implemented'])

        InpDS = open(inp_temp,"rb")

    log.Write([ '# of threads' , str(fMetaData.general['threads']) ])

    #if fMetaData.general['threads'] == 1:
    #vem por aqui
    #else:

    # prepare for multiprocessing
    lstFiles = []
    dctQueue = {}
    lstProce = []

    for f in range(1, fMetaData.general['threads']+1):
        strOutFile = fMetaData.general['working_folder'] + fMetaData.general['output'] + (str(f) if f > 1 else '')
        lstFiles.append(strOutFile)
        dctQueue[strOutFile] = mp.Queue()
        p = mp.Process(target=queue_worker, args=(log, fMetaData, strOutFile, dctQueue[strOutFile]))
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

def queue_worker(log, fMetaData, OutDs, q):

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