# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3, urllib3
import multiprocessing as mp
from core.filemeta      import FileMetaData
from core.ebcdic        import unpack
from itertools          import cycle
from botocore.exceptions import ClientError
from pathlib            import Path

def FileProcess(log, ExtArgs):

    # Download the output file
    fMetaData = FileMetaData(log, ExtArgs)

    if fMetaData.inputtype == 'local':

        InpDS = open(fMetaData.general['input'],"rb")

    else:

        inp_temp = fMetaData.general['working_folder'] + fMetaData.general['input'].split("/")[-1]

        if fMetaData.inputtype == 's3':

            log.Write(['Downloading file from s3', inp_temp])

            #try except missing
            with open(inp_temp, 'wb') as f:
                boto3.client('s3').download_fileobj(fMetaData.general['input_s3'], fMetaData.general['input'], f)

        else:
            log.Write(['Downloading file from s3 url'])

            http = urllib3.PoolManager()

            resp = http.request('GET', fMetaData.general['input_s3_url'])

            with open(inp_temp, 'wb') as f:
                f.write(resp.data)

        InpDS = open(inp_temp,"rb")

    log.Write([ '# of threads' , str(fMetaData.general['threads']) ])

    # Open the output file if single trheaded
    if fMetaData.general['threads'] == 1:

        if fMetaData.general['output_type'] in ['file', 's3_obj', 's3']:

            log.Write(['Creating output file', fMetaData.general['working_folder'], fMetaData.general['output']])

            folder = Path(fMetaData.general['working_folder'] + fMetaData.general['output']).parent

            Path(folder).mkdir(parents=True, exist_ok=True)

            outfile = open(fMetaData.general['working_folder'] + fMetaData.general['output'], 'w')
            newl = ''
        else:
            outfile = []

    # Create threads if multi threaded
    else:
        lstFiles = []
        dctQueue = {}
        lstProce = []

        for f in range(1, fMetaData.general['threads']+1):

            strOutFile = fMetaData.general['working_folder'] + fMetaData.general['output'] + "." + str(f)

            lstFiles.append(strOutFile)

            dctQueue[strOutFile] = mp.Queue()

            p = mp.Process(target=queue_worker, args=(log, fMetaData, strOutFile, dctQueue[strOutFile], '.' + str(f)))

            p.start()

            lstProce.append(p)

        cyFiles = cycle(lstFiles)

    # Process each input record
    i=0
    newl=''
    while i < fMetaData.general['max'] or fMetaData.general['max'] == 0:

        record = read(InpDS, fMetaData.general['input_recfm'], fMetaData.general["input_recl"])

        if not record: break

        i+= 1
        if i > fMetaData.general["skip"]:

            if(fMetaData.general["print"] != 0 and i % fMetaData.general["print"] == 0): log.Write(['Records read', str(i)])

            if fMetaData.general['threads'] == 1:
                r = write_output(log, fMetaData, outfile, record, newl)
                if r: newl='\n'
            else:
                nxq = next(cyFiles)
                dctQueue[nxq].put(record)

    if fMetaData.general['threads'] == 1:
        close_output(log, fMetaData, outfile, fMetaData.general['working_folder'] + fMetaData.general['output'])
    else:
        # stop /wait for the workers
        for f in lstFiles: dctQueue[f].put(None)
        for p in lstProce: p.join()

    log.Write(['Records processed', str(i)])

def write_output(log, fMetaData, outfile, record, newl):

    OutRec = [] if fMetaData.general['output_type'] in ['file', 's3-obj', 's3'] else {}

    layout = fMetaData.Layout(record)

    if layout != 'discard':

        for transf in fMetaData.general[layout]:
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
        else:
            outfile.append({'PutRequest' : { 'Item' : OutRec }})

            if len(outfile) >= fMetaData.general['req_size']:
                ddb_write(log, fMetaData.general['output'], outfile)
                outfile.clear()
        return True
    return False

def ddb_write(log, table, data):
    log.Write(['Updating DynamoDB', str(len(data))])
    response = boto3.client('dynamodb').batch_write_item(RequestItems={ table : data })

def close_output(log, fMetaData, outfile, OutDs, strSuff = ''):

    if fMetaData.general['output_type'] in ['file', 's3_obj', 's3']:

        outfile.close()

        if fMetaData.general['output_s3'] != '':

            log.Write(['Uploading to s3',  fMetaData.general['output_s3'], fMetaData.general['output'] + strSuff])

            if fMetaData.general['verbose']: log.Write(['Source file', OutDs])

            try:
                response = boto3.client('s3').upload_file(OutDs, fMetaData.general['output_s3'], fMetaData.general['output'] + strSuff)

            except ClientError as e:
                log.Write(e)

        elif fMetaData.general['input_s3_url'] != '':

            log.Write(['Generating s3 lambda object response'])

            # try/except missing
            with open(OutDs, 'rb') as f:
                boto3.client('s3').write_get_object_response(Body=f,RequestRoute=fMetaData.general['input_s3_route'],RequestToken=fMetaData.general['input_s3_token'])

    else:
        if len(outfile) >= 0: ddb_write(log, fMetaData.general['output'], outfile)

def queue_worker(log, fMetaData, OutDs, q, strSuf = ''):

    if fMetaData.general['output_type'] in ['file', 's3_obj', 's3']:
        outfile = open(OutDs, 'w')
    else:
        outfile = []

    newl = ''

    while True:
        record = q.get()

        if record is not None:
            r = write_output(log, fMetaData, outfile, record, newl)
            if r: newl='\n'
        else:
            log.Write(['Closing output', fMetaData.general['output'], 'thread', strSuf])
            close_output(log, fMetaData, outfile, OutDs, strSuf)
            break

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