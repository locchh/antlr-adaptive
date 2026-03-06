"""Grammar-agnostic quality-scoring parser with perceptron training."""

import sys

from antlr4 import CommonTokenStream, InputStream

from ._features import extract_features
from ._simulator import FeedbackErrorListener, ObservingATNSimulator
from .types import ParseResult
from .weights import WeightStore


class QualityParser:
    """
    Observe-and-learn parser.  Works with any ANTLR4-generated grammar.

    Parameters
    ----------
    lexer_class   : generated Lexer class
    parser_class  : generated Parser class
    start_rule    : name of the top-level rule to call (default "parse")
    store         : WeightStore instance (created automatically if None)
    """

    def __init__(self, lexer_class, parser_class,
                 start_rule: str = "parse", store: WeightStore | None = None):
        self.lexer_class = lexer_class
        self.parser_class = parser_class
        self.start_rule = start_rule
        self.store = store or WeightStore()

    # -- internal -------------------------------------------------------

    def _run(self, text: str) -> tuple:
        """
        Parse text.  Returns (errors, sim, tokens_consumed).
        """
        stream = InputStream(text)
        lexer = self.lexer_class(stream)
        lexer.removeErrorListeners()

        tokens = CommonTokenStream(lexer)
        parser = self.parser_class(tokens)
        parser.removeErrorListeners()

        el = FeedbackErrorListener()
        parser.addErrorListener(el)

        sim = ObservingATNSimulator(
            parser, parser.atn,
            parser.decisionsToDFA, parser.sharedContextCache,
        )
        parser._interp = sim

        try:
            getattr(parser, self.start_rule)()
        except Exception:
            pass

        tokens.fill()
        consumed = sum(
            1 for tok in tokens.tokens
            if tok.type != -1 and tok.channel == 0
        )
        return el.errors, sim, consumed

    # -- public API -----------------------------------------------------

    def parse(self, text: str) -> ParseResult:
        """Parse without learning; return quality-scored ParseResult."""
        errors, sim, consumed = self._run(text)

        score = 0.0
        if sim.trace:
            score = sum(
                self.store.score(d, a, f) for d, a, f in sim.trace
            ) / len(sim.trace)

        return ParseResult(
            forced={},
            errors=errors,
            tokens_consumed=consumed,
            score=score,
            n_decisions=len(sim.trace),
            trace=sim.trace,
        )

    def learn(self, text: str, verbose: bool = False) -> ParseResult:
        """
        Parse and update weights via perceptron.

        Reward:  +1.0 if no errors, else -n_errors / total_tokens.
        """
        errors, sim, consumed = self._run(text)

        total_tokens = max(consumed, 1)
        reward = 1.0 if not errors else -float(len(errors)) / total_tokens

        for decision, alt, features in sim.trace:
            self.store.update(decision, alt, features, reward)

        score = 0.0
        if sim.trace:
            score = sum(
                self.store.score(d, a, f) for d, a, f in sim.trace
            ) / len(sim.trace)

        result = ParseResult(
            forced={},
            errors=errors,
            tokens_consumed=consumed,
            score=score,
            n_decisions=len(sim.trace),
            trace=sim.trace,
        )

        if verbose:
            tag = "OK  " if result.ok else "FAIL"
            print(f"  {tag}  q={score:+.3f}  reward={reward:+.3f}  | {text[:55]}")
            for e in errors[:1]:
                print(f"       -> {e['line']}:{e['col']} {e['msg']}")

        return result

    def train(self, texts: list[str], epochs: int = 1, verbose: bool = False):
        """
        Train the weight store on a list of text samples.

        verbose=True prints a one-liner per sample per epoch.
        """
        for epoch in range(epochs):
            if verbose:
                print(f"\n  epoch {self.store.epochs + 1}")
            for text in texts:
                self.learn(text, verbose=verbose)
            self.store.epochs += 1
