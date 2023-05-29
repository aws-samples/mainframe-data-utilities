# Mainframe Data Utilities V2  <- current

## Load a DymamoDB table from local disk

### Create the DynamoDB table

1. Create the DynanamoDb table which will be loaded on next steps. In this example we defined `CLIENT` as the table name, `CLIENT_ID` as its partition key, and CLIENT-R-TYPE as its sort key.

```
aws dynamodb create-table \
--table-name CLIENT \
--attribute-definitions AttributeName=CLIENT_ID,AttributeType=S AttributeName=CLIENT_R_TYPE,AttributeType=S  \
--key-schema AttributeName=CLIENT_ID,KeyType=HASH AttributeName=CLIENT_R_TYPE,KeyType=RANGE \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

2. Check the status of the table creation:

```
aws dynamodb describe-table --table-name CLIENT | grep TableStatus
```

### Parse the copybook

Run the `mdu.py parse` function to convert the [COBKS05.cpy](/LegacyReference/COBKS05.cpy) copybook file provided in [LegacyReference](/LegacyReference/COBKS05.cpy) from Cobol to JSON representation.

 1. Inform `ddb` on `-output-type`.
 2. Inform the DynamoDB table name (created before) on `-output`.
 3. Inform the DynamoDB table partition key name on `-part-k-name`.
 4. Inform the DynamoDB table partition key size (as it is in the EBCDIC file) on `-part-k-len`.
 5. Inform the DynamoDB table sort key name on `-sort-k-name`.
 6. Inform the DynamoDB table sort key size (as it is in the EBCDIC file) on `-sort-k-len`.

```
python3      src/mdu.py parse              \
             LegacyReference/COBKS05.cpy   \
             sample-json/COBKS05-ddb.json  \
-input       sample-data/CLIENT.EBCDIC.txt \
-output      CLIENT                        \
-part-k-len  4                             \
-part-k-name CLIENT_ID                     \
-sort-k-len  2                             \
-sort-k-name CLIENT_R_TYPE                 \
-output-type ddb                           \
-req-size    25                            \
-print       20
```
### Set the transformatiom rules

The step above will generate the [COBKS05-ddb.json](sample-json/COBKS05-ddb.json) with empty transformation rules: `"transf_rule"=[],`. Replace the transformation rule with the content bellow and save it. Example: [COBKS05-ddb-rules.json](sample-json/COBKS05-ddb-rules.json):

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

### Load the data into the CLIENT Dynamodb table

1. Run the `mdu.py extract` to extract the [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) and load into the `CLIENT` Dynamodb table in the ASCII encoding.

```
python3 src/mdu.py extract sample-json/COBKS05-ddb.json
```

### More use cases

Check the [main page](/).