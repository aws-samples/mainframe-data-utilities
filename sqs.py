# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3

sqs = boto3.resource('sqs')

class Batch:
    def __init__(self, rate, queue_name):
        self.entries = []
        self.rate = rate
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)              

    def send_message(self, message_body={}, id = 0, message_attributes={}):
        if id != 0:
            self.entries.append (
                {
                    'Id': str(id),
                    'MessageBody': message_body
                }
            )

        if len(self.entries) >= self.rate or id == 0:
            response = self.queue.send_messages(Entries=self.entries)
            self.entries = []