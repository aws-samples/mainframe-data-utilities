//LUISDAN1 JOB (COBUNPACK),'DANTAS',CLASS=A,MSGCLASS=A,
//         TIME=1440,NOTIFY=&SYSUID
//**********************************************************************
//* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
//* SPDX-License-Identifier: Apache-2.0
//**********************************************************************
//COBPACK  EXEC PGM=COBPACK2
//STEPLIB  DD  DISP=SHR,DSN=LUISDAN.LOAD
//SYSPRINT DD  SYSOUT=*
//UTPRINT  DD  SYSOUT=*
//SYSOUT   DD  SYSOUT=*
//OUTFILE  DD  DISP=(SHR,CATLG,CATLG),
//             DSN=LUISDAN.COBPACK.OUTFILE,
//             SPACE=(CYL,(1,1),RLSE)
