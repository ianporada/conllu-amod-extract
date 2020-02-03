# conllu-amod-extract
Really simple script for extracting (noun, adjective) bigrams from conllu files.

Usage (where `$INPUT_DIR` is a directory of `.conllu` files; `$OUTPUT_FNAME` is a `.tsv`):
```shell script
python extract_amod.py $INPUT_DIR $OUTPUT_FNAME
```