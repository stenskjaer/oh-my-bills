from typing import List, Set, Union

import pandas as pd

from analysis.comparator import TrigramSimilarity, Comparator
from receiver.transactions import Comparable, Datable


class Recurring:
    """Represents a collection of recurring payments that belong together."""

    def __init__(
        self, members: List[Union[Comparable, Datable]], variance: float
    ) -> None:
        self.members = members
        self.variance = variance

    def __eq__(self, other) -> bool:
        return (self.members, self.variance) == (other.members, other.variance)

    def __repr__(self) -> str:
        return f"<Recurring: members={self.members}, variance={self.variance}"


class RecurringCalculator:
    """Identifies recurring payments from a list of Transactions."""

    def __init__(
        self,
        transactions: List[Comparable],
        comparator: Comparator = TrigramSimilarity(),
    ) -> None:
        self.transactions = transactions
        self.comparator = comparator

    def find_recurrences(
        self,
    ) -> List[Recurring]:
        """Determines which entries are likely to be recurring payments and
        returns them.

        We only calculate recurrence on collections larger than two, as we can't
        estimate a recurrence with only two observations.
        """
        similar = self._find_similar(self.transactions)

        recurring: List[Recurring] = []
        for group in similar:
            if len(group) > 2:
                distance = self._calculate_recurring(group)
                if 0 < distance < 5:
                    recurring.append(Recurring(group, distance))
        return recurring

    def _find_similar(
        self, transactions: List[Comparable]
    ) -> List[List[Union[Comparable, Datable]]]:
        """Collects lists of transactions that are textually similar.

        Items that don't have any similarity sibling in the list of transactions will
        not be included in the result.

        The `comparator` returns a collection of all similar entries. This means that
        once an entry has been included once, we shouldn't include it again, as it
        would result in duplicate collections. So before running comparisons on an
        item, we check that it hasn't already been done in another connection.
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

    def _calculate_recurring(self, group: List[Datable]) -> float:
        """Compare the transaction dates for the transactions in the collection of
        similar entries. If they are sufficiently even spread out, then we estimate
        them to be a recurring payment.

        We estimate the likelihood by subtracting the standard deviation of the
        differences between the payments from the span between the shortest and
        the longest duration between payments. This turns out to be a good heuristic
        for some wiggle-room for weekday or monthly variations in recurring payments.

        TODO: This heuristic could be replaced by a more solid evaluation of recurrence.
        """
        deltas = pd.Series(self._deltas(group))
        distance = deltas.max() - deltas.min()
        closeness = round(distance - deltas.std(), 3)
        return closeness

    @staticmethod
    def _deltas(datables: List[Datable]) -> List[int]:
        deltas: List[int] = []
        try:
            for idx in range(len(datables)):
                delta = abs(datables[idx].date() - datables[idx + 1].date())
                deltas.append(delta.days)
        except IndexError:
            pass
        return deltas
