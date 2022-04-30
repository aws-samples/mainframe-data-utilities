# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3, utils, urllib3

ddbClient = boto3.client('dynamodb')

class Input:
    def __init__(self, file) -> None:
        log = utils.Log()
        self.obj = True
        self.slice = 0

        if file[:5] == "s3://":
            s3 = utils.S3File(file)
            self.Input = boto3.client('s3').get_object(Bucket=s3.bucket, Key=s3.s3obje)['Body']
        elif file[:8] == "https://":
            http = urllib3.PoolManager()
            self.Input = http.request('GET', file).data
            self.obj = False
        elif file:
            self.Input=open(file,"rb")
        else:
            log.Write(['Input file parameter missing'])
            quit()

    def read(self, lrecl):
        if self.obj:
            return self.Input.read(lrecl)
        else:
            self.slice += lrecl
            return self.Input[self.slice - lrecl :self.slice]
            
class Output:
    def __init__(self, param, req_route='', req_tkn='') -> None:
        
        log = utils.Log()
        self.type = param['output-type']
        self.Deli = param['separator']
        self.rsize = param['req-size']
        self.reqrt = req_route
        self.reqtk = req_tkn
        self.list = []
        self.crlf = ''

        if param['output-type'] == 'file': self.Output=open(param['output'],'w')
            
        elif param['output-type'] == 'ddb':
            self.Record = {}
            self.dsrc = param['output']
            
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

class item:

    def __init__(self, param):
        self.Type   = param['output-type']
        self.Record = {}

        if self.Type == 'file' or self.Type ==  's3-obj': self.Record['row'] = []

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