from typing import List, Set

from analysis.comparator import TrigramSimilarity, Comparator
from receiver.transactions import Comparable


class Recurring:
    def __init__(self):
        self.confidence = "calculated_confidence()"
        self.interval = "calculate_interval()"
        self.average_amount = "calculate_average()"


class RecurringCalculator:
    def __init__(
        self,
        comparator: Comparator = TrigramSimilarity(),
    ):
        self.comparator = comparator
        self.similarity_cache: Set[str] = set()

    def find_similar(self, transactions: List[Comparable]) -> List[List[Comparable]]:
        similar: List[List[Comparable]] = []

        for trans in transactions:
            # Skip calculation if already computed
            if trans.comparandum() in self.similarity_cache:
                continue

            similar_transactions = self.comparator.compare(trans, transactions)

            self.similarity_cache.update(
                [t.comparandum() for t in similar_transactions]
            )
            similar.append(similar_transactions)
        return similar

    def find_recurrences(
        self, transactions: List[Comparable]
    ) -> List[List[Comparable]]:
        similar = self.find_similar(transactions)
        # recurring_confidence = calculate_recurring()
        # if (recurring_confidence > threshold):
        #    Recurring(similars + trans, confidence)
        return similar
