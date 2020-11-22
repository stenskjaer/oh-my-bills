from abc import ABC, abstractmethod
from typing import List, Dict, Set

import pandas as pd

from receiver.transactions import Comparable


class Comparator(ABC):
    @abstractmethod
    def compare(self, present, others) -> List[Comparable]:
        pass


class TrigramSimilarity:
    """TrigramSimilarity compares a transaction description with other transactions
    to identify similar transactions."""

    def compare(
        self, present: Comparable, others: List[Comparable]
    ) -> List[Comparable]:
        self.has_comparandum(present)

        scores = pd.Series(self._run_comparison(present, others))
        most_similar = self._bigger_than_cutoff(scores)
        return most_similar.index.tolist()

    def _bigger_than_cutoff(self, scores: pd.Series) -> pd.Series:
        """Identifies all the values that have a similarity scores bigger than the
        first standard deviation from the mean. If they are all identical we return
        everything.
        """
        if scores.mean() == 1.0:
            return scores
        dev = scores.std()
        most_similar = scores[scores > dev]
        return most_similar

    def _run_comparison(
        self, present: Comparable, all: List[Comparable]
    ) -> Dict[Comparable, float]:
        res = {}
        for other in all:
            self.has_comparandum(other)
            quotient = self._similarity(present.comparandum(), other.comparandum())
            res[other] = quotient
        return res

    def _similarity(self, text1: str, text2: str, number: int = 3) -> float:
        """
        Finds the similarity between 2 strings using ngrams.
        0 being completely different strings, and 1 being equal strings
        """

        ngrams1 = self._find_ngrams(text1, number)
        ngrams2 = self._find_ngrams(text2, number)

        num_unique = len(ngrams1 | ngrams2)
        num_equal = len(ngrams1 & ngrams2)
        return float(num_equal) / float(num_unique)

    @staticmethod
    def has_comparandum(present):
        if not present.comparandum():
            raise ValueError(f"{present}.comparandum() cannot be an empty string.")

    @staticmethod
    def _find_ngrams(text: str, size: int = 3) -> set:
        ngrams: Set[str] = set()

        padded = f" {text} ".lower()
        for x in range(0, len(padded) - size + 1):
            ngrams.add(padded[x : x + size])
        return ngrams
