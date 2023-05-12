# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3, utils as utils, urllib3

ddbClient = boto3.client('dynamodb')

class Input:

    def __init__(self, general) -> None:
        log = utils.Log()
        self.localfile = True
        self.slice = 0
        self.recfm = general['recfm'] if 'recfm' in general else 'fb'

        file = general["input"]

        if file[:5] == "s3://":
            s3 = utils.S3File(file)
            self.Input = boto3.client('s3').get_object(Bucket=s3.bucket, Key=s3.s3obje)['Body']

        elif file[:8] == "https://":
            http = urllib3.PoolManager()
            self.Input = http.request('GET', file).data
            self.localfile = False

        elif file:
            self.Input=open(file,"rb")
        else:
            log.Write(['Input file parameter missing'])
            quit()

    def read(self, lrecl):
        if self.localfile:
            if self.recfm == 'fb':
                return self.Input.read(lrecl)
            else:
                l = self.getRDW(self.Input.read(4))
                return self.Input.read(l)
        else:
            if self.recfm == 'fb':
                self.slice += lrecl
                return self.Input[self.slice - lrecl :self.slice]
            else:
                self.slice += 4
                l = self.getRDW(self.Input[self.slice - lrecl :self.slice])
                self.slice += l
                return self.Input[self.slice - l :self.slice]

    def getRDW(self, b: bytearray):
        return int("0x" + b[:2].hex(), 0) - 4 if len(b) > 0 else 0

class Output:
    def __init__(self, param, req_route='', req_tkn='', tmp='') -> None:

        log = utils.Log()
        self.type = param['output-type']
        self.Deli = param['separator']
        self.rsize = param['req-size']
        self.dsrc = param['output']
        self.s3key = param['output-s3key'] if 'output-s3key' in param else param['output']
        self.s3bkt = param['output-s3bkt'] if 'output-s3bkt' in param else ''
        self.reqrt = req_route
        self.reqtk = req_tkn
        self.tmpfd = tmp
        self.list = []
        self.crlf = ''

        if param['output-type'] == 'file' or param['output-type'] == 's3':
            self.Output=open(self.tmpfd + self.dsrc, 'w')
        elif param['output-type'] == 'ddb':
            self.Record = {}

    def Write(self, item={}):

        if item != {}:
            if self.type == 'ddb':
                self.list.append(item)
            else:
                self.list.append(self.Deli.join(item['row']))

        if (len(self.list) >= self.rsize) or (len(self.list) > 0  and item == {}):
            if self.type == 'ddb':
                response = ddbClient.batch_write_item(RequestItems={ self.dsrc : self.list })
                self.list = []
            elif self.type == 's3-obj':
                if item == {}:
                    s3 = boto3.client('s3')
                    s3.write_get_object_response(Body=('\n'.join(self.list)),RequestRoute=self.reqrt,RequestToken=self.reqtk)
            else:
                self.Output.write(self.crlf + '\n'.join(self.list))
                self.crlf = '\n'
                self.list = []
                if item == {} and self.type == 's3':
                    self.Output.close()
                    boto3.client('s3').put_object(Body=open(self.tmpfd + self.dsrc,'rb'), Bucket=self.s3bkt, Key=self.s3key)

class item:

    def __init__(self, param):
        self.Type   = param['output-type']
        self.Record = {}

        if self.Type in ['file', 's3-obj', 's3'] : self.Record['row'] = []

    def addField(self, id, type, partkey, partkname, sortkey, sortkname, value, addempty = False):

        if self.Type == 'ddb' or self.Type == 'sqs':

            if not partkey and not sortkey:
                if value != '' or addempty:
                    self.Record[id] = {}
                    self.Record[id]['S' if type == "ch" else 'N'] = value
            elif not partkey:
                if sortkname in self.Record:
                    self.Record[sortkname]['S'] = self.Record[sortkname]['S'] + "|" + value
                else:
                    self.Record[sortkname] = {}
                    self.Record[sortkname]['S'] = value
            else:
                if partkname in self.Record:
                    self.Record[partkname]['S'] = self.Record[partkname]['S'] + "|" + value
                else:
                    self.Record[partkname] = {}
                    self.Record[partkname]['S'] = value
        else:
            self.Record['row'].append(value)

    def dump(self):
        return self.Record

    def get(self):
        if self.Type == 'ddb' or self.Type == 'sqs':
            tmp = {}
            tmp['PutRequest'] = {}
            tmp['PutRequest']['Item'] = self.Record
            return tmp
        else:
            return  self.Record