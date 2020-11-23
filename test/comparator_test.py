import pytest

from analysis.comparator import TrigramSimilarity
from receiver.transactions import Comparable


class TestTrigramSimilarity:
    sut = TrigramSimilarity()

    def test_should_only_match_itself_on_single_identical(self):
        present = FakeComparable("Netflix")
        full_list = [present]

        expect = [present]
        actual = self.sut.compare(present, full_list)
        assert actual == expect

    def test_should_match_on_two_identical(self):
        present = FakeComparable("Netflix")
        full_list = [present, FakeComparable("Netflix")]

        expect = full_list
        actual = self.sut.compare(present, full_list)
        assert actual == expect

    def test_should_match_case_insensitive(self):
        present = FakeComparable("Netflix")
        full_list = [present, FakeComparable("netflix"), FakeComparable("NETFLIX")]

        expect = full_list
        actual = self.sut.compare(present, full_list)
        assert actual == expect

    def test_should_match_similar(self):
        present = FakeComparable("Netflix")
        full_list = [
            present,
            FakeComparable("netfix"),
            FakeComparable("netflix A/S"),
            FakeComparable("netflix Aps."),
        ]

        expect = full_list
        actual = self.sut.compare(present, full_list)
        assert actual == expect

    def test_should_not_match_similar_but_not_close_enough(self):
        present = FakeComparable("Netflix")
        full_list = [
            present,
            FakeComparable("notfix"),
        ]

        expect = [present]
        actual = self.sut.compare(present, full_list)
        assert actual == expect

    def test_should_raise_on_empty_present(self):
        present = FakeComparable("")
        full_list = [
            present,
            FakeComparable("hello"),
        ]

        with pytest.raises(ValueError) as e_info:
            self.sut.compare(present, full_list)
        assert (
            str(e_info.value)
            == "<FakeComparable: ''>.comparandum() cannot be an empty string."
        )

    def test_should_raise_on_empty_other(self):
        present = FakeComparable("hello")
        full_list = [
            present,
            FakeComparable(""),
        ]

        with pytest.raises(ValueError) as e_info:
            self.sut.compare(present, full_list)
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
