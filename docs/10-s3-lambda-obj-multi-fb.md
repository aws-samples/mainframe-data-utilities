# Mainframe Data Utilities V2

## Convert a multiple layout file using S3 Lambda Object

### Create a working folder

From CloudShell or any Linux environment.

Create a working folder:
```
mkdir workdir; cd workdir
```

### Create variables to simplify next steps
```
bucket=bucket-to-create
access_point=your-access-point-name
account=your-account-number
region=your-region-code
json_pre=s3-prefix-for-layout-file/
```

### IAM

Create a trust policy for the Object Lambda

```
S3OLTrustPolicy=$(cat <<EOF
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
printf "$S3OLTrustPolicy" > S3OLTrustPolicy.json

```

Create the IAM Role

```
aws iam create-role --role-name S3OLRole --assume-role-policy-document file://S3OLTrustPolicy.json
```

Attach the policy

```
S3OLPolicy=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLambdaInvocation",
      "Action": [
        "lambda:InvokeFunction"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:lambda:us-east-1:${account}:function:S3OLConverter:\$LATEST",
      "Condition": {
        "ForAnyValue:StringEquals": {
          "aws:CalledVia": [
            "s3-object-lambda.amazonaws.com"
          ]
        }
      }
    },
    {
      "Sid": "AllowStandardAccessPointAccess",
      "Action": [
        "s3:Get*",
        "s3:List*"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:${region}:${account}:accesspoint/${access_point}/*",
      "Condition": {
        "ForAnyValue:StringEquals": {
          "aws:CalledVia": [
            "s3-object-lambda.amazonaws.com"
          ]
        }
      }
    },
    {
      "Sid": "AllowObjectLambdaAccess",
      "Action": [
        "s3-object-lambda:Get*",
        "s3-object-lambda:List*"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3-object-lambda:${region}:${account}:accesspoint/${bucket}-ascii"
    },
    {
        "Sid": "AllowObjectLambdaWriteResponse",
        "Action": ["s3-object-lambda:WriteGetObjectResponse"],
        "Effect": "Allow",
        "Resource": "*"
    },
    {
        "Sid": "AllowObjectLambdaAccessLayoutBucket",
        "Action": [
            "s3:GetObjectVersion",
            "s3:GetObject"
        ],
        "Effect": "Allow",
        "Resource": [
            "arn:aws:s3:::${bucket}/*",
            "arn:aws:s3:::${bucket}"
        ]
    },
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
    }
  ]
}
EOF
)
printf "$S3OLPolicy" > S3OLPolicy.json

aws iam put-role-policy --role-name S3OLRole --policy-name S3OLPolicy --policy-document file://S3OLPolicy.json
```

Download the source code and create a zip file from it:
```
git clone -b mdu_v2 https://github.com/aws-samples/mainframe-data-utilities.git mdu
cd mdu/src;  zip -r ../../mdu.zip *; cd ../..
```

Create the lambda function:
```
aws lambda create-function \
--function-name S3OLConverter \
--runtime python3.10 \
--zip-file fileb://mdu.zip \
--handler lambda_function.s3_obj_lambda_handler \
--environment "Variables={json_s3=${bucket},json_pre=${json_pre}}" \
--role arn:aws:iam::${account}:role/S3OLRole --timeout 10
```

Create the S3 bucket:
```
aws s3api create-bucket --bucket $bucket
```

Create the S3 Access point:
```
aws s3control create-access-point \
--account-id ${account} \
--bucket ${bucket} \
--name ${access_point}
```


Create the S3 Object Lambda Configuration file:
```
cat <<EOF>> S3OLAP.json
{
    "SupportingAccessPoint" : "arn:aws:s3:us-east-1:${account}:accesspoint/${access_point}",
    "TransformationConfigurations": [{
        "Actions" : ["GetObject"],
        "ContentTransformation" : {
            "AwsLambda": {
                "FunctionArn" : "arn:aws:lambda:us-east-1:${account}:function:S3OLConverter"
            }
        }
    }]
}
EOF

```

Create the S3 Object Lambda Access Point

```
aws s3control create-access-point-for-object-lambda \
--account-id ${account} \
--name ${bucket}-ascii \
--configuration file://S3OLAP.json

```


Upload the layout:
```
aws s3 cp mdu/sample-json/CLIENT-s3-obj.json s3://${bucket}/layout/CLIENT.json
```

Upload the input file:
```
aws s3 cp mdu/sample-data/CLIENT.EBCDIC.txt s3://${bucket}/
```


Download the EBCDIC file already converted to ASCII:

```
aws s3api get-object \
--bucket arn:aws:s3-object-lambda:${region}:${account}:accesspoint/${bucket}-ascii \
--key CLIENT.EBCDIC.txt CLIENT.ASCII.txt
```

### Cleanup
```
aws s3control delete-access-point-for-object-lambda --account-id $account --name $bucket-ascii
aws s3control delete-access-point --account-id $account --name $access_point
aws lambda delete-function --function-name S3OLConverter
aws iam delete-role-policy --role-name S3OLRole --policy-name S3OLPolicy
aws iam delete-role --role-name S3OLRole
```

### More use cases

Check the [main page](/).