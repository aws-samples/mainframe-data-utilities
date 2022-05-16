      *-----------------------------------------------------------------        
      * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.      
      * SPDX-License-Identifier: Apache-2.0                                     
      *-----------------------------------------------------------------        
       IDENTIFICATION DIVISION.                                         00010000
       PROGRAM-ID. COBVBFM2.                                             0002000
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
           RECORDING MODE IS V.                                                 
                                                                                
       01  OUT-RECORD.                                                          
           03  OUT-KEY.                                                         
               05  OUTK-TYPE       PIC XX.                                      
               05  OUTK-SEQT       PIC 99.                                      
           03  OUT-REC-CNT         PIC S999    COMP-3.                          
           03  OUT-REC             OCCURS 1 TO 10 TIMES                         
                                   DEPENDING ON OUT-REC-CNT.                    
               05  OUT-REC-NO      PIC 9(09).                                   
               05  OUT-NAME        PIC X(21).                                   
                                                                                
       WORKING-STORAGE SECTION.                                                 
      *-----------------------------------------------------------------        
       01  WS-AUX.                                                              
           05  WS-FS-OUTFILE             PIC  X(02)  VALUE SPACES.              
           05  WS-SEQT                   PIC  9(02)  VALUE ZEROS.               
           05  WS-IX                     PIC  9(05)  VALUE ZEROS.               
           05  WS-REC-CNT                PIC S999    COMP-3 VALUE ZEROS.        
           05  WS-NAME.                                                         
               10 WS-TEXT                PIC  X(10).                            
               10 WS-NO                  PIC  9(09).                            
               10 FILLER                 PIC  X(11).                            
                                                                                
       PROCEDURE DIVISION.                                                      
                                                                                
           OPEN OUTPUT OUTFILE.                                                 
                                                                                
           IF WS-FS-OUTFILE NOT EQUAL '00'                                      
              DISPLAY 'OPEN OUTFILE FS:  ' WS-FS-OUTFILE                        
              MOVE 1 TO RETURN-CODE                                             
              STOP RUN                                                          
           END-IF                                                               
                                                                                
           PERFORM UNTIL WS-SEQT EQUAL 20                                       
                                                                                
               ADD  1            TO WS-SEQT                                     
                                    WS-REC-CNT                                  
               MOVE '00'         TO OUTK-TYPE                                   
               MOVE WS-SEQT      TO OUTK-SEQT                                   
               MOVE WS-REC-CNT   TO OUT-REC-CNT                                 
                                                                                
               MOVE 0       TO WS-IX                                            
                                                                                
               PERFORM P201-FORMAT-OUTPUT THRU  P201-FORMAT-OUTPUT-EXIT         
               UNTIL   WS-IX              EQUAL OUT-REC-CNT                     
                                                                                
               WRITE OUT-RECORD          END-WRITE                              
                                                                                
               IF WS-FS-OUTFILE NOT EQUAL '00'                                  
                  DISPLAY 'WRITE OUTFILE FS:  ' WS-FS-OUTFILE                   
                  MOVE 2 TO RETURN-CODE                                         
                  STOP RUN                                                      
               END-IF                                                           
                                                                                
               IF WS-REC-CNT EQUAL 10                                           
                   MOVE ZEROS TO WS-REC-CNT                                     
               END-IF                                                           
                                                                                
           END-PERFORM                                                          
                                                                                
           CLOSE OUTFILE.                                                       
                                                                                
           IF WS-FS-OUTFILE NOT EQUAL '00'                                      
              DISPLAY 'CLOSE OUTFILE FS: ' WS-FS-OUTFILE                        
              MOVE 3 TO RETURN-CODE                                             
              STOP RUN                                                          
           END-IF                                                               
                                                                                
           DISPLAY 'FINISH'.                                                    
                                                                                
           STOP RUN.                                                            
                                                                                
       P201-FORMAT-OUTPUT.                                                      
                                                                                
           ADD  1 TO WS-IX                                                      
                                                                                
           MOVE 'NAME NUMBER ' TO WS-TEXT                                       
           MOVE WS-IX          TO WS-NO                                         
                                  OUT-REC-NO(WS-IX)                             
           MOVE WS-NAME        TO OUT-NAME  (WS-IX)                             
           .                                                                    
       P201-FORMAT-OUTPUT-EXIT.                                                 
           EXIT.                                                                
