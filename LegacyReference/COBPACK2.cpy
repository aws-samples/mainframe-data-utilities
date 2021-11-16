      *-----------------------------------------------------------------
      * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
      * SPDX-License-Identifier: Apache-2.0
      *-----------------------------------------------------------------
       01  REC-OUTFILE.                                                 00039300
           03  OUTFILE-TEXT              PIC -9(18).                    00039400
           03  OUTFILE-UNPACKED          PIC  9(18).                    00039400
           03  OUTFILE-UNPACKED-S        PIC S9(18).                    00039400
           03  BINARY-FIELDS.                                           00039400
            05 OUTFILE-COMP-04           PIC  9(04) COMP.               00039500
            05 OUTFILE-COMP-04-S         PIC S9(04) COMP.               00039500
            05 OUTFILE-COMP-09           PIC  9(09) COMP.               00039500
            05 OUTFILE-COMP-09-S         PIC S9(09) COMP.               00039500
            05 OUTFILE-COMP-18           PIC  9(18) COMP.               00039500
            05 OUTFILE-COMP-18-S         PIC S9(18) COMP.               00039500
           03  PACKED-DECIMAL-FIELDS.                                   00039400
            05 OUTFILE-COMP3-04          PIC  9(04) COMP-3.             00039500
            05 OUTFILE-COMP3-04-S        PIC S9(04) COMP-3.             00039500
            05 OUTFILE-COMP3-09          PIC  9(09) COMP-3.             00039500
            05 OUTFILE-COMP3-09-S        PIC S9(09) COMP-3.             00039500
            05 OUTFILE-COMP3-18          PIC  9(18) COMP-3.             00039500
            05 OUTFILE-COMP3-18-S        PIC S9(18) COMP-3.             00039500
           03  GROUP1.
            05 GROUP1-1 OCCURS 2 TIMES.                                 00039500
             07 TEXT1                   PIC  X(01).                     00039500
           03  GROUP2 REDEFINES GROUP1.
            05 TEXT2                     PIC  X(02).                    00039500
           03 FILLER                     PIC  X(29).                    