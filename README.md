# Mainframe Data Utilities

| :exclamation:  Mainframe Data Utilities v1 documentation available at [v1](docs/99-README-v1.md) :exclamation: |
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
* Docs
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
2. Packing statement is ignored when defined before the PIC clause.
3. The file's logical record length is the sum of all field sizes. This means that in some cases the calculation may result in a size that is smaller than the physical file definition.
4. The `REDEFINES` statement for **data items**, it's only supported for **group items**.

## Docs

There are some examples about how to extract data on different use cases:

|Document  |Description|
|---------------------------------|-|
|[Download](docs/00-download.md)| How to download the codebase |
|[Single Layout Fixed Blocked file](docs/01-local-single-fb.md)|Simplest conversion. Local, fixed blocked and single layout file|
|[Read the metadata JSON from Amazon S3](docs/02-local-single-fb-s3-json.md)|Single Layout Fixed Blocked file|
|[2](docs/03-local-single-fb-thread.md)||
|[3](docs/04-local-single-vb.md)||
|[4](docs/05-local-multi-fb.md)||
|[5](docs/06-local-multi-fb-s3-input.md)||
|[6](docs/07-local-multi-fb-s3-output.md)||
|[7](docs/08-local-multi-ddb.md)||
|[8](docs/09-lambda-multi-s3-output.md)||
|[9](docs/10-s3-lambda-obj-multi-fb.md)||
|[10]()||
|[11]()||
|[12]()||


1. [Single layout FB file](/docs/02-local-single-fb.md).
1. [Single layout VB file](/docs/03-local-single-vb.md).
1. [Multiple layout FB file](/docs/04-local-multi-fb.md).
1. [Multiple layout FB file from an S3 bucket]().


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