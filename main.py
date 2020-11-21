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
from typing import List, Dict, Set
from transactions import *

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

# Cache indicating whether this has one or more similar transactions.
# If that is the case, then recurrence has already been calculated for it and we don't have to do it again.
similarity_cache: Set[str] = set()

recurring_entries: List[Recurring]

# Let's create some entries
transactions: List[Transaction] = []
for desc in descriptions:
    transactions.append(Transaction(desc))


for trans in transactions:
    print("cache: ", similarity_cache)
    # Skip if already computed
    if trans.description in similarity_cache:
        print(f"'{trans.description}' in cache, skipping computation")
        continue
    similars = trans.find_similars(transactions)
    similar_desc = [t.description for t in similars]

    # recurring_confidence = calculate_recurring()
    # if (recurring_confidence > threshold):
    #    Recurring(similars + trans, confidence)
    print("adding to cache: ", similar_desc)
    similarity_cache.update(similar_desc)

assert similarity_cache == set(descriptions)
