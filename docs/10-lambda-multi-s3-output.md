# Mainframe Data Utilities V2 (to be refactored)

## Convert from EBCDIC to ASCII when a file is uploaded to s3 (using Lambda)

### Define variables to be used in the next steps
```
bucket=bucket-name
account=account-number
region=region-code
json_s3=layout-bucket
json_pre=layout-prefix/
```

### IAM

From CloudShell or any Linux environment.

Create a working folder:
```
mkdir workdir; cd workdir
```

Create a trust policy:
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

Create a role for your Lambda:
```
aws iam create-role --role-name E2AConvLambdaRole --assume-role-policy-document file://E2ATrustPol.json
```

Create a policy for the role:
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

Put the policy:
```
aws iam put-role-policy --role-name E2AConvLambdaRole --policy-name E2AConvLambdaPolicy --policy-document file://E2AConvLambdaPolicy.json
```

### Lambda and S3 event

Download mainframe data utilities:
```
git clone https://github.com/aws-samples/mainframe-data-utilities.git mdu
```

Create the zip packaged:
```
cd mdu/src; zip -r ../../mdu.zip *; cd ../..
```

Create the Lambda Function:
```
aws lambda create-function \
--function-name E2A \
--runtime python3.10 \
--zip-file fileb://mdu.zip \
--role arn:aws:iam::$account:role/E2AConvLambdaRole \
--timeout 10 \
--handler lambda_function.lambda_handler \
--environment "Variables={json_s3=$bucket,json_pre=$json_pre}"
```

Add the permission to the S3 event:

```
aws lambda add-permission \
--function-name E2A \
--action lambda:InvokeFunction \
--principal s3.amazonaws.com \
--source-arn arn:aws:s3:::$bucket \
--source-account $account \
--statement-id 1
```

Create the S3 event JSON:

```
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
```

Create the S3 event:
```
aws s3api put-bucket-notification-configuration --bucket $bucket --notification-configuration file://S3E2AEvent.json
```

### Run

Create the JSON metadata:
```
python3        mdu/src/mdu.py parse \
               mdu/LegacyReference/COBKS05.cpy \
               CLIENT.json \
-output        output/CLIENT.ASCII.txt \
-output-s3     $bucket \
-output-type   s3 \
-working-folder /tmp/ \
-print         10000 \
-verbose       1
```

Edit the CLIENT.json and replace the `transf_rule` with the following:

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

Upload the CLIENT.json to S3:
```
aws s3 cp CLIENT.json s3://$bucket/layout/CLIENT.json
```

Upload the data file to S3:
```
aws s3 cp mdu/sample-data/CLIENT.EBCDIC.txt s3://$bucket/input/
```


### More use cases

Check the [Read me](/docs/readme.md) page.