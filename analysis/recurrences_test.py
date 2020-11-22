from analysis.comparator_test import FakeComparable
from analysis.recurrences import RecurringCalculator


class TestRecurringCalculator:
    def test_should_match_identical(self):
        netflixes = [FakeComparable("Netflix"), FakeComparable("Netflix")]
        other = [FakeComparable("Other")]
        sut = RecurringCalculator()
        expect = [netflixes, other]
        actual = sut.find_recurrences(netflixes + other)

        assert actual == expect

    def test_should_add_to_cache_each_run(self):
        # WHEN: Calculating similarities on first items
        sut = RecurringCalculator()
        sut.find_recurrences([FakeComparable("Netflix"), FakeComparable("netflix")])

        # THEN: It should add the string representations of those to the cache
        assert "Netflix" in sut.similarity_cache
        assert "netflix" in sut.similarity_cache
        # "Other" is not added yet, and shouldn't be present.
        assert "Other" not in sut.similarity_cache

        # WHEN: Calculating similarities again on other items
        sut.find_recurrences([FakeComparable("Other")])

        # THEN: The cache should contain both the new and the previous items
        assert "Netflix" in sut.similarity_cache
        assert "netflix" in sut.similarity_cache
        assert "Other" in sut.similarity_cache
