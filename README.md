# Mainframe Data Utilities v2

| :exclamation:  Looking for [Mainframe Data Utilities v1](docs/99-README-v1.md)? :exclamation: |
|-----------------------------------------|
# Mainframe Data Utilities

Table of contents
=================
* Security
* License
* About
* Status
* Requirements
* Limitations
* Download
* Examples
* Backlog

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

## About

Mainframe Data Utilities is an AWS Sample written in Python.

The purpose of this project is to provide Python scripts as a starting point for those who need to read EBCDIC files transferred from mainframes and AS/400 platforms on AWS or any distributed environment.

## Requirements

- [Python](https://www.python.org/downloads/) 3.8 or above
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Limitations

1. File layouts defined inside Cobol programs are not supported.
2. The file's logical record length is the sum of all field sizes. This means that in some cases the calculation may result in a size that is smaller than the physical file definition.
4. The `REDEFINES` statement for **data items**, it's only supported for **group items**.

## Download

Download the code to run a preloaded example.

From Windows, Mac or Linux shell (including AWS CloudShell), clone this repo and change directory:

```
git clone https://github.com/aws-samples/mainframe-data-utilities.git mdu
cd mdu
```

## Examples

There are some examples about how to extract data on different use cases:

|Document  |Description|
| - | - |
|[Single Layout FB file](docs/01-local-single-fb.md)                    |The simplest conversion. Local, 'fixed blocked' and 'single layout' input file.|
|[Read JSON metadata from Amazon S3](docs/02-local-single-fb-s3-json.md)|The JSON metadata file read from S3.|
|[Single Layout FB file](docs/03-local-single-fb-thread.md)             |Convert a file using multithreading and generating multiple output files.|
|[Single Layout VB file](docs/04-local-single-vb.md)                    |Convert a Variable Block input file.|
|[Multiple Layout file](docs/05-local-multi-fb.md)                      |Convert a multiple layout input file.|
|[Read the input file from S3](docs/06-local-multi-fb-s3-input.md)      |Get the input file from S3 and generate a local converted file.|
|[Write the output file on S3](docs/07-local-multi-fb-s3-output.md)     |Read a local file and write a converted file on S3.|
|[Write the output data on DynamoDB](docs/08-local-multi-ddb.md)        |Read a local file and write its data on DynamoDB.|
|[Convert files using a Lambda function](docs/09-lambda-multi-s3-output.md)|Use a Lambda function to read an EBCDIC file from S3 and write the converted file back to S3.|
|[Convert files using S3 Object Lambda](docs/10-s3-lambda-obj-multi-fb.md) |Use an Object Lambda to convert a EBCDIC file while it's downloaded from S3.|
|[Split files by content/key](docs/99-file-split-fb.md)                 |Split an EBCDIC file according with a key provided |
|[Discard specific layout](docs/11-local-multi-fb-discard.md)           |Convert a multiple layout input file while discarding selected record types|

## Backlog

### General
- There are still some try / exceptions to be coded.
- Test automation.
- Code organization / refactoring.

### Copybook parser
- OCCURS DEPENDING ON copybook parsing.
- Data item REDEFINES.
- Aurora schema parser (DDL)
- Add similar packing statements (BINARY, PACKED-DECIMAL...)
- Handle packing statement (COMP, COMP-3, etc.) when declared before PIC statement

### Data conversion
- Aurora data load
