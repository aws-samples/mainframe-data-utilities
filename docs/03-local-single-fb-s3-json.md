# Mainframe Data Utilities V2

## Locally convert a single layout FB file, reading a JSON metadata from S3

### Convert the JSON metadata to an S3 file

Upload the [cobpack2-list.json](/sample-json/cobpack2-list.json) metadata created in the [Locally convert a single layout FB file](/docs/02-local-single-fb.md) procedure to your `s3 bucket`.

```
aws s3 cp sample-json/cobpack2-list.json s3://<your-bucket-name>/cobpack2-list.json
```

### Convert the local file

Run the `extract` function to convert the `COBPACK.OUTFILE.txt` EBCDIC file into an ASCII file.

```
python3 src/mdu.py extract cobpack2-list.json -json-s3 <your-bucket-name>
```

The generated ASCCI file will match the provided [COBPACK.ASCII.txt](/sample-data/COBPACK.ASCII.txt).

### More use cases

Check the [Read me](/docs/readme.md) page.