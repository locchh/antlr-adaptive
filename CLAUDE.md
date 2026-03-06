# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- Python 3.12 via `uv`, venv at `.venv/`
- JDK at `~/.jdk/jdk-21.0.10+7/bin/java` (no system Java)
- ANTLR4 JAR at `jars/antlr4.jar` (v4.13.2)

## Commands

```bash
# Run the SQLite demo (quality training + beam + retry)
uv run python examples/sqlite_demo.py [quality|beam|retry|all]

# Run tests
uv run pytest tests/ -v

# Regenerate Python lexer+parser from a grammar
~/.jdk/jdk-21.0.10+7/bin/java -jar jars/antlr4.jar \
  -Dlanguage=Python3 -visitor -o generated <Grammar>.g4

# For split grammars (lexer + parser separate files):
~/.jdk/jdk-21.0.10+7/bin/java -jar jars/antlr4.jar \
  -Dlanguage=Python3 -visitor -o generated grammars/SQLiteLexer.g4 grammars/SQLiteParser.g4

# Install dependencies
uv add <package>
```

## Architecture

`antlr_adaptive` is a grammar-agnostic library for learned parse-quality scoring and guided backtracking on top of any ANTLR4-generated parser.

### Package layout

```
antlr_adaptive/
  __init__.py       public API: QualityParser, BeamParser, RetryParser, WeightStore, ParseResult
  _features.py      feature extraction (decision one-hot + LA(1/2/3) token types + invoking state)
  _simulator.py     ObservingATNSimulator, ForcedATNSimulator, FeedbackErrorListener
  weights.py        WeightStore — perceptron update + save/load
  types.py          ParseResult dataclass
  quality.py        QualityParser — observe, learn, train
  beam.py           BeamParser — model-guided re-parse with forced overrides
  retry.py          RetryParser — exhaustive backtracking retry (no training needed)
examples/
  sqlite_demo.py    end-to-end demo using the SQLite grammar
tests/
  test_parsers.py   pytest tests for all three parsers
grammars/           source .g4 files (SQLiteLexer, SQLiteParser, arithmetic)
generated/          ANTLR-generated Python files (do not edit)
weights.json        persisted weight store (epochs + weight vectors)
```

### Three-parser design

All parsers take `lexer_class`, `parser_class`, `start_rule` — they work with **any** ANTLR4 grammar, not just SQLite.

| Parser | Needs training | How it works |
|---|---|---|
| `QualityParser` | trains itself | Observe-only; perceptron update after each parse; quality score = mean weight·feature over trace |
| `BeamParser` | yes (pre-trained) | Baseline parse → find high-confidence model overrides → re-parse top-K, pick best |
| `RetryParser` | no | Baseline → scan trace from end for untried alts → forced re-parse → repeat up to max_retries |

### Key internals

- **`ObservingATNSimulator`** — subclasses `ParserATNSimulator`, overrides `adaptivePredict()`. Always returns ANTLR's choice; records `(decision, alt, features)` trace. Safe to use mid-parse.
- **`ForcedATNSimulator`** — same, but overrides specific decisions with pre-chosen alts. Used by `BeamParser` and `RetryParser`.
- **`WeightStore`** — `(decision, alt)` → float vector of `FEATURE_DIM=694`. Perceptron update with `LEARNING_RATE=0.05`, clipped to `[-3.0, +3.0]`.

**Feature vector** (694 dims total):
- One-hot decision index (dims 0–269, covers SQLite's 263 decisions)
- One-hot LA(1), LA(2), LA(3) token types (dims 270–629)
- Invoking state mod 64 (dims 630–693)

### Key constraints and gotchas

- `ParserATNSimulator` must be imported from `antlr4` directly, not `antlr4.ParserATNSimulator`
- `decisionsToDFA` is the attribute on the generated parser; `decisionToDFA` is what `ParserATNSimulator.__init__` stores
- Call `tokens.fill()` before iterating `tokens.tokens`
- ATN decision count for SQLite is 263; N_DECISIONS=270 gives headroom
- Alt count per decision: `len(atn.decisionToState[decision].transitions)`
- Overriding `adaptivePredict` to steer a live parse causes cascading ATN failures — quality scoring is safe because it never changes the parse
