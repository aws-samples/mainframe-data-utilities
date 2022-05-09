      *-----------------------------------------------------------------
      * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
      * SPDX-License-Identifier: Apache-2.0
      *-----------------------------------------------------------------
       01  REC-OUTFILE.                                                 00039300
                                                                        BLANKLNE
           03  OUTFILE-TEXT              PIC -9(18).                    00039400
           03  OUTFILE-UNPACKED          PIC  9(18).                    00039400
           03  OUTFILE-UNPACKED-S        PIC S9(18).                    00039400
           03  BINARY-FIELDS.                                           00039400
            05 OUTFILE-COMP-01           PIC  9(01) COMP.               00039500
            05 OUTFILE-COMP-01-S         PIC S9(01) COMP.               00039500
            05 OUTFILE-COMP-02           PIC  9(02) COMP.               00039500
            05 OUTFILE-COMP-02-S         PIC S9(02) COMP.               00039500
            05 OUTFILE-COMP-03           PIC  9(03) COMP.               00039500
            05 OUTFILE-COMP-03-S         PIC S9(03) COMP.               00039500
            05 OUTFILE-COMP-04           PIC  9(04) COMP.               00039500
            05 OUTFILE-COMP-04-S         PIC S9(04) COMP.               00039500
            05 OUTFILE-COMP-05           PIC  9(05) COMP.               00039500
            05 OUTFILE-COMP-05-S         PIC S9(05) COMP.               00039500
            05 OUTFILE-COMP-06           PIC  9(06) COMP.               00039500
            05 OUTFILE-COMP-06-S         PIC S9(06) COMP.               00039500
            05 OUTFILE-COMP-07           PIC  9(07) COMP.               00039500
            05 OUTFILE-COMP-07-S         PIC S9(07) COMP.               00039500
            05 OUTFILE-COMP-08           PIC  9(08) COMP.               00039500
            05 OUTFILE-COMP-08-S         PIC S9(08) COMP.               00039500
            05 OUTFILE-COMP-09           PIC  9(09) COMP.               00039500
            05 OUTFILE-COMP-09-S         PIC S9(09) COMP.               00039500
            05 OUTFILE-COMP-18           PIC  9(18) COMP.               00039500
            05 OUTFILE-COMP-18-S         PIC S9(18) COMP.               00039500
       SKIP1
           03  PACKED-DECIMAL-FIELDS.                                   00039400
            05 OUTFILE-COMP3-01          PIC  9(01) COMP-3.             00039500
            05 OUTFILE-COMP3-01-S        PIC S9(01) COMP-3.             00039500
            05 OUTFILE-COMP3-02          PIC  9(02) COMP-3.             00039500
            05 OUTFILE-COMP3-02-S        PIC S9(02) COMP-3.             00039500
            05 OUTFILE-COMP3-03          PIC  9(03) COMP-3.             00039500
            05 OUTFILE-COMP3-03-S        PIC S9(03) COMP-3.             00039500
            05 OUTFILE-COMP3-04          PIC  9(04) COMP-3.             00039500
            05 OUTFILE-COMP3-04-S        PIC S9(04) COMP-3.             00039500
            05 OUTFILE-COMP3-05          PIC  9(05) COMP-3.             00039500
            05 OUTFILE-COMP3-05-S        PIC S9(05) COMP-3.             00039500
            05 OUTFILE-COMP3-06          PIC  9(06) COMP-3.             00039500
            05 OUTFILE-COMP3-06-S        PIC S9(06) COMP-3.             00039500
            05 OUTFILE-COMP3-07          PIC  9(07) COMP-3.             00039500
            05 OUTFILE-COMP3-07-S        PIC S9(07) COMP-3.             00039500
            05 OUTFILE-COMP3-08          PIC  9(08) COMP-3.             00039500
            05 OUTFILE-COMP3-08-S        PIC S9(08) COMP-3.             00039500
            05 OUTFILE-COMP3-09          PIC  9(09) COMP-3.             00039500
            05 OUTFILE-COMP3-09-S        PIC S9(09) COMP-3.             00039500
            05 OUTFILE-COMP3-18          PIC  9(18) COMP-3.             00039500
            05 OUTFILE-COMP3-18-S        PIC S9(18) COMP-3.             00039500
           03  GROUP1.
            05 GROUP1-1 OCCURS 2 TIMES.                                 00039500
             07 TEXT1                    PIC  X(01).                    00039500
           03  GROUP2 REDEFINES GROUP1.
            05 TEXT2                     PIC  X(02).                    00039500
           03 FILLER                     PIC  X(03).                    00039500