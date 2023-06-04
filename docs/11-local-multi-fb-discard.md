# Mainframe Data Utilities V2

## Locally convert a multiple layout file and discard specificy record types

### Parse a multiple layout copybook

The [COBKS05.cpy](/LegacyReference/COBKS05.cpy) is provided in the [LegacyReference](/LegacyReference/) folder as an example of a VSAM or a flat file copybook having three record layouts. The [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) is the EBCDIC sample that can be converted through the following steps.

Run the `src/mdu.py` script, using the `parse` function, to convert the copybook file provided in [LegacyReference](/LegacyReference) from Cobol to JSON representation:

```
python3 src/mdu.py parse \
        LegacyReference/COBKS05.cpy   \
        sample-json/COBKS05-list-disc.json \
-input  sample-data/CLIENT.EBCDIC.txt \
-output sample-data/CLIENT.ASCII-disc.txt  \
-print  20 -verbose true
```

### Add the transformation rules

2. The step above will generate the [COBKS05-list-disc.json](/sample-json/COBKS05-list-disc.json) with an empty transformation rules list: `"transf_rule"=[],`. To discard the record types 0 and 1 replace the transformation rule with the content bellow and save it:

```
    "transf_rule": [
        {
            "offset": 4,
            "size": 2,
            "hex": "0002",
            "transf": "transf1"
        },
        {
            "offset": 4,
            "size": 2,
            "hex": "0001",
            "transf": "discard"
        },
        {
            "offset": 4,
            "size": 2,
            "hex": "0000",
            "transf": "discard"
        }
    ],
```

The parameters above will inform the `extract` function that records having "0002" hexadecimal value between its 5th and 6th bytes must be converted through the layout specified in "transf1" layout, whereas records that contain "0000" or "0001" at the same position will be discarded.

The result of the change above must produce a file like [COBKS05-list-disc-rules.json](/sample-json/COBKS05-list-disc-rules.json).

### Extract a multiple layout file

3. Run the `src/mdu.py extract` fucntion to extract the `CLIENT.EBCDIC.txt` into an ASCII file.

```
python3 src/mdu.py extract sample-json/COBKS05-list-disc.json
```

4. Check the [CLIENT.ASCII-disc.txt](/sample-data/CLIENT.ASCII-disc.txt) file.

### More use cases

Check the [main page](/).
