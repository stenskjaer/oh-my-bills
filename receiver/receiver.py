import csv
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TextIO, IO, List

from dateutil import parser as dateutil_parser

from receiver.transactions import Transaction


import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug("often makes a very good meal of %s", "visiting tourists")


class CsvDecoder(ABC):
    @abstractmethod
    def decode(self) -> List[Transaction]:
        pass


class IOReader(ABC):
    @abstractmethod
    def read(self, filepath: str) -> IO:
        pass


class CsvFileReader(IOReader):
    def read(self, filepath: str) -> List[str]:
        with open(filepath, newline="", encoding="UTF-8") as fh:
            content = fh.read()
            return content.splitlines()


class LsbReceiver(CsvDecoder):
    def __init__(self, filepath: str, reader: IOReader = CsvFileReader()):
        self.filepath = filepath
        self.reader = reader

    def decode(self) -> List[Transaction]:
        csv_lines = self.reader.read(self.filepath)

        transactions: List[Transaction] = []
        for row in csv.reader(csv_lines, delimiter=";"):
            if self.validate(row):
                date = self.to_datetime(row[1])
                description = row[2]
                amount = self.to_float(row[3])
                transactions.append(Transaction(description, date, amount))
        return transactions

    def validate(self, row: List[str]) -> bool:
        try:
            self.not_empty(row[1], "date")
            self.not_empty(row[2], "description")
            self.not_empty(row[3], "amount")
            return True
        except (ValueError, IndexError) as e:
            logger.warning(
                f"The row {row} resulted in the following validation error: "
                f"{e}. The row is ignored."
            )
            return False

    @staticmethod
    def not_empty(input: object, name: str) -> None:
        if not input:
            raise ValueError(f"Field {name} was empty.")

    def to_datetime(self, value: str) -> datetime:
        return dateutil_parser.parse(value, dayfirst=True)

    def to_float(self, value: str) -> float:
        return float(value.replace(".", "").replace(",", "."))
