# Mainframe Data Utilities V2

## VB record format files

```
python3 mdu.py parse                        \
        ../LegacyReference/COBVBFM2.cpy     \
        ../sample-json/COBVBFM2-list.json   \
-input  ../sample-data/COBVBFM2.EBCDIC.txt  \
-output ../sample-data/COBVBFM2.ASCII.txt   \
-input-recfm vb
```

```
python3 mdu.py ../sample-json/COBVBFM2-list.json
```

### Convert a sample MULTI-LAYOUT file

Check the [Multi-layout fb Sample](/docs/04-local-multi-fb.md) page.