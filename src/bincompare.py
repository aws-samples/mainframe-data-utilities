import datetime, json, sys

print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), ": started")

with open(sys.argv[1]) as json_file: param = json.load(json_file)

InpA=open(param["ascii"],"rb")
InpE=open(param["ebcdic"],"rb")

i=0

while i < param["max"] or param["max"] == 0:

    liASCII = InpA.read(param["lrecl"])
    liEBCDI = InpE.read(param["lrecl"])
    
    biASCII = b''
    biEBCDI = b''

    if not liEBCDI and not liASCII: break

    i += 1
    if(i % param["printeach"] == 0): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + " : " + str(i))

    ini = 0
    for layout in param["layout"]:

        fim = layout["val"]

        if layout["type"] == "bin":
            biASCII += liASCII[ini:fim]
            biEBCDI += liEBCDI[ini:fim]
        elif layout["type"] == "nobin":
            biASCII += liASCII[ini:fim].decode('utf-8').encode('cp037')      
            biEBCDI += liEBCDI[ini:fim]

        ini = fim

    biASCII += liASCII[ini:]
    biEBCDI += liEBCDI[ini:]

    if biASCII != biEBCDI:
        print("ASCII.: ", i)
        print(liASCII)
        print("EBCDIC: ", i)
        print(liEBCDI)
        print("==========================================================================================================================================================================")

print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), ": ended")