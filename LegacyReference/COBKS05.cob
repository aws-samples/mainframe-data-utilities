      *-----------------------------------------------------------------        
      * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.      
      * SPDX-License-Identifier: Apache-2.0                                     
      *-----------------------------------------------------------------        
       IDENTIFICATION DIVISION.                                         00010000
       PROGRAM-ID. COBKS05.                                              0002000
       ENVIRONMENT DIVISION.                                                    
       INPUT-OUTPUT SECTION.                                            00030000
      *-----------------------------------------------------------------00030200
       FILE-CONTROL.                                                    00030300
      *-----------------------------------------------------------------00030200
           SELECT INPUTF  ASSIGN TO INPUTF                              00030500
                  FILE STATUS IS WS-FS-INPUT.                           00030700
      *-----------------------------------------------------------------00030800
                                                                        00030400
           SELECT CLIENT ASSIGN TO CLIENT                               00030500
                  ORGANIZATION  IS INDEXED                                      
                  ACCESS MODE   IS RANDOM                                       
                  RECORD KEY    IS CLIENT-KEY                                   
                  FILE STATUS   IS WS-FS-CLIENT.                        00030700
      *-----------------------------------------------------------------00030800
       DATA DIVISION.                                                   00030900
       FILE SECTION.                                                    00034000
                                                                        00036000
       FD  INPUTF                                                       00037000
           BLOCK CONTAINS 0 RECORDS                                     00038000
           RECORDING MODE IS F                                          00039000
           RECORD CONTAINS 080 CHARACTERS.                              00039100
                                                                        00039200
       01  REC-INPUT.                                                   00039300
           03  INPUTF-ID                 PIC  9(09).                    00039400
           03  INPUTF-TYPE               PIC  9(04).                    00039400
           03  INPUTF-MAIN.                                                     
            05 INPUTF-NAME               PIC  X(30).                    00039400
            05 INPUTF-BDATE              PIC  X(10).                    00039400
            05 INPUTF-ED-LVL             PIC  X(10).                    00039400
            05 INPUTF-INCOME             PIC  9(07)V99.                 00039400
           03  INPUTF-ADDRESS REDEFINES  INPUTF-MAIN.                           
            05 INPUTF-ADDR-NUMBER        PIC  9(009).                   00039500
            05 INPUTF-ADDR-STREET        PIC  X(040).                   00039500
            05 FILLER                    PIC  X(010).                   00039500
           03  FILLER                    PIC  X(08).                    00039400
      *-----------------------------------------------------------------00030800
       FD  CLIENT.                                                      00037000
                                                                        00039200
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
                                                                                
       WORKING-STORAGE SECTION.                                                 
      *-----------------------------------------------------------------        
       01  WS-AUX.                                                              
           05  WS-FS-CLIENT              PIC X(002) VALUE SPACES.               
           05  WS-FS-INPUT               PIC X(002) VALUE SPACES.               
           05  WS-READ                   PIC 9(009) VALUE ZEROS.        00039400
           05  WS-INSERTED               PIC 9(009) VALUE ZEROS.        00039400
           05  WS-UPDATED                PIC 9(009) VALUE ZEROS.        00039400
           05  WS-SPACES                 PIC X(500) VALUE SPACES.       00039400
                                                                                
       PROCEDURE DIVISION.                                              00040000
                                                                                
           DISPLAY 'COBKS02 STARTED'.                                   00050000
                                                                                
           OPEN INPUT INPUTF.                                                   
                                                                                
           IF WS-FS-INPUT  NOT EQUAL '00'                                       
                                                                                
              DISPLAY 'OPEN INPUT  FS:  ' WS-FS-INPUT                           
              PERFORM P999-ERROR THRU P999-ERROR-EXIT                           
                                                                                
           END-IF                                                               
                                                                                
           OPEN I-O   CLIENT.                                                   
                                                                                
           EVALUATE TRUE                                                        
           WHEN WS-FS-CLIENT EQUAL '00'                                         
              CONTINUE                                                          
           WHEN WS-FS-CLIENT EQUAL '35'                                         
              DISPLAY 'EMPTY VSAM. PLEASE RUN AGAIN.'                           
                                                                                
              OPEN OUTPUT CLIENT                                                
                                                                                
              MOVE ZEROS                                                        
              TO   CLIENT-ID                                                    
                   CLIENT-TYPE                                                  
                   CLIENT-RECORD-COUNT                                          
                                                                                
              WRITE REC-CLIENT                                                  
              STOP RUN                                                          
                                                                                
           WHEN OTHER                                                           
              DISPLAY 'OPEN CLIENT FS:  ' WS-FS-CLIENT                          
              PERFORM P999-ERROR THRU P999-ERROR-EXIT                           
           END-EVALUATE                                                         
                                                                                
           READ INPUTF                                                          
           END-READ                                                             
                                                                                
           PERFORM UNTIL WS-FS-INPUT    GREATER '00'                            
                                                                                
              ADD  1 TO WS-READ                                                 
                                                                                
              MOVE INPUTF-ID                                                    
              TO   CLIENT-ID                                                  00
                                                                                
              MOVE INPUTF-TYPE                                                  
              TO   CLIENT-TYPE                                          00039500
                                                                                
              READ CLIENT                                                       
                INVALID KEY                                                     
                                                                                
                   PERFORM P200-MOVE-DATA THRU P200-MOVE-DATA-EXIT              
                                                                                
                   WRITE   REC-CLIENT                                           
                                                                                
                   PERFORM P998-EVAL-CLIENT                                     
                   THRU    P998-EVAL-CLIENT-EXIT                                
                                                                                
                   ADD 1 TO WS-INSERTED                                         
                                                                                
                NOT INVALID KEY                                                 
                                                                                
                   PERFORM P200-MOVE-DATA THRU P200-MOVE-DATA-EXIT              
                                                                                
                   REWRITE REC-CLIENT                                           
                                                                                
                   PERFORM P998-EVAL-CLIENT                                     
                   THRU    P998-EVAL-CLIENT-EXIT                                
                                                                                
                   ADD 1 TO WS-UPDATED                                          
                                                                                
              END-READ                                                          
                                                                                
              READ INPUTF                                                       
              END-READ                                                          
                                                                                
           END-PERFORM.                                                         
                                                                                
           MOVE    ZEROS                                                        
           TO      CLIENT-ID                                                  00
                   CLIENT-TYPE                                          00039500
                                                                                
           READ    CLIENT                                                       
                                                                                
           ADD     WS-INSERTED TO CLIENT-RECORD-COUNT                           
                                                                                
           REWRITE REC-CLIENT                                                   
                                                                                
           PERFORM P998-EVAL-CLIENT                                             
           THRU    P998-EVAL-CLIENT-EXIT                                        
                                                                                
           CLOSE CLIENT.                                                        
           IF WS-FS-CLIENT NOT EQUAL '00'                                       
              DISPLAY 'CLOSE CLIENT FS: ' WS-FS-CLIENT                          
              PERFORM P999-ERROR THRU P999-ERROR-EXIT                           
           END-IF                                                               
                                                                                
           DISPLAY '--------------------'.                              00050000
           DISPLAY 'READ....: ' WS-READ.                                00050000
           DISPLAY 'INSERDED: ' WS-INSERTED.                            00050000
           DISPLAY 'UPDATED.: ' WS-UPDATED.                             00050000
           DISPLAY '--------------------'.                              00050000
           STOP RUN.                                                    00060000
                                                                                
       P200-MOVE-DATA.                                                  00040000
                                                                                
           MOVE WS-SPACES TO CLIENT-MAIN                                        
                                                                                
           EVALUATE TRUE                                                        
           WHEN CLIENT-TYPE EQUAL 1                                             
              MOVE  INPUTF-NAME                                                 
              TO    CLIENT-NAME                                                 
                                                                                
              MOVE  INPUTF-BDATE                                                
              TO    CLIENT-BDATE                                                
                                                                                
              MOVE  INPUTF-ED-LVL                                               
              TO    CLIENT-ED-LVL                                               
                                                                                
              MOVE  INPUTF-INCOME                                               
              TO    CLIENT-INCOME                                               
                                                                                
           WHEN CLIENT-TYPE EQUAL 2                                             
              MOVE  INPUTF-ADDR-NUMBER                                  00039500
              TO    CLIENT-ADDR-NUMBER                                  00039500
              MOVE  INPUTF-ADDR-STREET                                  00039500
              TO    CLIENT-ADDR-STREET                                  00039500
           WHEN OTHER                                                           
              DISPLAY 'UNSUPPORTED REC TYPE: ' CLIENT-TYPE                      
              PERFORM P999-ERROR THRU P999-ERROR-EXIT                           
                                                                                
           END-EVALUATE                                                         
           .                                                                    
                                                                                
       P200-MOVE-DATA-EXIT.                                             00040000
           EXIT.                                                                
                                                                                
       P998-EVAL-CLIENT.                                                00040000
                                                                                
           IF WS-FS-CLIENT NOT EQUAL '00'                                       
              DISPLAY 'WRITE CLIENT FS:  ' WS-FS-CLIENT                         
              PERFORM P999-ERROR THRU P999-ERROR-EXIT                           
           END-IF                                                               
           .                                                                    
       P998-EVAL-CLIENT-EXIT.                                           00040000
           EXIT.                                                                
       P999-ERROR.                                                      00040000
                                                                                
           MOVE 8 TO RETURN-CODE                                                
                                                                                
           STOP RUN.                                                            
                                                                                
       P999-ERROR-EXIT.                                                 00040000
           EXIT.                                                                
