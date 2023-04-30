# Mainframe Data Utilities V2

## VB record format files

To convert a Variable Block file you only need to inform the `-input-recfm vb` when parsing the copybook:
```
python3 mdu.py parse                        \
        ../LegacyReference/COBVBFM2.cpy     \
        ../sample-json/COBVBFM2-list.json   \
-input  ../sample-data/COBVBFM2.EBCDIC.txt  \
-output ../sample-data/COBVBFM2.ASCII.txt   \
-input-recfm vb -verbose true
```



```
python3 mdu.py ../sample-json/COBVBFM2-list.json
```

### For another use cases

Check the [Read me](/docs/readme.md) page.