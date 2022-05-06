       01  OUT-RECORD.                                                          
           03  OUT-KEY.                                                         
               05  OUTK-TYPE       PIC XX.                                      
               05  OUTK-SEQT       PIC 99.                                      
           03  OUT-REC-CNT         PIC S999    COMP-3.                          
           03  OUT-REC             OCCURS 1 TO 10 TIMES                         
                                   DEPENDING ON OUT-REC-CNT.                    
               05  OUT-REC-NO      PIC 9(09).                                   
               05  OUT-NAME        PIC X(21).