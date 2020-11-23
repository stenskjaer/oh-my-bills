import csv
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TextIO, IO, List

from dateutil import parser as dateutil_parser

from receiver.transactions import Transaction


class CsvDecoder(ABC):
    @abstractmethod
    def decode(self) -> List[Transaction]:
        pass


class IOReader(ABC):
    @abstractmethod
    def read(self, filepath: str) -> IO:
        pass


class CsvFileReader(IOReader):
    def read(self, filepath: str) -> TextIO:
        return open(filepath, newline="", encoding="UTF-8")


class LsbReceiver(CsvDecoder):
    def __init__(self, filepath: str, reader: IOReader = CsvFileReader()):
        self.filepath = filepath
        self.reader = reader

    def decode(self) -> List[Transaction]:
        with self.reader.read(self.filepath) as csv_file:
            transactions: List[Transaction] = []
            for row in csv.reader(csv_file, delimiter=";"):
                date = self.to_datetime(row[1])
                description = row[2]
                amount = self.to_float(row[3])
                transactions.append(Transaction(description, date, amount))
            return transactions

    @staticmethod
    def to_datetime(value: str) -> datetime:
        return dateutil_parser.parse(value, dayfirst=True)

    @staticmethod
    def to_float(value: str) -> float:
        return float(value.replace(",", "."))
