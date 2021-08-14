# Mainframe Data Utilities

Table of contents
=================
* Security
* License
* About
* Status
* How to use
    * Parameters
    * Local files execution
* LegacyReference

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

## About

The purpose of this project is to create a series of scripts to handle EBCDIC files migrated from mainframes or AS/400 platforms.

extract-ebcdic-to-ascii.py is the first script of this project. The idea is to

## Status

In progress

## How to use extract-ebcdic-to-ascii

1. Ensure that Python 3 or above is installed.

2. Using the ParamFile.json as an example, create the json parameter file based on your legacy file layout.

    ### The types must correspond to the list below:
    - ch : text                 | pic  x
    - zd : zoned                | pic  9
    - zd+: signed zoned         | pic s9
    - bi : binary               | pic  9 comp
    - bi+: signed binary        | pic s9 comp
    - pd : packed-decimal       | pic  9 comp-3
    - pd+: signed packed-decimal| pic s9 comp-3

    ### Length value must be in bytes. A 18 digit integer only takes 10 bytes.

    ### Layout of the input file used for testing (in Cobol notation).

    ```
        01. OUTFILE.
        03  OUTFILE-TEXT              PIC -9(18). 
        03  OUTFILE-UNPACKED          PIC  9(18). 
        03  OUTFILE-UNPACKED-SIGNED   PIC S9(18). 
        03  OUTFILE-COMP-SIGNED       PIC  9(18) COMP. 
        03  OUTFILE-COMP              PIC S9(18) COMP. 
        03  OUTFILE-COMP3             PIC  9(18) COMP-3. 
        03  OUTFILE-COMP3-SIGNED      PIC S9(18) COMP-3. 
    ```

    3. Execute through the command below:

    ```
    python3 e2a.py ParamFile.json 
        ```

## LegacyReference 

The code under the *LegacyReference* folder are JCL and Cobol components created exclusively to generate EBCDIC data mass for testing purposes.