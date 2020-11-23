from datetime import datetime
from typing import List

from dateutil import parser

from analysis.comparator import Comparator
from test.comparator_test import FakeComparable
from analysis.recurrences import RecurringCalculator, Recurring
from receiver.transactions import Comparable, Datable


class TestRecurringCalculator:
    def test_should_match_three_month_identical(self):
        input = [
            FakeTransaction("Netflix", "2020-10-10"),
            FakeTransaction("Netflix", "2020-09-10"),
            FakeTransaction("Netflix", "2020-08-10"),
        ]
        sut = RecurringCalculator(input, FakeComparator())

        expect = [Recurring(input, 0.293)]
        actual = sut.find_recurrences()
        assert actual == expect

    def test_should_match_similar_three_months(self):
        input = [
            FakeTransaction("netflix A/S", "2020-10-10"),
            FakeTransaction("Netflix", "2020-09-10"),
            FakeTransaction("netflix", "2020-08-10"),
        ]
        sut = RecurringCalculator(input, FakeComparator())

        expect = [Recurring(input, 0.293)]
        actual = sut.find_recurrences()
        assert actual == expect

    def test_should_match_weekly_identical(self):
        input = [
            FakeTransaction("Netflix", "2020-10-01"),
            FakeTransaction("Netflix", "2020-10-07"),
            FakeTransaction("Netflix", "2020-10-14"),
            FakeTransaction("Netflix", "2020-10-21"),
        ]
        sut = RecurringCalculator(input, FakeComparator())

        expect = [Recurring(input, 0.423)]
        actual = sut.find_recurrences()
        assert actual == expect

    def test_not_should_match_three_mixed_dates(self):
        input = [
            FakeTransaction("Netflix", "2020-10-01"),
            FakeTransaction("Netflix", "2020-09-15"),
            FakeTransaction("Netflix", "2020-08-25"),
        ]
        sut = RecurringCalculator(input, FakeComparator())

        expect = []
        actual = sut.find_recurrences()
        assert actual == expect

    def test_not_should_match_two_dates(self):
        input = [
            FakeTransaction("Netflix", "2020-10-10"),
            FakeTransaction("Netflix", "2020-09-10"),
        ]
        sut = RecurringCalculator(input, FakeComparator())

        expect = []
        actual = sut.find_recurrences()
        assert actual == expect

    def test_should_not_include_uniques(self):
        other = [FakeComparable("Other")]
        sut = RecurringCalculator(other)
        expect = []
        actual = sut.find_recurrences()

        assert actual == expect

    def test_should_not_recalculate_same_values(self):
        # WHEN: Calculating similarities with two similar items
        fake_comparator = FakeComparator()
        trans = [
            FakeTransaction("Netflix", "2020-10-10"),
            FakeTransaction("netflix", "2020-09-10"),
        ]
        sut = RecurringCalculator(trans, fake_comparator)
        sut.find_recurrences()

        # THEN: We should only calculate comparison once
        assert fake_comparator.times_called == 1


class TestRecurring:
    def test_recurring_repr(self):
        sut = Recurring([FakeTransaction("description", "2020-10-10")], 1.0)
        expect = f"<Recurring: members=[<FakeTransaction: 'description', '2020-10-10 00:00:00'>], variance=1.0"
        actual = sut.__repr__()
        assert actual == expect


class FakeTransaction(Datable, Comparable):
    def __init__(self, description: str, date: str) -> None:
        self.description = description
        self.datetime = parser.parse(date)

    def __repr__(self) -> str:
        return f"<FakeTransaction: '{self.description}', '{self.datetime}'>"

    def date(self) -> datetime:
        return self.datetime

    def comparandum(self) -> str:
        return self.description


class FakeComparator(Comparator):
    def __init__(self):
        self.times_called = 0

    def compare(self, present, others) -> List[Comparable]:
        self.times_called += 1
        return others
