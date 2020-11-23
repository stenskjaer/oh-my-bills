from dateutil import parser

from receiver.transactions import Transaction


class TestTransaction:
    date = parser.parse("03-02-2020", dayfirst=True)
    amount = 10.0
    desc = "description"
    sut = Transaction(desc, date, amount)

    def test_normalization(self):
        expect = "description"
        assert self.sut.normalized_description == expect

    def test_repr(self):
        expect = "<Transaction: description='description', date=2020-02-03 00:00:00, amount=10.0>"
        assert self.sut.__repr__() == expect

    def test_comparandum(self):
        expect = "description"
        assert self.sut.comparandum() == expect

    def test_date(self):
        expect = self.date
        actual = self.sut.date()
        assert actual == expect

    def test_eq(self):
        other = Transaction(self.desc, self.date, self.amount)
        assert self.sut.__eq__(other)
