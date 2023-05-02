# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
import os
import core.extract as Extract
from   core.log import Log
from   core.cli import CommandLine

json_s3 = os.environ.get('json_s3')
json_pre = os.environ.get('json_pre')

def lambda_handler(event, context):

    bkt =  event['Records'][0]['s3']['bucket']['name']
    key =  event['Records'][0]['s3']['object']['key']

    json = json_pre + key.split('/')[-1].split('.')[0] + '.json'

    cli = CommandLine(
        [
        'extract', json,
        '-json-s3', json_s3,
        '-input', key,
        '-input-s3', bkt
        ]
    )

    # -output and -output-s3 can be added to override the JSON content.

    log = Log(cli.verbose)

    Extract.FileProcess(log, cli.args)

    return {'statusCode': 200}