from typing import List

from analysis.comparator import Comparator
from analysis.comparator_test import FakeComparable
from analysis.recurrences import RecurringCalculator
from receiver.transactions import Comparable, Transaction


class TestRecurringCalculator:
    def test_should_match_identical(self):
        netflixes = [FakeComparable("Netflix"), FakeComparable("Netflix")]
        other = [FakeComparable("Other")]
        sut = RecurringCalculator()

        expect = [netflixes]
        actual = sut.find_recurrences(netflixes + other)
        assert actual == expect

    def test_should_not_include_uniques(self):
        other = [FakeComparable("Other")]
        sut = RecurringCalculator()
        expect = []
        actual = sut.find_recurrences(other)

        assert actual == expect

    def test_should_not_recalculate_same_values(self):
        # WHEN: Calculating similarities with two similar items
        fake_comparator = FakeComparator()
        sut = RecurringCalculator(fake_comparator)
        sut.find_recurrences([Transaction("Netflix"), Transaction("netflix")])

        # THEN: We should only calculate comparison once
        assert fake_comparator.times_called == 1


class FakeComparator(Comparator):
    def __init__(self):
        self.times_called = 0

    def compare(self, present, others) -> List[Comparable]:
        self.times_called += 1
        return others
