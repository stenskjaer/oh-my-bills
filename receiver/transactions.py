from abc import ABC, abstractmethod
from datetime import datetime


class Comparable(ABC):
    @abstractmethod
    def comparandum(self) -> str:
        pass


class Datable(ABC):
    @abstractmethod
    def date(self) -> datetime:
        pass


class Transaction(Comparable, Datable):
    """Transaction represents a single transaction from a bank statement."""

    def __init__(
        self,
        description: str,
        date: datetime,
        amount: float = 0.0,
    ) -> None:
        self.amount = amount
        self.datetime = date
        self.description = description
        self.normalized_description = self.normalize(description)

    def __repr__(self) -> str:
        return f"<Transaction: '{self.normalized_description}'>"

    def comparandum(self) -> str:
        """Returns a representation of the transaction for identifying similar
        transactions."""
        return self.description

    def date(self) -> datetime:
        return self.datetime

    @staticmethod
    def normalize(description: str) -> str:
        return description
