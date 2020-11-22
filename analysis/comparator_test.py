from analysis.comparator import TrigramSimilarity
from receiver.transactions import Comparable


class TestTrigramSimilarity:
    sut = TrigramSimilarity()

    def test_compare_on_identical(self):
        present = FakeComparable("Netflix")
        others = [FakeComparable("Netflix")]
        expect = [present] + others
        actual = self.sut.compare(present, others)
        assert actual == expect


class FakeComparable(Comparable):
    def __init__(self, value):
        self.value = value

    def comparandum(self) -> str:
        return self.value
