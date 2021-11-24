# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

class DDB:

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