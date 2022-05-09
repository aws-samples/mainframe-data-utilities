000100 01  DB-WORK-AREA.                                                00000001
000200***************************************************************** 00000002
000300*                                                     02/28/84  * 00000003
000400*                 DIFS MASTER FILE -DATA BASE-                  * 00000004
000500*                                                               * 00000005
000600***************************************************************** 00000006
000700*                                                               * 00000007
000800*    THE COMPLETE RECORD CONSISTS OF TWO PARTS:                 * 00000008
000900*        FIRST IS THE HEADER PORTION PRECEEDING EITHER THE      * 00000009
001000*              PERSONAL, CHECK, OR POLICE DETAIL INFORMATION.   * 00000010
001100*              THE LENGTH IS  91 POSITIONS.                     * 00000011
001200*        SECOND PART CONTAINS THE APPROPIATE DETAIL FOR         * 00000012
001300*              EITHER PERSONAL, CHECK, OR POLICE RECORDS.       * 00000013
001400*              THE LENGTH OF THIS PART IS 199 BYTES.            * 00000014
001500*    TOTAL LENGTH OF THE COMPLETE RECORD IS 290 CHARACTERS.     * 00000015
001600***************************************************************** 00000016
001700* 11/02/92 RS7221 VJM  FULL MICR PROJECT:                       * 00000017
001800*          REDEFINED CK-AMT, ABA-NO, CKING-ACCOUNT-FULL         * 00000018
001900* 08/15/94 RS8894   O. MARTINEZ                                 * 00000019
002000*          ADDED FIELD  DB-CLR-AGE                              * 00000020
002100* 08/19/95 RS12555  O. MARTINEZ                                 * 00000021
002200*          ADDED DB-MASTER-KEY AND DB-OFFENSE-COUNT FIELDS      * 00000022
002300*          ADDED SEVERAL 88 LEVEL DATA NAMES.                   * 00000023
002400*          CHANGED DB-SECURITY-REF-NO FROM X(6) TO X(3).        * 00000024
JSC001* 05/05/03 RS0204260100 CAGNINA                                 * 00000025
JSC001*          DEFINED 2 NEW FIELDS IN FILLER AT END OF OFFENSE     * 00000026
JSC001*          RECORDS.  THESE ARE NEEDED TO STORE NUMBER OF        * 00000027
JSC001*          LEADING FM ACCOUNT ZEROES TRUNCATED FROM PRIMARY     * 00000028
JSC001*          AND SECONDARY FM'S IN OFFENSE RECORD.                * 00000029
JSC002* 09/23/03 RS0303270100 CAGNINA                                 * 00000030
JSC002*          DEFINED NEGATIVE DETAILS DATABASE FIELDS             * 00000031
JSC002*          RE-DEPOSIT CODE AND ACH-RETURN CODE                  * 00000032
JSC003* 09/24/03 IRJCAA5RPNAY CAGNINA                                 * 00000033
JSC003*          CHANGE LOCATION OF REDEPOSIT CODE AND ACH RETURN CODE* 00000034
JSC004* 01/14/03 RS0303270100 CAGNINA                                 * 00000035
JSC004*          DEFINE NDD COLLECTOR CODE FIELD                      * 00000036
DPM001* 01/26/09 RS0811131000 DPMOODY                                 * 00000037
DPM001*          ADD DB-PROPRIETARY-NEGATIVE-FLAG FROM FILLER;        * 00000039
DPM001*          88 LVLS FOR POA AND NON PROP NEG                     * 00000040
VJM001* 04/28/13 RS0082178  V.MARCHESINI   FRAUD PROCESS                        
VJM001*          ADD TR-FRAUD-INDICATOR TO INDICATE IF DELETE/UPDATE            
VJM001*          OF ID DUE TO FRAUD OR ASSERTED FRAUD (R3/R4/MND/DND)           
VJM002* 03/24/13 RS0082178  V.MARCHESINI   FRAUD PROCESS                        
VJM002*          BACK OUT PREVIOUS CHANGE.                                      
VJM003* 04/17/16 RS0162132  V.MARCHESINI   DIFS INFO                            
VJM003*          REPLACE DB-CHECK-INFO POS 285 FILLER W/DB-CK-UPDT-FLAG         
VJM004* 02/04/18 I170917781 V.MARCHESINI   DIFS INFO                            
VJM004*          REDEFINE CYCLE NUMBER FIELDS FOR                               
VJM004*          DB-USER-ID-PREFIX AND DB-USER-ID-SUFFIX                        
002500******************************************************************00000044
002600     05  DB-HEADER-RECORD.                                        00000045
002700         10  DB-SORT-CODE                  PIC X.                 00000046
002800         10  DB-ID-TYPE                    PIC XX.                00000047
002900         10  DB-MASTER-KEY.                                       00000048
003000             15  DB-ID-STATE-NUMBER.                              00000049
003100                 20  DB-ID-STATE           PIC XX.                00000050
003200                 20  DB-ID-NO              PIC X(24).             00000051
003300                                                                  00000052
003400             15  DB-RECORD-TYPE            PIC XX.                00000053
003500                 88  DB-PERSONAL-RECORD    VALUE '10'.            00000054
003600                 88  DB-OFFENSE-RECORD     VALUE '20'.            00000055
003700                                                                  00000056
003800             15  DB-FILE-SRCE-SYS-CODE     PIC XX.                00000057
003900                 88  DB-MDE-SOURCE         VALUE '10'.            00000058
004000                 88  DB-CLAIMS-SOURCE      VALUE '20'.            00000059
004100                 88  DB-TCS-SOURCE         VALUE '30'.            00000060
004200                 88  DB-PATHWAYS-SOURCE    VALUES                 00000061
004300                     '40', '50', '60'.                            00000062
004400                 88  DB-NEG-EXCHANGE-DATA  VALUE '70'.            00000063
004500                                                                  00000064
004600             15  DB-FILE-REF-NO.                                  00000065
004700                 20  DB-F-REF-N            PIC X(10).             00000066
004800                 20  DB-SEQ-NO             PIC 99.                00000067
004900         10  DB-STATUS                     PIC X.                 00000068
005000             88  DB-INACTIVE               VALUE '0'.             00000069
005100             88  DB-ACTIVE                 VALUE '1'.             00000070
005200                                                                  00000071
005300         10  DB-DELETE-CODE                PIC XX.                00000072
005400         10  DB-SRCE-REF-SS-CODE           PIC XX.                00000073
005500         10  DB-SRCE-REF-DOCUMENT-NO       PIC X(10).             00000074
005600         10  DB-INITIALS                   PIC XXX.               00000075
005700         10  DB-PREP-DATE                  PIC X(6).              00000076
VJM004         10  DB-TO-MASTER-CYCLE-NO.                               00000077
VJM004             15  DB-USER-ID-PREFIX         PIC XXX.               00000077
005900         10  DB-TO-MASTER-DATE.                                   00000078
006000             15  DB-TO-MASTER-MM           PIC X(2).              00000079
006100             15  DB-TO-MASTER-DD           PIC X(2).              00000080
006200             15  DB-TO-MASTER-YY           PIC X(2).              00000081
006300         10  DB-MAINT-CODE                 PIC X.                 00000082
006400             88  DB-DELETE-TRANS           VALUE '2'.             00000083
006500             88  DB-ADD-TRANS              VALUE '3'.             00000084
006600             88  DB-CHANGE-TRANS           VALUE '4'.             00000085
VJM004         10  DB-FILE-MAINT-CYCLE-NO.                              00000086
VJM004             15  DB-USER-ID-SUFFIX         PIC XXX.               00000077
006800         10  DB-FILE-MAINT-DATE.                                  00000087
006900             15  DB-FILE-MAINT-MM          PIC X(2).              00000088
007000             15  DB-FILE-MAINT-DD          PIC X(2).              00000089
007100             15  DB-FILE-MAINT-YY          PIC X(2).              00000090
007200         10  DB-CLR-AGE                    PIC X.                 00000091
007300             88  DB-CLR-LT-30-DAYS         VALUE '1'.             00000092
007400             88  DB-CLR-LT-60-DAYS         VALUE '2'.             00000093
007500             88  DB-CLR-LT-90-DAYS         VALUE '3'.             00000094
007600             88  DB-CLR-OVER-90-DAYS       VALUE '4'.             00000095
JSC003         10  DB-NEW-TXN-FLAG               PIC X(1).              00000096
JSC003         10  DB-REDEPOSIT-CODE             PIC X(1).              00000097
007800*                                                                 00000098
007900*    DATA BASE PERSONAL INFORMATION RECORD                        00000099
008000*                                                               * 00000100
008100     05  DB-PERSONAL-INFO-RECORD.                                 00000101
008200         10  DB-REASON-CODE                PIC X(2).              00000102
008300             88  DB-REASON-NEG             VALUE '10'.            00000103
008400             88  DB-REASON-LOST            VALUE '20'.            00000104
008500             88  DB-REASON-STOLEN          VALUE '30'.            00000105
008600             88  DB-REASON-SKIP            VALUE '40'.            00000106
008700         10  DB-AS-OF-DATE.                                       00000107
008800             15  DB-AS-OF-MM               PIC X(2).              00000108
008900             15  DB-AS-OF-DD               PIC X(2).              00000109
009000             15  DB-AS-OF-YY               PIC XX.                00000110
009100         10  DB-NAME-TITLE                 PIC X.                 00000111
009200         10  DB-LAST-NAME                  PIC X(18).             00000112
009300         10  DB-FIRST-NAME                 PIC X(12).             00000113
009400         10  DB-MIDDLE-INIT                PIC X.                 00000114
009500         10  DB-SSAN.                                             00000115
009600             15  DB-SSAN-1                 PIC X(3).              00000116
009700             15  DB-SSAN-2                 PIC X(2).              00000117
009800             15  DB-SSAN-3                 PIC X(4).              00000118
009900         10  DB-2ND-ID-TYPE                PIC X(3).              00000119
010000         10  DB-2ND-ID                     PIC X(20).             00000120
010100         10  DB-STREET-ADDR                PIC X(24).             00000121
010200         10  DB-CITY-ADDR                  PIC X(20).             00000122
010300         10  DB-STATE-ADDR                 PIC XX.                00000123
010400         10  DB-ZIP                        PIC X(5).              00000124
010500         10  DB-PERSONAL-PHONE.                                   00000125
010600             15  DB-PERSONAL-PHONE-AC      PIC X(3).              00000126
010700             15  DB-PERSONAL-PHONE-PRE     PIC X(3).              00000127
010800             15  DB-PERSONAL-PHONE-NO      PIC X(4).              00000128
010900         10  DB-SECURITY-REF-NO            PIC X(3).              00000129
011000         10  DB-OFFENSE-COUNT              PIC S9(5) COMP-3.      00000130
011100         10  DB-PERSONAL-RMKS1             PIC X(30).             00000131
011200         10  DB-PERSONAL-RMKS2             PIC X(30).             00000132
011300******************************************************************00000133
011400*    DATA BASE CHECK INFORMATION RECORD.                          00000134
011500******************************************************************00000135
011600     05  DB-CHECK-INFO                     REDEFINES              00000136
011700         DB-PERSONAL-INFO-RECORD.                                 00000137
011800         10  DB-CK-OFFENSE-CODE            PIC XX.                00000138
011900         10  DB-CK-DATE.                                          00000139
012000             15  DB-CK-MM                  PIC XX.                00000140
012100             15  DB-CK-DD                  PIC XX.                00000141
012200             15  DB-CK-YY                  PIC XX.                00000142
012300         10  DB-CK-TYPE                    PIC X.                 00000143
012400         10  DB-CK-SERIAL-NO               PIC X(9).              00000144
012500         10  DB-CK-PAYEE                   PIC X(24).             00000145
012600         10  DB-CK-AMT                     PIC X(7).              00000146
012700         10  DB-CK-AMT9                    REDEFINES              00000147
012800             DB-CK-AMT                     PIC S9(5)V99.          00000148
012900         10  DB-ABA-NO                     PIC 9(9)   COMP-3.     00000149
013000         10  DB-CKING-ACCOUNT-NO           PIC X(12).             00000150
013100         10  DB-CK-REPORTING-SRCE          PIC X(24).             00000151
013200         10  DB-CK-REPORTING-PHONE.                               00000152
013300             15  DB-CK-REPORTING-PHONE-AC  PIC XXX.               00000153
013400             15  DB-CK-REPORTING-PHONE-PRE PIC XXX.               00000154
013500             15  DB-CK-REPORTING-PHONE-NO  PIC XXXX.              00000155
013600         10  DB-CK-REPORTING-CONTACT.                             00000156
013700             15  DB-CKING-ACCOUNT-FULL     PIC X(18).             00000157
013800         10  DB-REPORTING-STATION-NO       PIC X(12).             00000158
013900         10  DB-CK-SEVERITY-CODE           PIC S999 COMP-3.       00000159
014000         10  DB-CHECK-RMKS1                PIC X(30).             00000160
014100         10  DB-CHECK-RMKS2.                                      00000161
014200             15  DB-CHECK-RMKS2-A          PIC X(20).             00000162
014300             15  DB-CHECK-RMKS2-B          PIC X(10).             00000163
014400         10  DB-CK-ZIP-REGION              PIC X.                 00000164
VJM003         10  DB-CK-UPDT-FLAG               PIC X.                 00000162
DPM001         10  DB-PROPRIETARY-NEGATIVE-FLAG  PIC X.                 00000166
DPM001             88  DB-NON-PROP-NEG           VALUE '0'.             00000167
DPM001             88  DB-POA                    VALUE '1'.             00000168
JSC004         10  DB-COLLECTOR-CODE             PIC XX.                00000169
JSC003         10  DB-ACH-RETURN-CODE            PIC XX.                00000170
014600******************************************************************00000171
014700*    DATA BASE POLICE INFORMATION RECORD                          00000172
014800******************************************************************00000173
014900     05  DB-POLICE-INFO                    REDEFINES              00000174
015000         DB-PERSONAL-INFO-RECORD.                                 00000175
015100         10  DB-PD-OFFENSE-CODE            PIC XX.                00000176
015200         10  DB-PD-DATE.                                          00000177
015300             15  DB-PD-DATE-MM             PIC XX.                00000178
015400             15  DB-PD-DATE-DD             PIC XX.                00000179
015500             15  DB-PD-DATE-YY             PIC XX.                00000180
015600         10  DB-WARRANT-NO                 PIC X(12).             00000181
015700         10  DB-BOOKING-NO                 PIC X(12).             00000182
015800         10  DB-PENAL-CODE                 PIC X(8).              00000183
015900         10  DB-SECURITY-ACTION-CODE       PIC XX.                00000184
016000         10  DB-SECURITY-ACTION            PIC X(24).             00000185
016100         10  DB-PD-WANTING-AGENCY          PIC X(24).             00000186
016200         10  DB-PD-PHONE-NO.                                      00000187
016300             15  DB-PD-PHONE-NO-AC         PIC XXX.               00000188
016400             15  DB-PD-PHONE-NO-PRE        PIC XXX.               00000189
016500             15  DB-PD-PHONE-NO-NO         PIC XXXX.              00000190
016600         10  DB-DETECTIVE-NAME             PIC X(18).             00000191
016700         10  DB-PD-CASE-NO                 PIC X(12).             00000192
016800         10  DB-PD-SEVERITY-CODE           PIC S999 COMP-3.       00000193
016900         10  DB-PD-RMKS1                   PIC X(30).             00000194
017000         10  DB-PD-RMKS2                   PIC X(30).             00000195
017100         10  DB-PD-FILL                    PIC X(7).              00000200
