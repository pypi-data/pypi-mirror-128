"""
 Utility functions not related to I/O, that can be directly applied to a list
 of lists, where each sublist is a sentence, and contains entries of the form
 ((word, pos_tag, dom), iob)

"""
from collections import Counter
import copy


def get_tagset(sentences, with_prefix):
    """ Returns the set of entity types appearing in the list of sentences.

    If with_prefix is True, it returns both the B- and I- versions for each
    entity found. If False, it merges them (i.e., removes the prefix and only
    returns the entity type).

    """
    iobs = [iob for sent in sentences for (x,iob) in sent]

    tagset = set(iobs)
    if not with_prefix:
        tagset = set([t[2:] for t in list(tagset) if t != 'O'])
    return tagset


def get_IOB_counts(sentences):
    """ Return a counter with IOB labels and their frequency.

    """
    types2 =[ j[1] for sublist in sentences for j in sublist] #list of IOBs
    ner_tags = Counter()

    for i,x in enumerate(types2):
        ner_tags[x] += 1

    return ner_tags
