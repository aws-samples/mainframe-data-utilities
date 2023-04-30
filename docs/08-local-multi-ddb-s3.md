# Mainframe Data Utilities V2 (to be refactored)

## Load a DymamoDB table from s3 (locally triggered)

### Update the copybook parsed json file

Create a copy of the [COBKS05-ddb.json](sample-data/COBKS05-ddb.json) file and change the `input` parameter. An example is available in [COBKS05-ddb-s3.json](sample-data/COBKS05-ddb-s3.json).

From: `"input": "sample-data/CLIENT.EBCDIC.txt",`

To: `"input": "s3://your-bucket-name/yourfolder/CLIENT.EBCDIC.txt",`

### Trigger the data load

1. Run `extract_ebcdic_to_ascii.py` to extract the [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) and load into the `CLIENT` Dynamodb table in the ASCII encoding.

```
python3 extract_ebcdic_to_ascii.py -local-json sample-data/COBKS05-ddb-s3.json
```