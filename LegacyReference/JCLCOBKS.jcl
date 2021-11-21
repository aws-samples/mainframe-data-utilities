//LGDCOBKS  JOB ' ',LUISDAN,CLASS=A,MSGCLASS=A,NOTIFY=&SYSUID           JOB03752
//**********************************************************************
//* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
//* SPDX-License-Identifier: Apache-2.0
//**********************************************************************        
//DELETE   EXEC PGM=IDCAMS                                                      
//SYSPRINT DD  SYSOUT=*                                                         
//SYSOUT   DD  SYSOUT=*                                                         
//SYSIN    DD  *                                                                
 DELETE LUISDAN.FLAT.CLIENT                                                     
 SET MAXCC=0                                                                    
 SET LASTCC=0                                                                   
//**********************************************************************        
//COBKS05  EXEC PGM=COBKS05                                                     
//STEPLIB  DD  DISP=SHR,DSN=LUISDAN.LOAD                                        
//INPUTF   DD  DISP=SHR,DSN=LUISDAN.SRC(INPUT2)                                 
//CLIENT   DD  DISP=SHR,DSN=LUISDAN.KSDS.CLIENT                                 
//SYSPRINT DD  SYSOUT=*                                                         
//SYSOUT   DD  SYSOUT=*                                                         
//**********************************************************************        
//EXTRACT  EXEC PGM=SORT                                                        
//SORTIN   DD  DISP=SHR,DSN=LUISDAN.KSDS.CLIENT                                 
//SORTOUT  DD  DSN=LUISDAN.FLAT.CLIENT,                                         
//             DISP=(,CATLG,DELETE),                                            
//             SPACE=(CYL,(1,1),RLSE),UNIT=3390,                                
//             DCB=(RECFM=FB,LRECL=500)                                         
//SYSPRINT DD  SYSOUT=*                                                         
//SYSOUT   DD  SYSOUT=*                                                         
//SYSIN    DD  *                                                                
 SORT FIELDS=COPY                                                                                                                      