from analysis.recurrences import RecurringCalculator


class TestRecurringCalculator:
    descriptions = [
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

    def _test_find_similars(self):
        trans = []
        sut = RecurringCalculator()

        # assert self.similarity_cache == set(descriptions)
