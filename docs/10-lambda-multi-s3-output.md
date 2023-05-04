# Mainframe Data Utilities V2 (to be refactored)

## Convert from EBCDIC to ASCII when a file is uploaded to s3 (using Lambda)

### Variables
```
bucket=bucket-name
account=account-number
region=region-code
json_s3=layout-bucket
json_pre=layout-prefix/
```

### CloudShell

Create a working fodler
```
mkdir workdir; cd workdir
```

Create a trust policy

```
E2ATrustPol=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
)
printf "$E2ATrustPol" > E2ATrustPol.json
```
Create a role for your Lambda
```
aws iam create-role --role-name E2AConvLambdaRole --assume-role-policy-document file://E2ATrustPol.json
```

Create a policy for the role
```
E2APolicy=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Logs",
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "logs:CreateLogGroup"
            ],
            "Resource": [
                "arn:aws:logs:*:*:log-group:*",
                "arn:aws:logs:*:*:log-group:*:log-stream:*"
            ]
        },
        {
            "Sid": "S3",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:GetObjectVersion"
            ],
            "Resource": [
                "arn:aws:s3:::%s/*",
                "arn:aws:s3:::%s"
            ]
        }
    ]
}
EOF
)
printf "$E2APolicy" "$bucket" "$bucket" > E2AConvLambdaPolicy.json
```

Put the policy

```
aws iam put-role-policy --role-name E2AConvLambdaRole --policy-name E2AConvLambdaPolicy --policy-document file://E2AConvLambdaPolicy.json
```

Download mdu:
```
git clone https://github.com/aws-samples/mainframe-data-utilities.git mdu

cd mdu/src; zip -r ../../mdu.zip *; cd ../..
```

aws lambda create-function \
--function-name E2A \
--runtime python3.10 \
--zip-file fileb://mdu.zip \
--role arn:aws:iam::$account:role/E2AConvLambdaRole \
--timeout 10 \
--handler lambda_function.lambda_handler \
--environment "Variables={json_s3=$bucket,json_pre=$json_pre}"


aws lambda add-permission \
--function-name E2A \
--action lambda:InvokeFunction \
--principal s3.amazonaws.com \
--source-arn arn:aws:s3:::$bucket \
--source-account $account \
--statement-id 1

S3E2AEvent=$(cat <<EOF
{
"LambdaFunctionConfigurations": [
    {
      "Id": "E2A",
      "LambdaFunctionArn": "arn:aws:lambda:%s:%s:function:E2A",
      "Events": [ "s3:ObjectCreated:Put" ],
      "Filter": {
        "Key": {
          "FilterRules": [
            {
              "Name": "prefix",
              "Value": "input/"
            }
          ]
        }
      }
    }
  ]
}
EOF
)
printf "$S3E2AEvent" "$region" "$account" > S3E2AEvent.json

aws s3api put-bucket-notification-configuration --bucket $bucket --notification-configuration file://S3E2AEvent.json

python3        mdu/src/mdu.py parse \
               mdu/LegacyReference/COBKS05.cpy \
               CLIENT.json \
-output        /output/CLIENT.ASCII.txt \
-output-s3     $bucket \
-output-type   s3 \
-working-folder /tmp/ \
-print         10000 \
-verbose       1

Edit the CLIENT.json

```
"transf_rule": [
{
"offset": 4,
"size": 2,
"hex": "0002",
"transf": "transf1"
},
{
"offset": 4,
"size": 2,
"hex": "0000",
"transf": "transf2"
}
],
```

aws s3 cp CLIENT.json s3://$bucket/layout/CLIENT.json

aws s3 cp mdu/sample-data/CLIENT.EBCDIC.txt s3://$bucket/input/


### Prepare the bucket to receive the EBCDIC file

1. Create an S3 bucket.
2. Create the folder that will receive the input EBCDIC data file.
3. Create a `layout/` folder inside the bucket/folder previously created.
4. Rename the [sample-data/COBKS05-ddb-s3.json](sample-data/COBKS05-ddb-s3.json) to `CLIENT.json`
5. Remove the `input` key inside the CLIENT.json file and upload it to the `/layout` folder.

### Create the Lambda function

1. Create a Python 3.8+ Lambda function and assign a role with the below permissions:
   * Read access to the source data S3 bucket
   * Write access to the target DynamoDb table
   * Write access to CloudWatch logs
2. Create a zip file with the Python code and upload it into the Lambda function
   ```
   zip mdu.zip *.py
   ```
3. Change the Lambda funcion 'Handler' from `lambda_function.lambda_handler` to `extract_ebcdic_to_ascii.lambda_handler` under the Runtime settings section.
4. Create a new Lambda test event with the contens of `sample-data/CLIENT-TEST.json`
5. Replace the `your-bucket-name` by the bucket name created on step 1 and trigger the event.
6. Change the timeout to 10 seconds under General configuration.
7. Trigger the test.

### Create the S3 event

1. Select the bucket.
2. Select properties.
3. Select 'Create Event Notification' under the Event notifications section.
4. Type a name.
5. Select the 'Put' event type
6. And the lambda function in the Destination section.

### For another use cases

Check the [Read me](/docs/readme.md) page.