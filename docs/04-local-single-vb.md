# Mainframe Data Utilities V2

## VB record format files

To convert a Variable Block file you need to inform the `-input-recfm vb` when parsing the copybook. Run the `parse` function to convert the copybook:
```
python3 src/mdu.py parse                \
        LegacyReference/COBVBFM2.cpy    \
        sample-json/COBVBFM2-list.json  \
-input  sample-data/COBVBFM2.EBCDIC.txt \
-output sample-data/COBVBFM2.ASCII.txt  \
-input-recfm vb -verbose true
```

The [COBVBFM2-list.json](/sample-json/COBVBFM2-list.json) metadata will be generated at [sample-json](/sample-json)

### Convert the local file

Run the `extract` function to convert the `/sample-data/COBVBFM2.EBCDIC.txt` EBCDIC file into an ASCII file.
```
python3 src/mdu.py extract sample-json/COBVBFM2-list.json
```

### More use cases

Check the [main page](/).