      *-----------------------------------------------------------------
      * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
      * SPDX-License-Identifier: Apache-2.0
      *-----------------------------------------------------------------
       01  REC-CLIENT.                                                  00039300
           03  CLIENT-KEY.                                              00039400
            05 CLIENT-ID                 PIC  9(009) COMP.              00039500
            05 CLIENT-TYPE               PIC  9(004) COMP.              00039500
           03  CLIENT-MAIN.                                             00039400
            05 CLIENT-NAME               PIC  X(030).                   00039500
            05 CLIENT-BDATE              PIC  X(010).                   00039500
            05 CLIENT-ED-LVL             PIC  X(010).                   00039500
            05 CLIENT-INCOME             PIC  9(007)V99 COMP-3.         00039500
            05 FILLER                    PIC  X(439).                   00039500
           03  CLIENT-ADDRESS REDEFINES  CLIENT-MAIN.                           
            05 CLIENT-ADDR-NUMBER        PIC  9(009) COMP.              00039500
            05 CLIENT-ADDR-STREET        PIC  X(040).                   00039500
            05 FILLER                    PIC  X(450).                   00039500
           03  CLIENT-HEADER  REDEFINES  CLIENT-MAIN.                           
            05 CLIENT-RECORD-COUNT       PIC  9(009) COMP.              00039500
            05 FILLER                    PIC  X(490).                   00039500