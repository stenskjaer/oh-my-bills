from typing import List, Set, Dict

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

    def find_similar(self, transactions: List[Comparable]) -> List[List[Comparable]]:
        """Collects lists of transactions that are textually similar.

        Items that don't have any similarity sibling in the list of transactions will
        not be included in the result.

        The `comparator` returns a collection of all similar entries, which means
        that once an entry has been included once, we shouldn't include it again.
        That would result in duplicate collections. So before running comparisons on
        an item, we check that it hasn't already been done in another connection.
        """
        similarity_calculated: Set[str] = set()
        similar: List[List[Comparable]] = []

        for trans in transactions:
            if trans.comparandum() in similarity_calculated:
                continue

            similar_transactions = self.comparator.compare(trans, transactions)

            if len(similar_transactions) > 1:
                similarity_calculated.update(
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
