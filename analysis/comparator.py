from abc import ABC, abstractmethod
from typing import List, Dict, Set

import pandas as pd

from receiver.transactions import Transaction, Comparable


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
        scores = pd.Series(self._run_comparison(present, others))
        dev = scores.std()
        most_similar = scores[scores > dev]
        return most_similar.index.tolist()

    def _run_comparison(
        self, present: Comparable, others: List[Comparable]
    ) -> Dict[Comparable, float]:
        res = {present: 1.0}
        for other in others:
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
    def _find_ngrams(text: str, size: int = 3) -> set:
        ngrams: Set[str] = set()
        if not text:
            return ngrams

        padded = f" {text} ".lower()
        for x in range(0, len(padded) - size + 1):
            ngrams.add(padded[x : x + size])
        return ngrams
