"""
Extract s-v-o triples.
"""

import argparse
import collections
import csv
import logging
import os
import pickle
import re

from conll import CoNLLFile
from tqdm import tqdm


logger = logging.getLogger(__name__)


def main():
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    if os.path.exists(args.output):
        logger.error('Output file %s already exists', args.output)
        return

    logger.info('Extracting triples from %s', args.input)

    svo_triples = collections.defaultdict(int)
    conll_file = CoNLLFile(args.input)
    sentences = conll_file.load_conll()

    for sentence in sentences:
        subjs = {}
        objs = {}
        compounds = {}
        verbs = []

        invalid_sentence = False

        for line in sentence:
            pos_tag = line[3]
            head_id = int(line[6])
            relation = line[7]

            if relation == 'nsubj':
                # two subjs shouldn't have same root
                if head_id in subjs:
                    invalid_sentence = True
                    break
                subjs[head_id] = line
            # all possible obj relations and should be mutually exclusive
            elif relation in ['obj', 'ccomp', 'xcomp']:
                # two objs shouldn't have same root
                if head_id in objs:
                    invalid_sentence = True
                    break
                objs[head_id] = line
            elif pos_tag == 'VERB':
                verbs.append(line)
            elif 'compound' in line[7]:
                compounds[head_id] = line

        if invalid_sentence:
            continue

        for line in verbs:
            verb_id = int(line[0])
            verb_lemma = line[2]

            # skip verb if it is a compound
            if verb_id in compounds:
                continue

            if verb_id in subjs:
                subj_line = subjs[verb_id]
                subj_lemma = subj_line[2]
                subj_pos_tag = subj_line[3]

                if subj_pos_tag in ['NOUN', 'PROPN']:
                    if verb_id in objs:
                        obj_line = objs[verb_id]
                        obj_lemma = obj_line[2]
                        obj_pos_tag = obj_line[3]
                        obj_relation = obj_line[7]
                        if obj_relation == 'obj' and obj_pos_tag in ['NOUN', 'PROPN']:
                            svo_triples[(subj_lemma, verb_lemma, obj_lemma)] += 1
                    else:
                        svo_triples[(subj_lemma, verb_lemma, '[NONE]')] += 1

    logger.info('Writing triples to %s', args.output)
    with open(args.output, 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerows(svo_triples)


if __name__ == '__main__':
    main()
