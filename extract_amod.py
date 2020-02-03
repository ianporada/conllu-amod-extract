"""
Extract amod relations.
"""

import argparse
import os
import collections
import csv

from conll import CoNLLFile


def main():
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    # build document
    print('Extracting amod bigrams from directory: %s' % args.input)

    amod_bigrams = collections.defaultdict(int)

    for directory, subdirectories, files in os.walk(args.input):
        for file in files:
            fname = os.path.join(directory, file)
            conll_file = CoNLLFile(fname)
            sents = conll_file.load_conll()

            for sent in sents:
                for i in range(0, len(sent)):
                    line = sent[i]
                    if line[7] == 'amod':
                        amod = line[2] # get the lemma
                        noun_idx = int(line[6])
                        noun_line = sent[noun_idx]
                        if noun_line[3] == 'NN' or noun_line[3] == 'NOUN':
                            noun = noun_line[2] # get the lemma
                            amod_bigrams[(amod, noun)] += 1

    print('Writing to output file: %s' % args.output)

    with open(args.output, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for k, v in amod_bigrams.items():
            amod, noun = k
            writer.writerow([amod.lower(), noun.lower(), v])

    print('done.')


if __name__ == '__main__':
    main()
