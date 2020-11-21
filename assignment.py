"""
Structure
1. Word object with string and mask fields.
2. Create mask for all strings and put into list.
3. Sort the list based on the mask.
4. Run the list to check for similarities
5. Register similarities for repeating check.
6. Check repeating by matching closeness and regularity.

Runtime:
Docker starting a web server.

Interface:
REST API for interaction
- PUT csv with data (alternatively load data when starting docker)
- GET recurring payments -> JSON object {[{recurring object}]}
- GET is given entry recurring?
"""
from collections import namedtuple
from typing import List
import re


lines = ["man", "men", "cat", "stras", "tsras"]

Word = namedtuple("Word", "value mask")


def ngrams(input_value: str, n: int = 3) -> List[str]:
    """Create ngrams from the input word, by default a trigram."""
    normalized_word = normalize(input_value)
    ngrams = zip(*[normalized_word[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]


def normalize(input_value: str) -> str:
    """
    Normalize to avoid ambiguity due to non-essential variations.
    """

    def remove_punctuation(input: str) -> str:
        rx = "[" + re.escape("().,-|[]{}'") + "]"
        return re.sub(rx, "", input)

    def strip_pad_string(input: str) -> str:
        return " " + input.strip() + " "

    no_punctuation = remove_punctuation(input_value.lower())
    return strip_pad_string(no_punctuation)


print([ngrams(w) for w in lines])