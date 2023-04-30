## Multiple layout support

There are often multiple layouts in mainframe VSAM or sequential (flat) files. It means that you need a different transformation rule depending on the row you are reading.

The REDEFINES statement allows multiple layouts declaration in the COBOL language.

### Parsing a multiple layout copybook

The [COBKS05.cpy](LegacyReference/COBKS05.cpy) is provided in [LegacyReference](LegacyReference/) folder as an example of a VSAM file copybook having three record layouts. The [CLIENT.EBCDIC.txt](sample-data/CLIENT.EBCDIC.txt) is the EBCDIC sample that can be converted through the following steps.

1. Run the `parse_copybook_to_json.py` script to parse the copybook file provided in `sample-data`.

```
python3   parse_copybook_to_json.py     \
-copybook LegacyReference/COBKS05.cpy   \
-output   sample-data/COBKS05-list.json \
-dict     sample-data/COBKS05-dict.json \
-ebcdic   sample-data/CLIENT.EBCDIC.txt \
-ascii    sample-data/CLIENT.ASCII.txt  \
-print    20
```

### Extracting a multiple layout file

2. The step above will generate the [COBKS05-list.json](sample-data/COBKS05-list.json) with empty transformation rules: `"transf-rule"=[],`. Replace the transformation rule with the content bellow and save the `COBKS05-list.json`:

```
 "transf-rule": [
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

The parameters above will inform the `extract_ebcdic_to_ascii.py` script that records having "0002" hexadecimal value between its 5th and 6th bytes must be converted through the layout specified in "transf1" layout, whereas records that contain "0000" at the same position will be extracted with the "transf2" layout.

The result of the change above must produce a file like [COBKS05-rules.json](sample-data/COBKS05-rules.json).

3. Run `extract_ebcdic_to_ascii.py` to extract the `CLIENT.EBCDIC.txt` into an ASCII file.

```
python3 extract_ebcdic_to_ascii.py -local-json sample-data/COBKS05-list.json
```

4. Check the [CLIENT.ASCII.txt](sample-data/CLIENT.ASCII.txt) file.