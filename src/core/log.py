# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import datetime

class Log:
    def __init__(self, verbose = False) -> None:
        self.start = datetime.datetime.now()
        if verbose: self.verbose = True
        print(self.start.strftime("%Y-%m-%d %H:%M:%S.%f") ,'|',' | '.join(['started']))

    def Finish(self):
        sec = str((datetime.datetime.now() - self.start).total_seconds())
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,'Seconds', sec)

    def Write (self, content=[]):
        if len(content) > 0:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,'|',' | '.join(content))
        else:
            print("------------------------------------------------------------------")