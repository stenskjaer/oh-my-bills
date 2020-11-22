import pytest

from analysis.comparator import TrigramSimilarity
from receiver.transactions import Comparable


class TestTrigramSimilarity:
    sut = TrigramSimilarity()

    def test_should_match_on_identical(self):
        present = FakeComparable("Netflix")
        others = [FakeComparable("Netflix")]
        expect = [present] + others
        actual = self.sut.compare(present, others)
        assert actual == expect

    def test_should_match_case_insensitive(self):
        present = FakeComparable("Netflix")
        others = [FakeComparable("netflix"), FakeComparable("NETFLIX")]
        expect = [present] + others
        actual = self.sut.compare(present, others)
        assert actual == expect

    def test_should_match_similar(self):
        present = FakeComparable("Netflix")
        others = [
            FakeComparable("netfix"),
            FakeComparable("netflix A/S"),
            FakeComparable("netflix Aps."),
        ]
        expect = [present] + others
        actual = self.sut.compare(present, others)
        assert actual == expect

    def test_should_not_match_similar_but_not_close_enough(self):
        present = FakeComparable("Netflix")
        others = [
            FakeComparable("notfix"),
        ]
        expect = [present]
        actual = self.sut.compare(present, others)
        assert actual == expect

    def test_should_raise_on_empty_present(self):
        present = FakeComparable("")
        others = [
            FakeComparable("hello"),
        ]
        with pytest.raises(ValueError) as e_info:
            self.sut.compare(present, others)
        assert (
            str(e_info.value)
            == "<FakeComparable: ''>.comparandum() cannot be an empty string."
        )

    def test_should_raise_on_empty_other(self):
        present = FakeComparable("hello")
        others = [
            FakeComparable(""),
        ]
        with pytest.raises(ValueError) as e_info:
            self.sut.compare(present, others)
        assert (
            str(e_info.value)
            == "<FakeComparable: ''>.comparandum() cannot be an empty string."
        )


class FakeComparable(Comparable):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"<FakeComparable: '{self.value}'>"

    def comparandum(self) -> str:
        return self.value
