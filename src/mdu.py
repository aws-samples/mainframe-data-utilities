#!/usr/local/bin/python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from core.log import Log
from core.cli import CommandLine
import core.extract as Extract
import core.parsecp as Parsecp

import sys

def main(arg):

    cli = CommandLine()

    log = Log(cli.verbose)

    if cli.args.function == 'extract':
        Extract.FileProcess(log, cli.args)
    elif cli.args.function == 'parse':
        Parsecp.RunParse(log, cli.args)
    else:
        log.Write(['not implemented yet'])

    log.Finish()

if __name__ == '__main__':
    main(sys.argv)