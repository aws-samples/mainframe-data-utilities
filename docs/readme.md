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

1. [Download the source](/docs/sourcecode.md).
1. [Convert a single layout file](/docs/localsinglelayout.md).

## Backlog

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
- Aurora data load