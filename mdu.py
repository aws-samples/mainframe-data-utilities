#!/usr/local/bin/python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from core.log import Log
from core.arg import CommandLine
import core.extr as  Extract

import sys

def main(arg):
    log = Log()
    cli = CommandLine(log, arg)

    if cli.type == 'extr':

        Extract.FileProcess(log, cli.Extract)

    else:
        log.Write(['not implemented yet'])

    log.Finish()

if __name__ == '__main__':
    main(sys.argv)