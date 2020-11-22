from typing import List

from receiver.transactions import Transaction


class TestTransaction:
    sut = Transaction("description")

    def test_normalization(self):
        expect = "description"
        assert self.sut.normalized_description == expect

    def test_repr(self):
        expect = "<Transaction: 'description'>"
        assert self.sut.__repr__() == expect

    def test_comparandum(self):
        expect = "description"
        assert self.sut.comparandum() == expect
