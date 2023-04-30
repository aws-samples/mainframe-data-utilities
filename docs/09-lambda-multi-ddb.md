# Mainframe Data Utilities V2 (to be refactored)

## Load a DymamoDB table from s3 (from Lambda)

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