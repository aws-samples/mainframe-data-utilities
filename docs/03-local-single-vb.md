# Mainframe Data Utilities V2

## VB record format files

To convert a Variable Block file you only need to inform the `-input-recfm vb` when parsing the copybook.

From the **/src** folder run:
```
python3 mdu.py parse                        \
        ../LegacyReference/COBVBFM2.cpy     \
        ../sample-json/COBVBFM2-list.json   \
-input  ../sample-data/COBVBFM2.EBCDIC.txt  \
-output ../sample-data/COBVBFM2.ASCII.txt   \
-input-recfm vb -verbose true
```

The [COBVBFM2-list.json](/sample-json/COBVBFM2-list.json) metadata will be generated at [sample-json](/sample-json)

### Convert the local file

From the **/src** folder, run the `extract` function to convert the `/sample-data/COBVBFM2.EBCDIC.txt` EBCDIC file into an ASCII file.
```
python3 mdu.py extract ../sample-json/COBVBFM2-list.json
```

### For another use cases

Check the [Read me](/docs/readme.md) page.