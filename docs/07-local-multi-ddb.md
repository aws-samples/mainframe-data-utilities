# Mainframe Data Utilities V2 (to be refactored)

## Load a DymamoDB table from local disk

### Create the DynamoDB table

1. Create the DynanamoDb table which will be loaded on next steps. In this example we defined `CLIENT` as the table name, `CLIENT-ID` as its partition key, and CLIENT-R-TYPE as its sort key.

```
aws dynamodb create-table --table-name CLIENT --attribute-definitions AttributeName=CLIENT-ID,AttributeType=S AttributeName=CLIENT-R-TYPE,AttributeType=S  --key-schema AttributeName=CLIENT-ID,KeyType=HASH AttributeName=CLIENT-R-TYPE,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

2. Check the status of the table creation:

```
aws dynamodb describe-table --table-name CLIENT | grep TableStatus
```

### Parse the copybook

Run the `parse_copybook_to_json.py` script to parse the [COBKS05](LegacyReference/COBKS05.cpy) copybook file provided in `sample-data`.

 1. Inform `ddb` on `-output-type`.
 2. Inform the DynamoDB table name (created before) on `-ascii`.
 3. Inform the DynamoDB table partition key name on `-part-k-name`.
 4. Inform the DynamoDB table partition key size (as it is in the EBCDIC file) on `-part-k-len`.
 5. Inform the DynamoDB table sort key name on `-sort-k-name`.
 6. Inform the DynamoDB table sort key size (as it is in the EBCDIC file) on `-sort-k-len`.

```
python3      parse_copybook_to_json.py     \
-copybook    LegacyReference/COBKS05.cpy   \
-output      sample-data/COBKS05-ddb.json \
-ebcdic      sample-data/CLIENT.EBCDIC.txt \
-ascii       CLIENT                        \
-part-k-len  4                             \
-part-k-name CLIENT-ID                     \
-sort-k-len  2                             \
-sort-k-name CLIENT-R-TYPE                 \
-output-type ddb                           \
-print    20
```
### Set the transformatiom rules

The step above will generate the [COBKS05-ddb.json](sample-data/COBKS05-ddb.json) with empty transformation rules: `"transf-rule"=[],`. Replace the transformation rule with the content bellow and save the `COBKS05-ddb-rules.json`:

```
 "transf-rule": [
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

### Load the data into the CLIENT Dynamodb table

1. Run `extract_ebcdic_to_ascii.py` to extract the [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) and load into the `CLIENT` Dynamodb table in the ASCII encoding.

```
python3 extract_ebcdic_to_ascii.py -local-json sample-data/COBKS05-ddb-rules.json
```


### Update the copybook parsed json file

Create a copy of the [COBKS05-ddb.json](sample-data/COBKS05-ddb.json) file and change the `input` parameter. An example is available in [COBKS05-ddb-s3.json](sample-data/COBKS05-ddb-s3.json).

From: `"input": "sample-data/CLIENT.EBCDIC.txt",`

To: `"input": "s3://your-bucket-name/yourfolder/CLIENT.EBCDIC.txt",`

### Trigger the data load

1. Run `extract_ebcdic_to_ascii.py` to extract the [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) and load into the `CLIENT` Dynamodb table in the ASCII encoding.

```
python3 extract_ebcdic_to_ascii.py -local-json sample-data/COBKS05-ddb-s3.json
```

### For another use cases

Check the [Read me](/docs/readme.md) page.