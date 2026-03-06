"""Backtracking retry parser — no training required."""

from antlr4 import CommonTokenStream, InputStream

from ._simulator import FeedbackErrorListener, ForcedATNSimulator
from .types import ParseResult
from .weights import WeightStore


class RetryParser:
    """
    Grammar-agnostic backtracking parser.  No training required.

    Algorithm:
      1. Baseline parse (ANTLR's choice) → record trace.
      2. If errors: scan trace from the end for a decision with an
         untried alternative.
      3. Re-parse with that decision forced to the next candidate alt.
      4. Keep the best result (fewest errors > most tokens > score).
      5. Advance the "frontier" to whichever attempt went deepest.
      6. Repeat up to max_retries times or until a clean parse is found.

    If a WeightStore is provided its scores are used to order the
    candidate alternatives (best-first), reducing retries needed.

    Parameters
    ----------
    lexer_class  : generated Lexer class
    parser_class : generated Parser class
    start_rule   : top-level rule name (default "parse")
    store        : optional WeightStore for smarter alt ordering
    max_retries  : maximum forced re-parses (default 20)
    """

    def __init__(self, lexer_class, parser_class,
                 start_rule: str = "parse",
                 store: WeightStore | None = None,
                 max_retries: int = 20):
        self.lexer_class = lexer_class
        self.parser_class = parser_class
        self.start_rule = start_rule
        self.store = store
        self.max_retries = max_retries

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

        score = 0.0
        if self.store and sim.trace:
            score = sum(
                self.store.score(d, a, f)
                for d, a, _, f in sim.trace
            ) / len(sim.trace)

        return ParseResult(
            forced=forced,
            errors=el.errors,
            tokens_consumed=consumed,
            score=score,
            n_decisions=len(sim.trace),
            trace=sim.trace,
        )

    def _ranked_alts(self, decision: int, features: list,
                     n_alts: int, exclude: set) -> list[int]:
        """Return untried alts sorted by weight score (desc). Fallback: numeric."""
        alts = [a for a in range(1, n_alts + 1) if a not in exclude]
        if self.store:
            alts.sort(
                key=lambda a: self.store.score(decision, a, features),
                reverse=True,
            )
        return alts

    # -- public API -----------------------------------------------------

    def parse(self, text: str, verbose: bool = False) -> ParseResult:
        """
        Parse text with backtracking retry.  Returns best ParseResult found.
        """
        # build a throw-away parser once to get ATN alt counts
        _tokens = CommonTokenStream(self.lexer_class(InputStream(" ")))
        atn = self.parser_class(_tokens).atn

        # tried[decision] = set of alts already attempted
        tried: dict[int, set] = {}

        baseline = self._run(text, forced={})
        best = baseline
        frontier = baseline   # deepest-reaching attempt seen so far
        retries = 0

        if verbose:
            self._print(baseline, label="baseline", atn=atn)

        if baseline.ok:
            return best

        for _ in range(self.max_retries):
            override = None

            for decision, chosen, antlr_alt, features in reversed(frontier.trace):
                n_alts = len(atn.decisionToState[decision].transitions)
                if n_alts <= 1:
                    continue

                seen = tried.get(decision, {antlr_alt})
                candidates = self._ranked_alts(decision, features, n_alts, seen)

                if candidates:
                    next_alt = candidates[0]
                    tried.setdefault(decision, {antlr_alt}).add(next_alt)
                    override = {decision: next_alt}
                    break

            if override is None:
                break  # exhausted all candidates

            attempt = self._run(text, forced=override)
            retries += 1

            if verbose:
                self._print(attempt, label=f"retry {retries}", atn=atn,
                            forced=override, ref=best)

            if attempt.is_better_than(best):
                best = attempt

            if attempt.tokens_consumed >= frontier.tokens_consumed:
                frontier = attempt

            if best.ok:
                break

        if verbose:
            tag = "SOLVED" if best.ok else f"best={best.n_errors} error(s)"
            print(f"  -> {tag}  retries={retries}  score={best.score:+.3f}")

        return best

    def _print(self, r: ParseResult, label: str, atn,
               forced: dict = None, ref: ParseResult = None):
        tag = "OK  " if r.ok else "FAIL"
        forced_str = ""
        if forced:
            dec, alt = next(iter(forced.items()))
            n_alts = len(atn.decisionToState[dec].transitions)
            forced_str = f"  forced={{dec={dec}, alt={alt}/{n_alts}}}"
        better = "  [better]" if ref and r.is_better_than(ref) else ""
        score_str = f"  score={r.score:+.3f}" if self.store else ""
        print(f"  [{label:12s}]  {tag}  errors={r.n_errors}"
              f"  tok={r.tokens_consumed}{score_str}{forced_str}{better}")
        for e in r.errors[:1]:
            print(f"    -> {e['line']}:{e['col']} {e['msg'][:60]}")
