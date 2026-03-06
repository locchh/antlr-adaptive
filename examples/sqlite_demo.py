"""
SQLite grammar demo for antlr_adaptive.

Shows all three parsers against a set of valid and broken SQL queries.

Usage
-----
    # from the repo root
    uv run python examples/sqlite_demo.py [quality|beam|retry|all]

Prerequisites
-------------
    Generated files must exist in generated/:
        ~/.jdk/jdk-21.0.10+7/bin/java -jar jars/antlr4.jar \\
            -Dlanguage=Python3 -visitor -o generated \\
            grammars/SQLiteLexer.g4 grammars/SQLiteParser.g4

    Beam parser also needs a trained weights.json:
        uv run python examples/sqlite_demo.py quality   # trains for 5 epochs
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generated"))

from SQLiteLexer import SQLiteLexer
from SQLiteParser import SQLiteParser

from antlr_adaptive import BeamParser, QualityParser, RetryParser, WeightStore

WEIGHTS_FILE = os.path.join(os.path.dirname(__file__), "..", "weights.json")

VALID = [
    "SELECT * FROM users;",
    "SELECT id, name FROM users WHERE id = 1;",
    "SELECT a.id, b.name FROM a JOIN b ON a.id = b.id WHERE a.x > 10;",
    "SELECT COUNT(*) FROM orders GROUP BY status HAVING COUNT(*) > 5;",
    "SELECT * FROM t ORDER BY name ASC LIMIT 10 OFFSET 5;",
    "SELECT x FROM t WHERE x IN (SELECT y FROM s);",
    "SELECT DISTINCT name FROM users;",
    "SELECT * FROM t WHERE x IS NOT NULL;",
    "SELECT id, SUM(amount) FROM orders GROUP BY id;",
    "SELECT * FROM a LEFT JOIN b ON a.id = b.id;",
    "INSERT INTO users (id, name) VALUES (1, 'alice');",
    "INSERT INTO users VALUES (2, 'bob');",
    "INSERT INTO t (x, y) VALUES (1, 2);",
    "UPDATE users SET name = 'bob' WHERE id = 2;",
    "UPDATE t SET x = 1, y = 2 WHERE id = 3;",
    "DELETE FROM users WHERE id = 3;",
    "DELETE FROM t WHERE x > 100;",
    "CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT NOT NULL);",
    "CREATE TABLE IF NOT EXISTS cfg (key TEXT, value TEXT);",
    "DROP TABLE users;",
    "BEGIN TRANSACTION;",
    "COMMIT;",
    "ROLLBACK;",
]

BROKEN = [
    "SELECT FROM;",
    "INSERT INTO VALUES;",
    "SELECT * FROM t WHERE;",
    "CREATE TABLE;",
    "SELECT * FROM t WHERE id = AND name = 'x';",
    "UPDATE SET x = 1;",
    "DELETE WHERE id = 1;",
    "INSERT VALUES;",
]


# ---------------------------------------------------------------------------
# Quality / training demo
# ---------------------------------------------------------------------------

def demo_quality(epochs: int = 5):
    store = WeightStore()
    store.load(WEIGHTS_FILE)

    qp = QualityParser(SQLiteLexer, SQLiteParser, start_rule="parse", store=store)

    print(f"\n{'='*65}")
    print(f"  QualityParser — training  (starting epoch {store.epochs + 1})")
    print(f"{'='*65}")

    qp.train(VALID + BROKEN, epochs=epochs, verbose=True)
    store.save(WEIGHTS_FILE)

    # show score separation
    valid_scores  = [qp.parse(s).score for s in VALID]
    broken_scores = [qp.parse(s).score for s in BROKEN]
    avg_v = sum(valid_scores)  / len(valid_scores)
    avg_b = sum(broken_scores) / len(broken_scores)
    print(f"\n  avg score  valid={avg_v:+.4f}  broken={avg_b:+.4f}  "
          f"sep={avg_v - avg_b:+.4f}")
    print(f"  epoch {store.epochs}  weight keys={len(store.weights)}")


# ---------------------------------------------------------------------------
# Beam demo
# ---------------------------------------------------------------------------

def demo_beam():
    store = WeightStore()
    store.load(WEIGHTS_FILE)

    if store.epochs == 0:
        print("No trained weights found. Run:  python examples/sqlite_demo.py quality")
        sys.exit(1)

    bp = BeamParser(SQLiteLexer, SQLiteParser, store,
                    start_rule="parse", beam_width=4)

    queries = VALID[:3] + BROKEN

    print(f"\n{'='*65}")
    print(f"  BeamParser  beam_width=4  epoch={store.epochs}")
    print(f"{'='*65}")

    total_broken = 0
    fewer_errors = 0

    for sql in queries:
        print(f"\n  Query: {sql}")
        print(f"  {'─'*60}")
        baseline = bp._run(sql, forced={})
        best = bp.parse(sql, verbose=True)
        if baseline.n_errors > 0:
            total_broken += 1
            if best.n_errors < baseline.n_errors:
                fewer_errors += 1

    print(f"\n  Broken queries : {total_broken}")
    print(f"  Errors reduced : {fewer_errors}/{total_broken}")


# ---------------------------------------------------------------------------
# Retry demo
# ---------------------------------------------------------------------------

def demo_retry():
    store = WeightStore()
    store.load(WEIGHTS_FILE)
    has_weights = store.epochs > 0

    rp = RetryParser(
        SQLiteLexer, SQLiteParser,
        start_rule="parse",
        store=store if has_weights else None,
        max_retries=20,
    )

    queries = VALID[:3] + BROKEN

    print(f"\n{'='*65}")
    print(f"  RetryParser  max_retries=20  "
          f"weights={'epoch=' + str(store.epochs) if has_weights else 'none'}")
    print(f"{'='*65}")

    solved = 0
    broken_total = len(BROKEN)

    for sql in queries:
        kind = "clean" if sql in VALID else "broken"
        print(f"\n  [{kind}] {sql}")
        print(f"  {'─'*60}")
        best = rp.parse(sql, verbose=True)
        if kind == "broken" and best.ok:
            solved += 1

    print(f"\n  Broken queries solved (0 errors): {solved}/{broken_total}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("quality", "all"):
        demo_quality()
    if mode in ("beam", "all"):
        demo_beam()
    if mode in ("retry", "all"):
        demo_retry()
