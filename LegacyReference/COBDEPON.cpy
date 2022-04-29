       01  VSAM-RECORD.                                        
           03  VSAM-KEY.                                     
               05  VSAM-K-TYPE PIC XX.                   
               05  VSAM-K-SEQT PIC 99.            
           03  VSAM-REC-CNT    PIC S999    COMP-3.    
           03  VSAM-REC        OCCURS 1 TO 15 TIMES           
                               DEPENDING ON SEG-CNT.
               05  REC-NO      PIC 9(9).              
               05  LAST-NAME   PIC X(18).             
               05  FIRST-NAME  PIC X(12).             
               05  STATE       PIC XX.                            