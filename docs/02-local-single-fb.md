# Mainframe Data Utilities V2

## Locally convert a single layout FB file

### Parse a sample copybook

`mdu.py` is the root CLI script. Run the `parse` function to parse the [COBPACK2](/LegacyReference/COBPACK2.cpy) copybook file provided in [LegacyReference](/LegacyReference).

```
python3 mdu.py parse                        \
        ../LegacyReference/COBPACK2.cpy     \
        ../sample-json/cobpack2-list.json   \
-input  ../sample-data/COBPACK.OUTFILE.txt  \
-output ../sample-data/COBPACK.ASCII.txt    \
-print  10000 -verbose true
```

The [JSON metadata](/sample-json/cobpack2-list.json) will be generated at [sample-json](/sample-json)

### Convert the local file

Run the `extract` function to convert the `COBPACK.OUTFILE.txt` EBCDIC file into an ASCII file.

```
python3 mdu.py extract ../sample-json/cobpack2-list.json
```

The generated ASCCI file must match the provided [COBPACK.ASCII.txt](/sample-data/COBPACK.ASCII.txt).

### For another use cases

Check the [Read me](/docs/readme.md) page.