# Mainframe Data Utilities V2

## Convert a file locally

### Clone this repo:

```
git clone git@github.com:aws-samples/mainframe-data-utilities.git.
```

### Change directory:

```
cd mainframe-data-utilities/src
```

### Parse a sample copybook

`mdu.py` is now the root CLI script. Run the `parse` function to parse the [COBPACK2](/LegacyReference/COBPACK2.cpy) copybook file provided in `sample-data`.

```
python3 mdu.py parse \
../LegacyReference/COBPACK2.cpy \
../sample-json/cobpack2-list.json \
-input ../sample-data/COBPACK.OUTFILE.txt \
-output ../sample-data/COBPACK.ASCII.txt \
-json-debug ../sample-json/cobpack2-dict.json \
-print 10000 -verbose 1
```

### Convert the local file

3. Run `extract`function to concert the `COBPACK.OUTFILE.txt` EBCDIC file into an ASCII file.

```
python3 mdu.py extract ../sample-json/cobpack2-list.json
```

The generated ASCCI file must martch the provided [COBPACK.ASCII.txt](sample-data/COBPACK.ASCII.txt).