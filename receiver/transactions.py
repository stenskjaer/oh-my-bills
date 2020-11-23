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
    """Transaction represents a single transaction from a bank statement. They
    contain the date of the transaction, a description, and the amount transferred."""

    rules = [
        lambda x: x.lower(),
        lambda x: x.replace("visa/dankort", ""),
        lambda x: x.replace("dankort", ""),
        lambda x: x.replace("visa/mastercard", ""),
        lambda x: x.replace("mastercard", ""),
        lambda x: x.replace("mobilepay", ""),
        lambda x: " " + x.strip() + " ",
    ]

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
        return (
            f"<Transaction: description='{self.normalized_description}', "
            f"date={self.date()}, amount={self.amount}>"
        )

    def __eq__(self, other) -> bool:
        return (self.description, self.date(), self.amount) == (
            other.description,
            other.date(),
            other.amount,
        )

    def __hash__(self):
        return hash((self.description, str(self.date()), self.amount))

    def comparandum(self) -> str:
        """Returns a representation of the transaction for identifying similar
        transactions."""
        return self.normalized_description

    def date(self) -> datetime:
        return self.datetime

    def normalize(self, value: str) -> str:
        for rule in self.rules:
            value = rule(value)
        return value
