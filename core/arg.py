# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json

class CommandLine:

    def __init__(self, l, sysargv):

        self.log = l

        # get the argument descriptions
        with open("core//arg.json", "r") as jsonarg:
            self.desc = json.load(jsonarg)

        # check if any parameter is present
        if len(sysargv) < 2:
            self.show_help()

        # check the first parameter (function)
        if sysargv[1] in self.desc:
            self.valid_func_args = self.desc[sysargv[1]]
        else:
            self.show_help()

        #transform the list into dict.
        args = dict(zip(sysargv[2::2], sysargv[3::2]))

        # check if arguments are valid for the function
        for a in args:
            if a in self.valid_func_args:
                self.log.Write([self.valid_func_args[a], a, args[a]])
            else:
                self.log.Write(['Unknown argument', a, args[a]])

        # validate and process function specific arguments
        if sysargv[1] == 'extract':
            self.extract(args)
        else:
            self.log('not implemented yet')
            quit()

    def extract(self, args):
        # check if any parameter is present
        if len(args) < 1 or (not '-json' in args):
            self.extract_show_help()

        self.type          = 'extr'
        self.Extract       = ExtractArgs(
            args['-json'],
            args['-json-s3']    if '-json-s3'       in args else False,
            args['-input']      if '-input'         in args else False,
            args['-input-s3']   if '-input-s3'      in args else False,
            args['-input-s3ol'] if '-input-s3ol'    in args else False,
            args['-output']     if '-output'        in args else False,
            args['-output-s3']  if '-output-s3'     in args else False
        )

    def show_help(self, content=[]):
        self.log.Write(['Usage: python3 mdu.py [parsecopy | extract]'])
        self.log.Write(content)
        quit()

    def extract_show_help(self, content=[]):
        self.log.Write(['Usage: python3 mdu.py extract -json path/to/layout.json [-json-s3 buketname] [-inp path/to/input-file] [-inp-s3 input-bucketname] '])
        self.log.Write(content)
        quit()

class ExtractArgs:
    def __init__(self, json, json_s3 = False, inp = False, inp_s3 = False, inp_s3url = False, out = False, out_s3 = False, wfolder = False, route = False, token = False):
        self.json      = json
        self.json_s3   = json_s3
        self.inp       = inp
        self.inp_s3    = inp_s3
        self.inp_s3url = inp_s3url
        self.out       = out
        self.out_s3    = out_s3
        self.wfolder   = wfolder
        self.route     = route
        self.token     = token