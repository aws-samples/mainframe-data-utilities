# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3, json
ddbclient = boto3.client('dynamodb')

class Batch:
    def __init__(self, tbname, rate):
        self.dict = {}
        self.list = []
        self.table = tbname
        self.rate = rate

    def WriteItems(self, item={}):

        if item != {}:
            self.list.append(item)

        if len(self.list) >= self.rate or item == {}:

            response = ddbclient.batch_write_item(RequestItems={ self.table : self.list })
            self.list = []

class item:

    def __init__(self):
        self.dict = {}

    def create(self, id, type, key, keyname, value):
        
        if not key: 
            self.dict[id] = {}
            self.dict[id]['S' if type == "ch" else 'N'] = value
        else:
            if keyname in self.dict:
                self.dict[keyname]['S'] = self.dict[keyname]['S'] + "|" + value
            else:
                self.dict[keyname] = {}
                self.dict[keyname]['S'] = value
    def read(self):
        return self.dict

    def readPutReq(self):
        tmp = {}
        tmp['PutRequest'] = {}
        tmp['PutRequest']['Item'] = self.dict
        return tmp