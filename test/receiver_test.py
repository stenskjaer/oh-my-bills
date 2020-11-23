from datetime import datetime
from pathlib import Path
from typing import List

from dateutil import parser

from receiver.receiver import LsbReceiver, CsvFileReader, IOReader
from receiver.transactions import Transaction

resource_dir = Path(__file__).parent / "resources"


class TestCsvFileReader:
    sut = CsvFileReader()

    def test_valid_csv(self):
        file_path = resource_dir / "default.csv"

        expect = self.read_local_file(file_path)
        actual = self.sut.read(file_path)
        assert actual == expect

    @staticmethod
    def read_local_file(path: str) -> List[str]:
        with open(path) as fh:
            return fh.read().splitlines()


class TestLsbReceiver:
    def test_should_decode_valid(self):
        file_content = [
            '"19-11-2020";"19-11-2020";"Entry 1";"269,00";"5.423,67"',
            '"18-11-2020";"18-11-2020";"Entry 2";"-200,00";"5.223,67"',
            '"16-11-2020";"16-11-2020";"Entry 3";"150,00";"5.373,67"',
        ]

        sut = LsbReceiver("dummy-path", FakeCsvReader(file_content))
        actual = sut.decode()
        expect = [
            Transaction("Entry 1", datetime(2020, 11, 19, 0, 0, 0, 0), 269.00),
            Transaction("Entry 2", datetime(2020, 11, 18, 0, 0, 0, 0), -200.00),
            Transaction("Entry 3", datetime(2020, 11, 16, 0, 0, 0, 0), 150.00),
        ]

        assert actual == expect

    def test_should_decode_high_amount_correctly(self):
        file_content = [
            '"19-11-2020";"19-11-2020";"Entry 1";"5.269,00";"5.423,67"',
        ]

        sut = LsbReceiver("dummy-path", FakeCsvReader(file_content))
        actual = sut.decode()
        expect = [
            Transaction("Entry 1", datetime(2020, 11, 19, 0, 0, 0, 0), 5269.00),
        ]

        assert actual == expect

    def test_should_skip_invalid_empty_field_with_warning(self):
        file_content = [
            '"19-11-2020";"19-11-2020";"Entry 1";"";"5.423,67"',
        ]

        sut = LsbReceiver("dummy-path", FakeCsvReader(file_content))
        actual = sut.decode()
        expect = []
        assert actual == expect

    def test_should_skip_invalid_incomplete_line_with_warning(self):
        file_content = [
            '"19-11-2020";"19-11-2020";"Entr',
        ]

        sut = LsbReceiver("dummy-path", FakeCsvReader(file_content))
        actual = sut.decode()
        expect = []
        assert actual == expect


class FakeCsvReader(IOReader):
    def __init__(self, result: List[str]):
        self.result: List[str] = result

    def read(self, filepath: str) -> List[str]:
        return self.result
