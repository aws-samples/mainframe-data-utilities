      *-----------------------------------------------------------------
      * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
      * SPDX-License-Identifier: Apache-2.0
      *-----------------------------------------------------------------
       IDENTIFICATION DIVISION.                                         00010000
       PROGRAM-ID. COBPACK2.                                            00020000
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.                                            00030000
      *-----------------------------------------------------------------00030200
       FILE-CONTROL.                                                    00030300
                                                                        00030400
           SELECT OUTFILE ASSIGN TO OUTFILE                             00030500
                  FILE STATUS IS WS-FS-OUTFILE.                         00030700
      *-----------------------------------------------------------------00030800
       DATA DIVISION.                                                   00030900
       FILE SECTION.                                                    00034000
                                                                        00036000
       FD  OUTFILE                                                      00037000
           BLOCK CONTAINS 0 RECORDS                                     00038000
           RECORDING MODE IS F                                          00039000
           RECORD CONTAINS 150 CHARACTERS.                              00039100
                                                                        00039200
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

       WORKING-STORAGE SECTION.
      *-----------------------------------------------------------------
       01  WS-AUX.
           05  WS-FS-OUTFILE             PIC X(002)  VALUE SPACES.
           05  WS-IX                     PIC S9(18).                    00039400

       PROCEDURE DIVISION.                                              00040000

           DISPLAY 'COBPACK START...'.                                  00050000
           OPEN OUTPUT OUTFILE.
           IF WS-FS-OUTFILE NOT EQUAL '00'
              DISPLAY 'OPEN OUTFILE FS:  ' WS-FS-OUTFILE
              STOP RUN
           END-IF

           MOVE -100000000 TO WS-IX

           PERFORM UNTIL WS-IX          GREATER 100000000

              MOVE WS-IX
              TO   OUTFILE-TEXT                                               00
                   OUTFILE-UNPACKED                                           00
                   OUTFILE-UNPACKED-S                                   00039400
                   OUTFILE-COMP-04                                      00039500
                   OUTFILE-COMP-04-S                                    00039500
                   OUTFILE-COMP-09                                      00039500
                   OUTFILE-COMP-09-S                                    00039500
                   OUTFILE-COMP-18                                      00039500
                   OUTFILE-COMP-18-S                                    00039500
                   OUTFILE-COMP3-04                                     00039500
                   OUTFILE-COMP3-04-S                                   00039500
                   OUTFILE-COMP3-09                                     00039500
                   OUTFILE-COMP3-09-S                                   00039500
                   OUTFILE-COMP3-18                                     00039500
                   OUTFILE-COMP3-18-S                                   00039500

              MOVE 'A'
              TO    TEXT1 OF GROUP1-1 (1)
                    TEXT1 OF GROUP1-1 (2)

              WRITE REC-OUTFILE         END-WRITE

              IF WS-FS-OUTFILE NOT EQUAL '00'
                 DISPLAY 'WRITE OUTFILE FS:  ' WS-FS-OUTFILE
                 STOP RUN
              END-IF

              ADD 2001 TO WS-IX

           END-PERFORM.

           CLOSE OUTFILE.
           IF WS-FS-OUTFILE NOT EQUAL '00'
              DISPLAY 'CLOSE OUTFILE FS: ' WS-FS-OUTFILE
              STOP RUN
           END-IF

           DISPLAY 'COBPACK FINISH..'.                                  00050000

           STOP RUN.                                                    00060000
