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
        transactions: List[Comparable],
        comparator: Comparator = TrigramSimilarity(),
    ):
        self.transactions = transactions
        self.comparator = comparator
        self.similarity_cache: Set[str] = set()

    def find_similar(self) -> List[List[Comparable]]:
        similar: List[List[Comparable]] = []

        for trans in self.transactions:
            print("cache: ", self.similarity_cache)
            # Skip if already computed
            if trans.comparandum() in self.similarity_cache:
                print(f"'{trans.comparandum()}' in cache, skipping computation")
                continue

            similar_transactions = self.comparator.compare(trans, self.transactions)
            similar_descriptions = [t.comparandum() for t in similar_transactions]

            print("adding to cache: ", similar_descriptions)
            self.similarity_cache.update(similar_descriptions)
            similar.append(similar_transactions)
        return similar

    def find_recurrences(self) -> List[List[Comparable]]:
        similar = self.find_similar()
        # recurring_confidence = calculate_recurring()
        # if (recurring_confidence > threshold):
        #    Recurring(similars + trans, confidence)
        return similar
