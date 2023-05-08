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

def s3_obj_lambda_handler(event, context):

    request_route = event["getObjectContext"]["outputRoute"]
    request_token = event["getObjectContext"]["outputToken"]
    s3_url        = event["getObjectContext"]["inputS3Url"]
    key           = event['userRequest']['url']

    json = json_pre + key.split('/')[-1].split('.')[0] + '.json'

    cli = CommandLine(
        [
        'extract', json,
        '-json-s3', json_s3,
        '-input-s3-url', s3_url,
        '-input-s3-route', request_route,
        '-input-s3-token', request_token
        ]
        )

    log = Log(cli.verbose)

    Extract.FileProcess(log, cli.args)

    return {'statusCode': 200}