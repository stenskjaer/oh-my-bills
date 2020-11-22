"""
1. Receive

Steps for identification algorithm:
2. Pre-process
3. NLP Comparison
4. Identifying recurring
5. Store result

Presenting data:
API
"""
from typing import List

from analysis.recurrences import RecurringCalculator
from receiver.transactions import Transaction

# Test data
descriptions = [
    "MobilePay køb DSB app",
    "MobilePay køb Hedensted Y's Mens Club",
    "Visa/Dankort MINI-MARKED 151, COOENHAGEN,",
    "Visa/Dankort AMZN Mktp DE*M72LO3VM4, AMAZON.DE,",
    "Visa/Dankort IZ *COFFICPH, COPENHAGEN,",
    "UDK STUDIEGÆLD",
    "UDK STUDIEGÆLD",
    "UDS STUDIEGÆLD",
    "Netflix",
    "netflix",
    "netfix",
    "flexnet",
    "fixnet",
    "NotFix",
    "Netflix A/S",
    "Netflix Aps.",
]

# Let's create some entries
transactions: List[Transaction] = []
for desc in descriptions:
    transactions.append(Transaction(desc))

calculator = RecurringCalculator(transactions)
var = calculator.similars
