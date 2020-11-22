from dateutil import parser

from receiver.transactions import Transaction


class TestTransaction:
    date = parser.parse("03-02-2020", dayfirst=True)
    sut = Transaction("description", date)

    def test_normalization(self):
        expect = "description"
        assert self.sut.normalized_description == expect

    def test_repr(self):
        expect = "<Transaction: 'description'>"
        assert self.sut.__repr__() == expect

    def test_comparandum(self):
        expect = "description"
        assert self.sut.comparandum() == expect

    def test_date(self):
        expect = self.date
        actual = self.sut.date()
        assert actual == expect
