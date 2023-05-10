# Mainframe Data Utilities

| :exclamation:  Mainframe Data Utilities v2 documentation available at [Readme](/) |
|-----------------------------------------|

Table of contents
=================
* Security
* License
* About
* Status
* Requirements
* Limitations
* Getting started
* Multiple layout support
* Load a DymamoDB table from local disk
* Load a DymamoDB table from s3 (locally triggered)
* Load a DymamoDB table from s3 (using Lambda)
* How it works
* LegacyReference
* Do you want to help?

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

## About

Mainframe Data Utilities is an AWS Sample written in Python.

The purpose of this project is to provide Python scripts as a starting point for those who need to handle EBCDIC files transferred from mainframes and AS/400 platforms to AWS or any distributed environment.

The current release of this toolset consists of three scripts:

- **parse_copybook_to_json** is a module that creates a JSON parameter file by parsing Cobol Copybook. The parameter file is a description of the file EBCDIC file layout, required by extract_ebcdic_to_ascii.py

- **extract_ebcdic_to_ascii.py** uses the JSON parameter file to slice a fixed length EBCDIC file, unpack its contents and write them to an ASCII file.

- **ebcdic.py** is the main library that handles the encoding transformation logic.

- **copybook.py** is the main library that generates a Python dictionary from COBOL copybooks.

## Status

Stable

## Requirements

Make sure [Python](https://www.python.org/downloads/) 3.8 or above is installed.

## Limitations

1. File layouts defined inside Cobol programs are not supported.
2. Packing statement is ignored when defined before the PIC clause.
3. The file's logical record length is the sum of all field sizes. This means that in some cases the calculation may result in a size that is smaller than the physical file definition.
4. The `REDEFINES` statement for **data items**, it's only supported for **group items**.

## Getting started

### Parsing a basic copybook

1. Clone this repo:

```
git clone git@github.com:aws-samples/mainframe-data-utilities.git.
```

2. Run the `parse_copybook_to_json.py` script to parse the [COBPACK2](LegacyReference/COBPACK2.cpy) copybook file provided in `sample-data`.

```
python3      parse_copybook_to_json.py       \
-copybook    LegacyReference/COBPACK2.cpy    \
-output      sample-data/cobpack2-list.json  \
-dict        sample-data/cobpack2-dict.json  \
-ebcdic      sample-data/COBPACK.OUTFILE.txt \
-ascii       sample-data/COBPACK.ASCII.txt   \
-print       10000
```

### Extracting ebcdic data to a delimiter-separated ASCII file

3. Run `extract_ebcdic_to_ascii.py`to extract the `COBPACK.OUTFILE.txt` EBCDIC file into an ASCII file.

```
python3 extract_ebcdic_to_ascii.py -local-json sample-data/cobpack2-list.json
```

4. The generated ASCCI file must martch the provided [COBPACK.ASCII.txt](sample-data/COBPACK.ASCII.txt).

## Multiple layout support

There are often multiple layouts in mainframe VSAM or sequential (flat) files. It means that you need a different transformation rule depending on the row you are reading.

The REDEFINES statement allows multiple layouts declaration in the COBOL language.

### Parsing a multiple layout copybook

The [COBKS05.cpy](LegacyReference/COBKS05.cpy) is provided in [LegacyReference](LegacyReference/) folder as an example of a VSAM file copybook having three record layouts. The [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) is the EBCDIC sample that can be converted through the following steps.

1. Run the `parse_copybook_to_json.py` script to parse the copybook file provided in `sample-data`.

```
python3   parse_copybook_to_json.py     \
-copybook LegacyReference/COBKS05.cpy   \
-output   sample-data/COBKS05-list.json \
-dict     sample-data/COBKS05-dict.json \
-ebcdic   sample-data/CLIENT.EBCDIC.txt \
-ascii    sample-data/CLIENT.ASCII.txt  \
-print    20
```

### Extracting a multiple layout file

2. The step above will generate the [COBKS05-list.json](sample-data/COBKS05-list.json) with empty transformation rules: `"transf-rule"=[],`. Replace the transformation rule with the content bellow and save the `COBKS05-list.json`:

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

The parameters above will inform the `extract_ebcdic_to_ascii.py` script that records having "0002" hexadecimal value between its 5th and 6th bytes must be converted through the layout specified in "transf1" layout, whereas records that contain "0000" at the same position will be extracted with the "transf2" layout.

The result of the change above must produce a file like [COBKS05-rules.json](sample-data/COBKS05-rules.json).

3. Run `extract_ebcdic_to_ascii.py` to extract the `CLIENT.EBCDIC.txt` into an ASCII file.

```
python3 extract_ebcdic_to_ascii.py -local-json sample-data/COBKS05-list.json
```

4. Check the [CLIENT.ASCII.txt](sample-data/CLIENT.ASCII.txt) file.

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

## Load a DymamoDB table from s3 (using Lambda)

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

## VB record format files

python3 parse_copybook_to_json.py -copybook LegacyReference/COBVBFM2.cpy -output sample-data/COBVBFM2-list.json -ebcdic sample-data/COBVBFM2.EBCDIC.txt -ascii sample-data/COBVBFM2.ASCII.txt -recfm vb

python3 extract_ebcdic_to_ascii.py -local-json sample-data/COBVBFM2-list.json

## File split

python3 split_ebcdic_file.py -local-json sample-data/COBKS05-split-local.json

## How it works

### parse_copybook_to_json

Mainframe files are typically packed (into decimal and binary formats), and encoded in EBCDIC.

To make the extraction possible it's important to slice the source file according to its layouts and data types. This module is an automation that reads the file's layout from a Cobol copybook and creates a JSON file that holds the information required to interpret and extract the data from the source file.

#### Arguments

The arguments below are supported by this function:

|Parameter  |Type    |Description                                                                    |
|-----------|--------|-------------------------------------------------------------------------------|
| -copybook |Required| Path of the copybook file to be processed                                     |
| -output   |Required| Path of the JSON file to be generated                                         |
| -ebcdic   |Optional| Informs the name of the ebcdic file that will be processed by the next script |
| -ascii    |Optional| Informs the name of the ascii  file that will be processed by the next script |
| -print    |Optional| Changes the print frequency of the next script                                |
| -dict     |Optional| Generates output nested JSON file to be used as a documentation               |

#### Output

This script generates a JSON file that holds **general parameters** and **layout transformation parameters** as its output.

|Parameter      |Description                                           |
|---------------|------------------------------------------------------|
|input          |Name of the input EBCDIC file to be extracted         |
|output         |Name of the output ASCII file to be generated         |
|max            |Max number of records to be extracted                 |
|skip           |Number of records to be skipped                       |
|print          |Number of records before print status                 |
|lrecl          |Logical record length of the ebcdic file              |
|rem-low-values |Remove null chars                                     |
|separator      |Char to add between fields to separate them           |
|transf-rule    |Rules for layout section within a multi-layout file  |
|transf         |List of the transformation fields (layout)            |
|transf.type    |type of the field to be transformed                   |
|transf.bytes   |Size in bytes of the field to be transformed          |
|transf.name    |Name of the field to be transformed                   |

Sample:
```
   "input": "extract-ebcdic-to-ascii/COBPACK.OUTFILE.txt",
   "output": "extract-ebcdic-to-ascii/COBPACK.ASCII.txt",
   "max": 0,
   "skip": 0,
   "print": 10000,
   "lrecl": 150,
   "rem-low-values": true,
   "separator": "|",
   "transf-rule": [],
   "transf": [
      {
         "type": "ch",
         "bytes": 19,
         "name": "OUTFILE-TEXT"
      }
```

The length is represented in bytes. An 18-digit integer field, for instance, only takes 10 bytes. For more information check [IBM Computational items documentation](https://www.ibm.com/docs/en/cobol-zos/4.2?topic=clause-computational-items).

#### Supported data types

The supported data types are created as follows:

| Parameter | Meaning              |Legacy Notation |
|-----------|----------------------|----------------|
| ch        | text                 | PIC  x         |
| zd        | zoned                | PIC  9         |
| zd+       | signed zoned         | PIC S9         |
| bi        | binary               | PIC  9 COMP    |
| bi+       | signed binary        | PIC S9 COMP    |
| pd        | packed-decimal       | PIC  9 COMP-3  |
| pd+       | signed packed-decimal| PIC S9 COMP-3  |

### extract-ebcdic-to-ascii

Once the Cobol copybook is parsed to JSON it can be used as the input of this module.

Both **input** (EBCDIC) and **output** (ASCII) files are identified by the JSON file.

```
   "input":  "extract-ebcdic-to-ascii/COBPACK.OUTFILE.txt",
   "output": "extract-ebcdic-to-ascii/COBPACK.ASCII.txt",
```

## LegacyReference

The source code under the *LegacyReference* folder are JCL and Cobol components created exclusively to generate EBCDIC data mass for testing purposes.

The [layout](LegacyReference/COBPACK2.cpy) of the [source file](sample-data/COBPACK.OUTFILE.txt) used for testing (in Cobol notation) is:

```
01 REC-OUTFILE.
   03 OUTFILE-TEXT                PIC -9(18).
   03 OUTFILE-UNPACKED            PIC  9(18).
   03 OUTFILE-UNPACKED-S          PIC S9(18).
   03 BINARY-FIELDS.
      05 OUTFILE-COMP-04          PIC  9(04) COMP.
      05 OUTFILE-COMP-04-S        PIC S9(04) COMP.
      05 OUTFILE-COMP-09          PIC  9(09) COMP.
      05 OUTFILE-COMP-09-S        PIC S9(09) COMP.
      05 OUTFILE-COMP-18          PIC  9(18) COMP.
      05 OUTFILE-COMP-18-S        PIC S9(18) COMP.
   03 PACKED-DECIMAL-FIELDS.
      05 OUTFILE-COMP3-04         PIC  9(04) COMP-3.
      05 OUTFILE-COMP3-04-S       PIC S9(04) COMP-3.
      05 OUTFILE-COMP3-09         PIC  9(09) COMP-3.
      05 OUTFILE-COMP3-09-S       PIC S9(09) COMP-3.
      05 OUTFILE-COMP3-18         PIC  9(18) COMP-3.
      05 OUTFILE-COMP3-18-S       PIC S9(18) COMP-3.
   03 GROUP1.
      05 GROUP1-1 OCCURS 2 TIMES.
         07 TEXT1                 PIC  X(01).
   03 GROUP2 REDEFINES GROUP1.
      05 TEXT2                    PIC  X(02).
   03 FILLER                      PIC  X(29).
```

## Do you want to help?

### General
- Test automation.
- Code organization / refactoring.

### Copybook parser
- OCCURS DEPENDING ON copybook parsing.
- Data item REDEFINES.
- Aurora schema parser (DDL)
- Add similar packing statements (BINARY, PACKED-DECIMAL...)
- Handle packing statement (COMP, COMP-3, etc.) when declared before PIC statement

### Data conversion
- VB file conversion
- Aurora data load