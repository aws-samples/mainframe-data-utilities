# Mainframe Data Utilities V2

## Locally convert a multiple layout file and upload to S3

### Pre-requisites
- An S3 bucket already created

### Create a variable for you bucket name
```
bucket=your-bucket-name
```

### Parse a multiple layout copybook

Run the `src/mdu.py` script, using the `parse` function, to convert the copybook file provided in [LegacyReference](/LegacyReference) from Cobol to JSON representation. Use `-output-s3` to inform your bucket name:

```
python3     src/mdu.py parse                \
            LegacyReference/COBKS05.cpy     \
            sample-json/COBKS05-list-s3-out.json \
-input      sample-data/CLIENT.EBCDIC.txt   \
-output-s3  ${bucket}                       \
-output     sample-data/CLIENT.ASCII.txt    \
-threads    2                               \
-print      20 -verbose true
```

### Add the multiple layout conversion rules

2. The step above will generate the [COBKS05-list-s3-out.json](/sample-json/sample-json/COBKS05-list-s3-out.json) with an empty transformation rules list: `"transf_rule"=[],`. Replace the transformation rule with the content bellow and save it:

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

The result of the change above must produce a file like [sample-json/COBKS05-list-s3-out.json](/sample-json/sample-json/COBKS05-list-s3-out.json).

### Extract a multiple layout file

3. Run the `src/mdu.py extract` fucntion to extract the `CLIENT.EBCDIC.txt` into an ASCII file.

```
python3 src/mdu.py extract sample-json/COBKS05-list-s3-out.json
```

4. Check the [CLIENT.ASCII.txt](/sample-data/CLIENT.ASCII.txt) file (and your S3 bucket content).

### More use cases

Check the [main page](/).