025097 01  STOCK-MASTER.                                              
025100     05  STOCK-KEY.                                             
025102         10  STOCK-ITEM-ID            PIC X(09).
025104         10  STOCK-RECORD-TYPE        PIC X(01).                
025105             88  STOCK-TYPE1            VALUE '1'.              
025106             88  STOCK-TYPE2            VALUE '2'.              
025107         10  FILLER                   PIC X(10).                
025112     05  STOCK-INVENTORY-U-M          PIC X(04).                
025122     05  STOCK-DESCRIPTION-DATA OCCURS  2 TIMES.                
025123         10  STOCK-LINE-NO            PIC 9(02).                
025124         10  STOCK-DESCRIPTION        PIC X(40).                
025125         10  STOCK-INTERNAL-USE-IND   PIC X(01).                
025126             88  STOCK-INTERNAL-USE-ONLY VALUE 'Y'.             
025127             88  STOCK-NOT-INTERNAL-USE VALUE 'N'.              
025192     05  FILLER                      PIC X(09).                 
025193     05  STOCK-CONVERSION-DATA  OCCURS  2 TIMES.                
025194         10  STOCK-ALTERNATE-U-M       PIC X(04).               
025195         10  STOCK-CONVERSION-FACTOR   PIC 9(05)V9(04)  COMP-3. 
025196         10  STOCK-USE-DESIGNATOR      PIC X(02).               
025206     05  STOCK-DEFAULT-UNIT-PRICE      PIC S9(08)V9(05) COMP-3. 
025207     05  STOCK-CLASS-CODE              PIC X(04).               
025208     05  STOCK-CUS-ORDER-PROC-IND      PIC X(01).               
025209         88  STOCK-USE-COPS-DATA        VALUE 'Y'.              
025210         88  STOCK-COPS-DATA-NOT-USE    VALUE 'N'.              
025211     05  STOCK-MFG-PUR-IND             PIC X(01).               
025212         88  STOCK-USE-FOR-MRP          VALUE 'Y'.              
025213         88  STOCK-NOT-USED-FOR-MRP     VALUE 'N'.              
025214     05  STOCK-GSS-IND                 PIC X(01).				
025215         88  STOCK-IGNORE              VALUE 'I'.              
025216         88  STOCK-COLLECT-INFO        VALUE 'C'.              
025217         88  STOCK-GSS                 VALUE 'F'.              
025218     05  STOCK-BUYER                   PIC 9(03).              
025219     05  STOCK-PRICE-IND               PIC X(01).              
025220         88  STOCK-ITEM-LEVEL-STD-COST  VALUE '5'.             
025221     05  STOCK-SHELF-LIFE              PIC S9(3)        COMP-3.
025222     05  STOCK-SALES-PRICE             PIC S9(8)V9(5)   COMP-3.
025223     05  STOCK-CUST-DATA               PIC X(104).             
025224     05  STOCK-SAP-CUST REDEFINES STOCK-CUST-DATA.             
025225         10 STOCK-SAP-CUST-DATA        PIC X(71).              
025226         10 STOCK-SAP-OTHER-DATA.                              
025227           15 STOCK-OH-UNPRICED-QTY    PIC S9(09)V9(04) COMP-3.
025228           15 STOCK-OH-PRICED-QTY      PIC S9(09)V9(04) COMP-3.
025229           15 STOCK-INVEN-VALUE        PIC S9(09)V9(02) COMP-3.
025230           15 STOCK-PAID-NOT-RECVD-QTY PIC S9(09)V9(04) COMP-3.
025231           15 FILLER                    PIC X(6).              
025232     05  STOCK-STD-CUST REDEFINES STOCK-CUST-DATA.             
025233         10 STOCK-STD-CUST-DATA.                               
025234             15 FILLER                  PIC X(61).             
025235             15 STOCK-CP-SIZE         PIC X(10).               
025236         10 STOCK-STD-OTHER-DATA.                              
025237             15 STOCK-NEW-STD-COST    PIC S9(08)V9(05) COMP-3. 
025238              15  STOCK-TAX-CLASS     PIC X(01).               
025239              15  FILLER                PIC X(25).             
025240*                                                              
025241     05  STOCK-ITEM-USER-DATA REDEFINES STOCK-CUST-DATA.       
025242         10 STOCK-SAP-CUST-DATA.                               
025243            15  STOCK-LOC             PIC 9(03).               
025244                88  NUM01                     VALUE 001.       
025245                88  NUM02                     VALUE 002.       
025246                88  NUM03                     VALUE 003.       
025255            15  STOCK-PRIME-LOC-DEFAULT PIC X(03).             
025256            15  STOCK-PROD-TYPE       PIC X(02).               
025257            15  STOCK-PROD-CLASS      PIC 9(03).               
025258            15  STOCK-PRODUCT-LENGTH  PIC 9(07).               
025259            15  STOCK-PROD-FEET-INCH REDEFINES                 
025260                                    STOCK-PRODUCT-LENGTH.      
025261                20  STOCK-PROD-FEET   PIC 9(03).               
025262                20  STOCK-PROD-INCH   PIC 9(02).               
025263                20  STOCK-PROD-FRAC-OF-INCH PIC 9(02).         
025264                20  STOCK-PROD-FRAC-OF-INCH-REDF REDEFINES     
025265                         STOCK-PROD-FRAC-OF-INCH.              
025266                   30  STOCK-FOI-1    PIC 9(01).               
025267                   30  STOCK-FOI-2    PIC 9(01).               
025268            15  FILLER                  PIC X(7).              
025269            15  STOCK-QUANTITY-CHECK  PIC S9(07) COMP-3.
025270            15  STOCK-QTY-CHECK-IND   PIC X(01).               
025271                88  STOCK-QTY-CHECK-GT    VALUE 'G'.           
025272                88  STOCK-QTY-CHECK-LT    VALUE 'L'.           
025273            15  STOCK-VOP-DISC-IND    PIC X(01).               
025274                88  STOCK-VOP-ALLOWED     VALUE 'Y'.           
025275                88  STOCK-NO-VOP-ALLOWED  VALUE 'N'.           
025276            15  STOCK-PRICE-UOM-1     PIC X(04).               
025277            15  STOCK-PRICE-QTY-1     PIC S9(05) COMP-3.       
025278            15  STOCK-PRICE-UOM-2     PIC X(04).               
025279            15  STOCK-PRICE-QTY-2     PIC S9(05) COMP-3.       
025280            15  STOCK-PRICE-UOM-3     PIC X(04).               
025281            15  STOCK-PRICE-QTY-3     PIC S9(05) COMP-3.       
025282            15  STOCK-UPC-CODE        PIC X(14).               
025283            15  STOCK-DISCONTINUED-IND PIC X.                  
025284                88  STOCK-DISCONTINUED-ITEM VALUE 'Y'.         
025285            15  STOCK-PREPACK-IND     PIC X.                   
025286                88  STOCK-PREPACK         VALUE 'Y'.           
025287                88  STOCK-NOT-PREPACK     VALUE 'N'.           
025288            15  STOCK-LIFO-IND        PIC 9(3).                
025289            15 STOCK-STD-COST-USER-DATA PIC S9(08)V9(05)       
025290                                                   COMP.       
025291            15  STOCK-DONT-USE-THIS-AREA PIC X(14).            
025292            15  STOCK-DONT-USE-THIS-EITHER PIC X(12).          
