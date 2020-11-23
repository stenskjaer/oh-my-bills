from receiver.receiver import LsbReceiver


class TestLsbReceiver:
    def test_decode(self):
        sut = LsbReceiver("./data/export.csv")
        sut.decode()
