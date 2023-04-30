# Mainframe Data Utilities V2

## Convert a local file

### Parse the copybook

```
./mdu.py parsecopy \
../LegacyReference/COBPACK2.cpy \
../sample-json/cobpack2-list.json \
-input ../sample-data/COBPACK.OUTFILE.txt \
-output ../sample-data/COBPACK.ASCII.txt \
-json-debug ../sample-json/cobpack2-dict.json \
-print 10000 -verbose 1
```

### Convert the local file

```
./mdu.py extract ../sample-json/cobpack2-list.json
```