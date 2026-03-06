# antlr-adaptive

Learned parse-quality scoring and guided backtracking for any ANTLR4 grammar.

Works by hooking into ANTLR4's `adaptivePredict` — the single point where all grammar ambiguities are resolved. No grammar changes required.

## Three parsers

| Parser | Training | Description |
|---|---|---|
| `QualityParser` | self-trains | Observe-only; learns a quality score per parse from a perceptron. Valid inputs score higher than broken ones after a few epochs. |
| `BeamParser` | needs weights | Uses trained weights to identify suspect decisions and tries model-preferred alternatives. |
| `RetryParser` | none | Pure backtracking: on failure, scans the parse trace from the end and retries with untried alternatives until clean or exhausted. |

## Usage

```python
import sys
sys.path.insert(0, "generated")   # path to ANTLR-generated files

from SQLiteLexer import SQLiteLexer
from SQLiteParser import SQLiteParser
from antlr_adaptive import QualityParser, BeamParser, RetryParser, WeightStore

# --- Quality scoring + training ---
store = WeightStore()
store.load("weights.json")

qp = QualityParser(SQLiteLexer, SQLiteParser, store=store)
result = qp.parse("SELECT * FROM users;")
print(result.ok, result.score)     # True, +n.nnn

qp.train(my_sql_corpus, epochs=10)
store.save("weights.json")

# --- Beam search (needs trained weights) ---
bp = BeamParser(SQLiteLexer, SQLiteParser, store, beam_width=4)
result = bp.parse("SELECT * FROM t WHERE;")

# --- Retry / backtracking (no training needed) ---
rp = RetryParser(SQLiteLexer, SQLiteParser, max_retries=20)
result = rp.parse("SELECT * FROM t WHERE;")
print(result.n_errors, result.tokens_consumed)
```

`ParseResult` fields: `ok`, `n_errors`, `errors`, `tokens_consumed`, `score`, `n_decisions`, `trace`.

## Setup

```bash
# 1. Install
uv sync

# 2. Generate lexer/parser from a grammar (needs Java + ANTLR JAR)
~/.jdk/jdk-21.0.10+7/bin/java -jar jars/antlr4.jar \
    -Dlanguage=Python3 -visitor -o generated \
    grammars/SQLiteLexer.g4 grammars/SQLiteParser.g4

# 3. Run the SQLite demo
uv run python examples/sqlite_demo.py all

# 4. Run tests
uv run pytest tests/ -v
```

## How it works

ANTLR resolves grammar ambiguities through `ParserATNSimulator.adaptivePredict`. This library subclasses that simulator:

- **`ObservingATNSimulator`** — records every `(decision, alt, features)` without changing the parse. Safe for training.
- **`ForcedATNSimulator`** — overrides specific decisions with chosen alternatives. Used for retries.

**Feature vector** (694 dims): one-hot decision index + one-hot LA(1/2/3) token types + invoking state mod 64.

**Weight update**: perceptron rule `w += lr * reward * features`, clipped to `[-3, +3]`. Reward is `+1` for clean parses, `-n_errors / total_tokens` for failures.

## Applying to other grammars

Pass any ANTLR4-generated `lexer_class` and `parser_class`:

```python
from antlr_adaptive import QualityParser
from MyLexer import MyLexer
from MyParser import MyParser

qp = QualityParser(MyLexer, MyParser, start_rule="compilationUnit")
```

Tune `N_DECISIONS` in `antlr_adaptive/_features.py` to cover your grammar's decision count (`len(parser.atn.decisionToState)`).
