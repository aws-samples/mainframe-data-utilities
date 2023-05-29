# Mainframe Data Utilities V2

## Locally convert a single layout FB file

This page shows how to convert an EBCDIC file which has been downloaded to a local directory.

### Parse the copybook

Use the `parse` function to convert the copybook from Cobol to JSON representation.

This sample converts the [COBPACK2.cpy](/LegacyReference/COBPACK2.cpy) copybook file provided in [LegacyReference](/LegacyReference).

```
python3 src/mdu.py parse                \
        LegacyReference/COBPACK2.cpy    \
        sample-json/cobpack2-list.json  \
-input  sample-data/COBPACK.OUTFILE.txt \
-output sample-data/COBPACK.ASCII.txt   \
-print  10000 -verbose true
```

The [cobpack2-list.json](/sample-json/cobpack2-list.json) metadata will be generated at [sample-json](/sample-json)

### Convert the local file

Run the `extract` function to convert the `COBPACK.OUTFILE.txt` EBCDIC file into an ASCII file.

```
python3 src/mdu.py extract sample-json/cobpack2-list.json
```

The generated ASCII file will match the provided [COBPACK.ASCII.txt](/sample-data/COBPACK.ASCII.txt).

### More use cases

Check the [main page](/).