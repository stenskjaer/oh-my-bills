from typing import List, Dict, Set
import pandas as pd


class Comparator:
    def find_similars(
        self, present: "Transaction", others: List["Transaction"]
    ) -> List["Transaction"]:
        scores = pd.Series(self._compare_descriptions(present, others))
        dev = scores.std()
        most_similar = scores[scores > dev]
        return most_similar.index

    def _compare_descriptions(
        self, present: "Transaction", others: List["Transaction"]
    ) -> Dict["Transaction", float]:
        res = {}
        for other in others:
            quotient = self._similarity(present.description, other.description)
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

    def _find_ngrams(self, text: str, size: int = 3) -> set:
        ngrams: Set[str] = set()
        if not text:
            return ngrams

        padded = f" {text} ".lower()
        for x in range(0, len(padded) - size + 1):
            ngrams.add(padded[x : x + size])
        return ngrams


class Transaction:
    def __init__(
        self,
        description: str,
        comparator: Comparator = Comparator(),
        amount=0,
        date="",
    ) -> None:
        self.description = description
        self.normalized_description = self.normalize(description)
        self.amount = amount
        self.date = date
        self.comparator = comparator

    def __repr__(self) -> str:
        return f"{self.normalized_description}"

    def normalize(self, description: str) -> str:
        return description

    def find_similars(self, transactions: List["Transaction"]) -> List["Transaction"]:
        return self.comparator.find_similars(self, transactions)


class Recurring:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions
        self.confidence = "calculated_confidence()"
        self.interval = "calculate_interval()"
        self.average_amount = "calculate_average()"
