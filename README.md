# Mainframe Data Utilities

Table of contents
=================
* Security
* License
* About
* Status
* Requirements
* extract-ebcdic-to-ascii
    * Parameters
    * Execution
* LegacyReference
* Roadmap

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

## About

Mainframe Data Utilities is an AWS Sample

The purpose of this project is to create a series of Python scripts to handle EBCDIC files migrated from mainframes or AS/400 platforms to AWS or any distributed environment.

The first release of this toolset consists of two scripts:

- extract-ebcdic-to-ascii.py is the first script/tool of this project. It uses a json parameter file to slice a fixed length EBCDIC file and unpack its contents and write them to an ASCII file.

- ebcdic is the main library that handles the encoding transformation logic.

- parse-copybook-to-json is a module to automate the creation of the parameters file required by the extract-ebcdic-to-ascii script.

## Status

In progress

### Requirements

Make sure [Python](https://www.python.org/downloads/) 3 or above is installed.

## extract-ebcdic-to-ascii

### Parameters

Using `extract-ebcdic-to-ascii/ParamFile.json` as an example, create the json parameter file based on your legacy file layout. The types must correspond to the list below:

| Parameter | Meaning              |Legacy Notation |
|-----------|----------------------|----------------|
| ch        | text                 | pic  x         |
| zd        | zoned                | pic  9         |
| zd+       | signed zoned         | pic s9|        |
| bi        | binary               | pic  9 comp    |
| bi+       | signed binary        | pic s9 comp    |
| pd        | packed-decimal       | pic  9 comp-3  |
| pd+       | signed packed-decimal| pic s9 comp-3  |
| skip      | skip / bypass column | N/A            |

The length must be in bytes. A 18 digit integer field, for instance, only takes 10 bytes. For more information check [IBM Computational items documentation](https://www.ibm.com/docs/en/cobol-zos/4.2?topic=clause-computational-items).

### Execution

Execute `extract-ebcdic-to-ascii.py` passing the json parameter file created in the previous step as an argument. The command below will process the [extract-ebcdic-to-ascii/SourceFile.txt](extract-ebcdic-to-ascii/SourceFile.txt) file provided as an example.

```
python3 extract-ebcdic-to-ascii.py extract-ebcdic-to-ascii/ParamFile.json 
```

## parse-copybook-to-json
### Execution

```
python parse-copybook-to-json.py parse-copybook-to-json/stock.cpy parse-copybook-to-json/stock.json

python parse-copybook-to-json.py parse-copybook-to-json/cobpack.cpy parse-copybook-to-json/cobpack.json
```

## LegacyReference 

The source code under the *LegacyReference* folder are JCL and Cobol components created exclusively to generate EBCDIC data mass for testing purposes.

The layout of the [source file](extract-ebcdic-to-ascii/SourceFile.txt) used for testing (in Cobol notation) is:

```
01. OUTFILE.
03  OUTFILE-TEXT              PIC -9(18). 
03  OUTFILE-UNPACKED          PIC  9(18). 
03  OUTFILE-UNPACKED-SIGNED   PIC S9(18). 
03  OUTFILE-COMP              PIC  9(18) COMP. 
03  OUTFILE-COMP-SIGNED       PIC S9(18) COMP. 
03  OUTFILE-COMP3             PIC  9(18) COMP-3. 
03  OUTFILE-COMP3-SIGNED      PIC S9(18) COMP-3. 
```