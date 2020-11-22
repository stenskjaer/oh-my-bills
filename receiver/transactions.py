from abc import ABC, abstractmethod


class Comparable(ABC):
    @abstractmethod
    def comparandum(self) -> str:
        pass


class Transaction(Comparable):
    """Transaction represents a single transaction from a bank statement."""

    def __init__(
        self,
        description: str,
        amount=0,
        date="",
    ) -> None:
        self.amount = amount
        self.date = date
        self.description = description
        self.normalized_description = self.normalize(description)

    def __repr__(self) -> str:
        return f"<Transaction: '{self.normalized_description}'>"

    def comparandum(self) -> str:
        """Returns a representation of the transaction for identifying similar
        transactions."""
        return self.description

    @staticmethod
    def normalize(description: str) -> str:
        return description
