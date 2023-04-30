# Mainframe Data Utilities V2

## Locally convert a multiple layout file

There are often multiple layouts in mainframe VSAM or sequential (flat) files. It means that you need a different transformation rule depending on the row you are reading.

The REDEFINES statement allows multiple layouts declaration in the COBOL language.

### Parsing a multiple layout copybook

The [COBKS05.cpy](/LegacyReference/COBKS05.cpy) is provided in the [LegacyReference](/LegacyReference/) folder as an example of a VSAM file copybook having three record layouts. The [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) is the EBCDIC sample that can be converted through the following steps.

From **/src** Run the `mdu.py` script, using the `parse` function, to parse the copybook file provided in [LegacyReference](/LegacyReference):

```
python3 mdu.py parse \
        ../LegacyReference/COBKS05.cpy   \
        ../sample-json/COBKS05-list.json \
-input  ../sample-data/CLIENT.EBCDIC.txt \
-output ../sample-data/CLIENT.ASCII.txt  \
-print  20 -verbose true
```

### Extracting a multiple layout file

2. The step above will generate the [COBKS05-list.json](/sample-json/COBKS05-list.json) with an empty transformation rules list: `"transf_rule"=[],`. Replace the transformation rule with the content bellow and save the `COBKS05-list-rules.json`:

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
            "hex": "0000",
            "transf": "transf2"
        }
    ],
```

The parameters above will inform the `extract` function that records having "0002" hexadecimal value between its 5th and 6th bytes must be converted through the layout specified in "transf1" layout, whereas records that contain "0000" at the same position will be extracted with the "transf2" layout.

The result of the change above must produce a file like [COBKS05-rules.json](/sample-json/COBKS05-rules.json).

3. From **/src** folder run `mdu.py extract` to extract the `CLIENT.EBCDIC.txt` into an ASCII file.

```
python3 mdu.py extract ../sample-json/COBKS05-list-rules.json
```

4. Check the [CLIENT.ASCII.txt](/sample-data/CLIENT.ASCII.txt) file.

### For another use cases

Check the [Read me](/docs/readme.md) page.