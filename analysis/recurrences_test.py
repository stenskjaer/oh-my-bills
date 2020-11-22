from analysis.comparator_test import FakeComparable
from analysis.recurrences import RecurringCalculator


class TestRecurringCalculator:
    descriptions = [
        "UDK STUDIEGÆLD",
        "UDK STUDIEGÆLD",
        "UDS STUDIEGÆLD",
        "Netflix",
        "netflix",
        "netfix",
        "flexnet",
        "fixnet",
        "NotFix",
        "Netflix A/S",
        "Netflix Aps.",
    ]

    def test_should_match_identical(self):
        netflixes = [FakeComparable("Netflix"), FakeComparable("Netflix")]
        other = [FakeComparable("Other")]
        sut = RecurringCalculator(netflixes + other)
        expect = [netflixes, other]
        actual = sut.find_recurrences()

        assert actual == expect
        # assert self.similarity_cache == set(descriptions)
