# Teaching a Parser to Learn from Its Mistakes

Parsers are deterministic. Given the same input, they always make the same decisions — and when a grammar is ambiguous, they always pick the same alternative, right or wrong. What if we could teach a parser to *prefer* better alternatives, or at least recover from bad ones?

That is the question behind **antlr-adaptive**: a small library that wraps any ANTLR4-generated parser with learned quality scoring and guided backtracking.

---

## The Problem

ANTLR4 is one of the most widely used parser generators. It takes a grammar file and produces a lexer and parser in your target language. At the core of every generated parser is a method called `adaptivePredict` — the single point where all grammar ambiguities are resolved. ANTLR computes the best alternative using its ATN (Augmented Transition Network) and returns it. The parser follows it. End of story.

The trouble is that "best" means *syntactically consistent with the grammar*, not *closest to what the user meant*. For broken or near-broken inputs, ANTLR's choice can cascade into a chain of errors that makes recovery harder than it needs to be.

Classic error recovery strategies (panic mode, phrase-level recovery) are built into ANTLR's runtime. They work well for many cases. But they are grammar-specific, manually tuned, and blind to the history of what has worked before.

**Can we do better by learning from examples?**

---

## The Idea

ANTLR resolves ambiguities at *decision points*. Each decision has a small number of alternatives (typically 2–22 for real grammars). At every decision, the parser is in a specific state: it knows which tokens are coming next and which rule invoked this decision.

That state is learnable.

We represent it as a fixed-length feature vector:
- **One-hot decision index** — which of the grammar's decisions are we at?
- **One-hot lookahead tokens** — what are the next 1, 2, 3 tokens?
- **Invoking state mod 64** — a coarse encoding of calling context.

For the SQLite grammar (263 decisions), this gives a 694-dimensional vector. Then we apply a simple **perceptron**:

```
weight[decision][alt] · features  →  quality score
```

After each parse:
- If it succeeded: reward `+1.0` — reinforce every decision made.
- If it failed: reward `-n_errors / total_tokens` — penalise every decision made.

Over many examples, weights for decisions that lead to clean parses grow positive; weights for decisions that lead to errors shrink.

The key insight: **we never override the parser during a parse**. Overriding `adaptivePredict` mid-parse breaks the ATN state machine — one wrong turn and every subsequent decision is operating on a corrupted state. Instead, we *observe only*, then use the learned weights to evaluate or reorder alternatives in separate re-parse attempts.

---

## Three Parsers

### QualityParser — learn by watching

`QualityParser` subclasses ANTLR's simulator with an `ObservingATNSimulator` that records every `(decision, alt, features)` tuple without changing the result. After each parse it updates the weight store with the perceptron rule.

After training, it can assign a **quality score** to any parse: the mean `weight[decision][alt] · features` over all decisions in the trace. Valid inputs consistently score higher than broken ones.

```python
qp = QualityParser(SQLiteLexer, SQLiteParser, store=store)
qp.train(corpus, epochs=10)

result = qp.parse("SELECT * FROM users;")
print(result.score)   # e.g. +10.3

result = qp.parse("SELECT FROM;")
print(result.score)   # e.g. +8.1
```

This is useful for **ranking multiple parse candidates**, detecting suspicious inputs, or as a signal in a larger pipeline.

### BeamParser — model-guided re-parse

Once the weight store is trained, `BeamParser` uses it to *actively improve* parse results on broken inputs.

Algorithm:
1. Run baseline (ANTLR's normal parse), record trace.
2. For each decision in the trace, check if the model prefers a different alternative (margin > 0).
3. Collect the top-K such decisions, sorted by confidence margin.
4. Re-parse with each override forced.
5. Return the result with fewest errors (tie-broken by score).

```python
bp = BeamParser(SQLiteLexer, SQLiteParser, store, beam_width=4)
result = bp.parse("SELECT id name FROM users;")
```

`BeamParser` is fast (at most `beam_width + 1` parses) and targets the decisions the model is *most confident about*. It works best when the training corpus is representative of the input distribution.

### RetryParser — exhaustive backtracking without training

`RetryParser` does not need a weight store at all. It treats the parse trace as a search space and backtracks through it:

1. Baseline parse → record trace.
2. Scan the trace **from the end** (deepest decisions first) for a decision with an untried alternative.
3. Re-parse with that decision forced.
4. Track the "frontier" — the attempt that consumed the most tokens.
5. Repeat from step 2 using the frontier's trace. Stop when clean or `max_retries` reached.

Scanning from the end is the key detail. The early decisions in a parse (e.g., which statement type) have many downstream dependencies. Trying alternatives there first cascades into many failures. Starting from the end targets local decisions that are more likely to be independently fixable.

```python
rp = RetryParser(SQLiteLexer, SQLiteParser, max_retries=20)
result = rp.parse("SELECT * FROM t WHERE id = AND name = 'x';")
```

If weights are available, they are used to order the candidate alternatives — reducing the number of retries needed.

---

## How Each Parser Compares

| | QualityParser | BeamParser | RetryParser |
|---|---|---|---|
| Training required | yes (self-trains) | yes (pre-trained) | no |
| Max re-parses | 1 | `beam_width` | `max_retries` |
| Modifies parse | never | forced overrides | forced overrides |
| Best for | scoring / ranking | fast guided repair | no-training repair |
| Limitation | scores only; doesn't fix | needs representative training data | exponential search space |

On the SQLite grammar with 8 genuinely broken queries (missing table names, missing WHERE clause bodies, etc.), none of the parsers produce zero errors — because no valid alternative combination in the grammar can parse `SELECT FROM;`. What improves is **how gracefully** the parser fails: more tokens consumed, fewer cascading errors, better partial structure.

The quality score separation after 10 epochs on 31 mixed queries:

```
avg score  valid=+10.34  broken=+8.12  sep=+2.22
```

The model reliably distinguishes clean parses from broken ones within a few epochs, without any manually written rules.

---

## Grammar-Agnostic by Design

Nothing in the library is SQLite-specific. The three parsers accept any ANTLR4-generated lexer and parser class:

```python
from antlr_adaptive import RetryParser
from MyLexer import MyLexer
from MyParser import MyParser

rp = RetryParser(MyLexer, MyParser, start_rule="compilationUnit")
result = rp.parse(source_code)
```

The only grammar-specific constant is `N_DECISIONS` in `_features.py`, which should be set to slightly above `len(parser.atn.decisionToState)` for your grammar. The SQLite value (270, covering 263 actual decisions) is the default; it works as-is for any grammar with fewer decisions.

This means you can apply the same approach to SQL dialects, programming languages, configuration formats, or domain-specific languages — any grammar where ANTLR4 can generate a Python parser.

---

## Testing

The test suite covers all three parsers against the SQLite grammar:

```bash
uv run pytest tests/ -v
```

Key checks:
- Valid SQL parses clean (`result.ok == True`) across all three parsers.
- Broken SQL returns a `ParseResult` (no crash; graceful degradation).
- `QualityParser` score separation: valid average > broken average after 3 training epochs.
- `WeightStore` save/load roundtrip preserves exact weight values.
- `ParseResult.is_better_than` ranking: fewer errors > more tokens consumed > higher score.

19 tests, all passing in under 0.2 seconds.

---

## More

Source code, examples, and grammar files:
**[github.com/locchh/antlr-adaptive](https://github.com/locchh/antlr-adaptive)**

The SQLite demo runs all three parsers end-to-end:

```bash
uv run python examples/sqlite_demo.py all
```
