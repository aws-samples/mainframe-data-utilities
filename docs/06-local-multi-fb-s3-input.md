# Mainframe Data Utilities V2

## Locally convert a multiple layout file

### Pre-requisites
- An S3 bucket already created

### Create a variable for you bucket name
```
bucket=your-bucket-name
```
### Upload the input file to S3

```
aws s3 cp sample-data/CLIENT.EBCDIC.txt s3://${bucket}/sample-data/
```
### Parse a multiple layout copybook

Run the `src/mdu.py` script, using the `parse` function, to convert the copybook file provided in [LegacyReference](/LegacyReference) from Cobol to JSON representation:

```
python3     src/mdu.py parse \
            LegacyReference/COBKS05.cpy   \
            sample-json/COBKS05-list-s3.json \
-input      sample-data/CLIENT.EBCDIC.txt \
-input-s3   ${bucket} \
-output     sample-data/CLIENT.ASCII.txt  \
-print      20 -verbose true
```

### Extract a multiple layout file

2. The step above will generate the [COBKS05-list-s3.json](/sample-json/COBKS05-list-s3.json) with an empty transformation rules list: `"transf_rule"=[],`. Replace the transformation rule with the content bellow and save it:

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

The result of the change above must produce a file like [COBKS05-s3-rules.json](/sample-json/COBKS05-list-s3-rules.json).

3. Run the `src/mdu.py extract` fucntion to extract the `CLIENT.EBCDIC.txt` into an ASCII file.

```
python3 src/mdu.py extract sample-json/COBKS05-list-s3.json
```

4. Check the [CLIENT.ASCII.txt](/sample-data/CLIENT.ASCII.txt) file.

### More use cases

Check the [main page](/).