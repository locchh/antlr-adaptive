"""Shared result type for all three parsers."""

from dataclasses import dataclass, field


@dataclass
class ParseResult:
    """
    Result of a single parse attempt (possibly with forced decisions).

    forced          : {decision_index: alt} overrides applied, or {} for baseline
    errors          : list of {"line", "col", "msg"} from the error listener
    tokens_consumed : visible (non-hidden-channel) tokens consumed
    score           : mean weight score over all decisions (0.0 if no weights)
    n_decisions     : number of adaptivePredict calls made
    trace           : raw (decision, chosen, antlr_alt, features) — omitted from repr
    """

    forced: dict
    errors: list
    tokens_consumed: int
    score: float
    n_decisions: int
    trace: list = field(default_factory=list, repr=False)

    @property
    def n_errors(self) -> int:
        return len(self.errors)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def is_better_than(self, other: "ParseResult") -> bool:
        """
        Ranking: fewer errors > more tokens consumed > higher score.
        """
        if self.n_errors != other.n_errors:
            return self.n_errors < other.n_errors
        if self.tokens_consumed != other.tokens_consumed:
            return self.tokens_consumed > other.tokens_consumed
        return self.score > other.score
