# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import boto3

class FileMetaData:

    def __init__(self, log, args):

        if args.json_s3 == '':
            json_local = args.working_folder + args.json

            with open(json_local) as json_file:
                self.general = json.load(json_file)
        else:
            json_local = args.working_folder + args.json.split("/")[-1]

            log.Write(['Downloading json metadata from s3', args.json_s3, args.json])

            #pending try / except
            self.general = json.load(boto3.client('s3').get_object(Bucket=args.json_s3, Key=args.json)['Body'])

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
            self.general['working_folder']          = args.working_folder
            if self.general['working_folder'][-1]  != '/': self.general['working_folder'] += '/'
        elif 'working_folder' not in self.general:
            self.general['working_folder']          = ''

        if args.input_s3_url != '':
            self.general['input_s3_url']   = args.input_s3_url
            self.general['input_s3_route'] = args.input_s3_route
            self.general['input_s3_token'] = args.input_s3_token
        else:
            self.general['input_s3_url'] = ''

        # new parameter to define parallelism
        if 'threads' not in self.general:
            self.general['threads'] = 1

        #identify the input file source
        if  self.general['input_s3_url']    !=  '':
            self.inputtype                  =   's3_url'
        elif self.general['input_s3']       !=  '':
            self.inputtype                  =   's3'
        else:
            self.inputtype = 'local'

        self.rules = []

        for paramrule in self.general['transf_rule']:
            self.rules.append(TransformationRule(
                paramrule['offset'],
                paramrule['size'],
                paramrule['hex'],
                paramrule['transf'],
                paramrule['skip'] if 'skip' in paramrule else False
                )
            )

    def GetLayout(self, _data):
        if len(self.rules) == 0: return self.general['transf']

        for r in self.rules:
            if _data[r.offset:r.end].hex() == r.hexv.lower():
                return self.general[r.transf]

        return self.general['transf']

    def Layout(self, _data):
        if len(self.rules) == 0: return 'transf'

        for r in self.rules:
            if _data[r.offset:r.end].hex() == r.hexv.lower():
                return r.transf

        return 'transf'

class TransformationRule:
    def __init__(self, _offset, _size, _hex, _transf, _skip):
        self.offset = _offset
        self.size = _size
        self.end = _offset + _size
        self.hexv = _hex
        self.transf = _transf
        self.skip = _skip