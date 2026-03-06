"""Beam-search parser: re-parse with model-preferred alternatives."""

from antlr4 import CommonTokenStream, InputStream

from ._features import extract_features
from ._simulator import FeedbackErrorListener, ForcedATNSimulator
from .types import ParseResult
from .weights import WeightStore


class BeamParser:
    """
    Grammar-agnostic beam-search parser.

    Requires a trained WeightStore.  On each parse:
      1. Run baseline (ANTLR's choice).
      2. If errors, find decisions where the model prefers a different alt.
      3. Re-parse with each top-K override forced.
      4. Return the best result (fewest errors, then highest score).

    Parameters
    ----------
    lexer_class  : generated Lexer class
    parser_class : generated Parser class
    store        : trained WeightStore
    start_rule   : top-level rule name (default "parse")
    beam_width   : max number of forced re-parses to try (default 4)
    """

    def __init__(self, lexer_class, parser_class, store: WeightStore,
                 start_rule: str = "parse", beam_width: int = 4):
        self.lexer_class = lexer_class
        self.parser_class = parser_class
        self.store = store
        self.start_rule = start_rule
        self.beam_width = beam_width

    # -- helpers --------------------------------------------------------

    def _run(self, text: str, forced: dict) -> ParseResult:
        stream = InputStream(text)
        lexer = self.lexer_class(stream)
        lexer.removeErrorListeners()

        tokens = CommonTokenStream(lexer)
        parser = self.parser_class(tokens)
        parser.removeErrorListeners()

        el = FeedbackErrorListener()
        parser.addErrorListener(el)

        sim = ForcedATNSimulator(
            parser, parser.atn,
            parser.decisionsToDFA, parser.sharedContextCache,
            forced=forced, store=self.store,
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

        n = len(sim.trace)
        score = 0.0
        if n > 0:
            score = sum(
                self.store.score(d, a, f)
                for d, a, _, f in sim.trace
            ) / n

        return ParseResult(
            forced=forced,
            errors=el.errors,
            tokens_consumed=consumed,
            score=score,
            n_decisions=n,
            trace=sim.trace,
        )

    def _candidate_overrides(self, baseline: ParseResult) -> list[dict]:
        """
        Scan baseline trace for decisions where the model prefers a
        different alternative.  Return up to beam_width override dicts,
        sorted by confidence margin (highest first).
        """
        # build a throw-away parser just to access ATN alt counts
        _tokens = CommonTokenStream(self.lexer_class(InputStream(" ")))
        atn = self.parser_class(_tokens).atn

        suspects: list[tuple[float, int, int]] = []

        for decision, chosen, antlr_alt, features in baseline.trace:
            n_alts = len(atn.decisionToState[decision].transitions)
            scores = {
                alt: self.store.score(decision, alt, features)
                for alt in range(1, n_alts + 1)
            }
            best_alt = max(scores, key=lambda a: scores[a])
            if best_alt != antlr_alt:
                margin = scores[best_alt] - scores.get(antlr_alt, 0.0)
                if margin > 0:
                    suspects.append((margin, decision, best_alt))

        suspects.sort(reverse=True)

        return [{decision: best_alt}
                for _, decision, best_alt in suspects[:self.beam_width]]

    # -- public API -----------------------------------------------------

    def parse(self, text: str, verbose: bool = False) -> ParseResult:
        """
        Parse text using beam search.  Returns best ParseResult found.
        """
        baseline = self._run(text, forced={})

        if verbose:
            tag = "OK  " if baseline.ok else "FAIL"
            print(f"  [beam 0 / baseline]  {tag}  "
                  f"score={baseline.score:+.3f}  "
                  f"decisions={baseline.n_decisions}  "
                  f"errors={baseline.n_errors}")
            for e in baseline.errors[:1]:
                print(f"    -> {e['line']}:{e['col']} {e['msg']}")

        if baseline.ok:
            return baseline

        candidates = self._candidate_overrides(baseline)

        if not candidates:
            return baseline

        beams: list[ParseResult] = [baseline]

        for i, forced in enumerate(candidates, 1):
            beam = self._run(text, forced=forced)
            beams.append(beam)

            if verbose:
                tag = "OK  " if beam.ok else "FAIL"
                dec, alt = next(iter(forced.items()))
                improved = " [better]" if beam.is_better_than(baseline) else ""
                print(f"  [beam {i}]  {tag}  "
                      f"score={beam.score:+.3f}  "
                      f"errors={beam.n_errors}  "
                      f"forced={{dec={dec}, alt={alt}}}{improved}")

        best = min(beams, key=lambda b: (b.n_errors, -b.score))

        if verbose:
            print(f"  -> best: beam {beams.index(best)}  "
                  f"errors={best.n_errors}  score={best.score:+.3f}")

        return best
