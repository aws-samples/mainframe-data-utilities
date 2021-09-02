# Mainframe Data Utilities

Table of contents
=================
* Security
* License
* About
* Status
* Requirements
* Limitations
* Getting started
* How it works
* LegacyReference
* To be implemented

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

## About

Mainframe Data Utilities is an AWS Sample written in Python.

The purpose of this project is to provide Python scripts as a starting point for those who need to handle EBCDIC files transferred from mainframes and AS/400 platforms to AWS or any distributed environment.

The current release of this toolset consists of three scripts:

- **parse-copybook-to-json** is a module that creates a JSON parameter file by parsing Cobol Copybook. The parameter file is a description of the file EBCDIC file layout, required by extract-ebcdic-to-ascii.py 

- **extract-ebcdic-to-ascii.py** uses the JSON parameter file to slice a fixed length EBCDIC file, unpack its contents and write them to an ASCII file.

- **ebcdic** is the main library that handles the encoding transformation logic.

## Status

Stable

## Requirements

Make sure [Python](https://www.python.org/downloads/) 3 or above is installed.

## Limitations

1. Occurs for non-group data elements are not detected by the copybook parser yet.
2. Multi-layout files are not supported. Redefines statements are ignored.
3. File layouts defined inside Cobol programas are not supported.
4. The file's logical record length is the sum of all field sizes. This means that in some cases the calculation may result in a size that is smaller than the physical file definition.

## Getting started

1. Clone this repo:

```
git clone git@github.com:aws-samples/mainframe-data-utilities.git.
```

2. Run the `parse-copybook-to-json.py` script to parse the copybook file provided in `sample-data`.

```
python parse-copybook-to-json.py -copybook LegacyReference/COBPACK2.cpy -output sample-data/cobpack2-list.json -dict sample-data/cobpack2-dict.json -ebcdic sample-data/COBPACK.OUTFILE.txt -ascii sample-data/COBPACK.ASCII.txt -print 10000
```

3. Run `extract-ebcdic-to-ascii.py`to extract the `COBPACK.OUTFILE.txt` into an ASCII file.

```
python extract-ebcdic-to-ascii.py sample-data/cobpack2-list.json
```

## How it works

### parse-copybook-to-json

Mainframe files are typicaly packed (into decimal and binary formats), and encoded in EBCDIC. 

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

|Parameter      |Description                                    |
|---------------|-----------------------------------------------|
|input          |Name of the input EBCDIC file to be extracted  |
|output         |Name of the outout ASCII file to be generated  |
|max            |Max number of records to be extracted          |
|skip           |Number of records to be skiped                 |
|print          |Amount of records before print status          |
|lrecl          |Logical record lenght of the ebcdic file       |
|rem-low-values |Remove null chars                              |
|separator      |Char to add between fields to separate them    |
|transf.type    |type of the field to be transformed            |
|transf.bytes   |Sice in bytes of the field to be transformed   |
|transf.name    |Name of the field to be transformed            |

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
    "transf": [
        {
            "type": "ch",
            "bytes": 19,
            "name": "OUTFILE-TEXT"
        }
```

The length is represented in bytes. A 18 digit integer field, for instance, only takes 10 bytes. For more information check [IBM Computational items documentation](https://www.ibm.com/docs/en/cobol-zos/4.2?topic=clause-computational-items).

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
   "input": "extract-ebcdic-to-ascii/COBPACK.OUTFILE.txt",
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

## To be implemented
- Occurs for non-group data elements.
- Creation of the DDL from JSON parsed copybook.
- Multi-layout files / redefines handling.
- Easytrive layout parsing.

