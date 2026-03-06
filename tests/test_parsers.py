"""
Basic tests for antlr_adaptive against the SQLite grammar.

Run:
    uv run pytest tests/ -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generated"))

from SQLiteLexer import SQLiteLexer
from SQLiteParser import SQLiteParser

from antlr_adaptive import BeamParser, ParseResult, QualityParser, RetryParser, WeightStore


VALID_SQL = [
    "SELECT * FROM users;",
    "INSERT INTO t (id) VALUES (1);",
    "DELETE FROM t WHERE id = 1;",
    "UPDATE t SET x = 1 WHERE id = 2;",
    "CREATE TABLE t (id INTEGER PRIMARY KEY);",
]

BROKEN_SQL = [
    "SELECT FROM;",
    "INSERT INTO VALUES;",
    "SELECT * FROM t WHERE;",
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def trained_store():
    """Return a WeightStore trained for 3 epochs on the SQL samples."""
    store = WeightStore()
    qp = QualityParser(SQLiteLexer, SQLiteParser, store=store)
    qp.train(VALID_SQL + BROKEN_SQL, epochs=3)
    return store


# ---------------------------------------------------------------------------
# ParseResult
# ---------------------------------------------------------------------------

class TestParseResult:
    def test_ok_no_errors(self):
        r = ParseResult(forced={}, errors=[], tokens_consumed=5,
                        score=1.0, n_decisions=3)
        assert r.ok
        assert r.n_errors == 0

    def test_ok_with_errors(self):
        r = ParseResult(forced={}, errors=[{"line": 1, "col": 0, "msg": "err"}],
                        tokens_consumed=2, score=0.0, n_decisions=1)
        assert not r.ok

    def test_is_better_than_fewer_errors(self):
        good = ParseResult(forced={}, errors=[], tokens_consumed=5,
                           score=0.0, n_decisions=1)
        bad  = ParseResult(forced={}, errors=[{"line":1,"col":0,"msg":"x"}],
                           tokens_consumed=5, score=10.0, n_decisions=1)
        assert good.is_better_than(bad)
        assert not bad.is_better_than(good)

    def test_is_better_than_more_tokens(self):
        a = ParseResult(forced={}, errors=[], tokens_consumed=10,
                        score=0.0, n_decisions=1)
        b = ParseResult(forced={}, errors=[], tokens_consumed=5,
                        score=0.0, n_decisions=1)
        assert a.is_better_than(b)

    def test_is_better_than_higher_score(self):
        a = ParseResult(forced={}, errors=[], tokens_consumed=5,
                        score=2.0, n_decisions=1)
        b = ParseResult(forced={}, errors=[], tokens_consumed=5,
                        score=1.0, n_decisions=1)
        assert a.is_better_than(b)


# ---------------------------------------------------------------------------
# QualityParser
# ---------------------------------------------------------------------------

class TestQualityParser:
    def test_valid_parses_clean(self):
        qp = QualityParser(SQLiteLexer, SQLiteParser)
        for sql in VALID_SQL:
            r = qp.parse(sql)
            assert r.ok, f"Expected clean parse for: {sql}"

    def test_broken_has_errors(self):
        qp = QualityParser(SQLiteLexer, SQLiteParser)
        for sql in BROKEN_SQL:
            r = qp.parse(sql)
            assert not r.ok, f"Expected errors for: {sql}"

    def test_learn_returns_result(self):
        qp = QualityParser(SQLiteLexer, SQLiteParser)
        r = qp.learn("SELECT * FROM t;")
        assert isinstance(r, ParseResult)
        assert r.ok

    def test_train_increments_epochs(self):
        store = WeightStore()
        qp = QualityParser(SQLiteLexer, SQLiteParser, store=store)
        qp.train(VALID_SQL, epochs=2)
        assert store.epochs == 2

    def test_score_separation_after_training(self, trained_store):
        """Valid queries should score higher than broken ones on average."""
        qp = QualityParser(SQLiteLexer, SQLiteParser, store=trained_store)
        valid_avg  = sum(qp.parse(s).score for s in VALID_SQL)  / len(VALID_SQL)
        broken_avg = sum(qp.parse(s).score for s in BROKEN_SQL) / len(BROKEN_SQL)
        assert valid_avg > broken_avg, (
            f"Expected valid avg ({valid_avg:.3f}) > broken avg ({broken_avg:.3f})"
        )


# ---------------------------------------------------------------------------
# WeightStore
# ---------------------------------------------------------------------------

class TestWeightStore:
    def test_get_initialises_zeros(self):
        ws = WeightStore()
        w = ws.get(0, 1)
        assert all(x == 0.0 for x in w)

    def test_score_zero_before_training(self):
        ws = WeightStore()
        features = [1.0] + [0.0] * 693
        assert ws.score(0, 1, features) == 0.0

    def test_update_changes_weights(self):
        ws = WeightStore()
        features = [1.0] + [0.0] * 693
        ws.update(0, 1, features, reward=1.0)
        assert ws.get(0, 1)[0] > 0.0

    def test_save_load_roundtrip(self, tmp_path):
        ws = WeightStore()
        features = [1.0] + [0.0] * 693
        ws.update(0, 1, features, reward=1.0)
        ws.epochs = 7
        path = str(tmp_path / "weights.json")
        ws.save(path)

        ws2 = WeightStore()
        ws2.load(path)
        assert ws2.epochs == 7
        assert ws2.get(0, 1)[0] == pytest.approx(ws.get(0, 1)[0])


# ---------------------------------------------------------------------------
# RetryParser
# ---------------------------------------------------------------------------

class TestRetryParser:
    def test_valid_no_retries_needed(self):
        rp = RetryParser(SQLiteLexer, SQLiteParser)
        for sql in VALID_SQL:
            r = rp.parse(sql)
            assert r.ok, f"Expected clean parse for: {sql}"

    def test_broken_returns_parse_result(self):
        rp = RetryParser(SQLiteLexer, SQLiteParser)
        for sql in BROKEN_SQL:
            r = rp.parse(sql)
            assert isinstance(r, ParseResult)

    def test_retry_with_weights(self, trained_store):
        rp = RetryParser(SQLiteLexer, SQLiteParser, store=trained_store)
        r = rp.parse("SELECT * FROM users;")
        assert r.ok


# ---------------------------------------------------------------------------
# BeamParser
# ---------------------------------------------------------------------------

class TestBeamParser:
    def test_valid_baseline_clean(self, trained_store):
        bp = BeamParser(SQLiteLexer, SQLiteParser, trained_store)
        for sql in VALID_SQL:
            r = bp.parse(sql)
            assert r.ok, f"Expected clean parse for: {sql}"

    def test_broken_returns_parse_result(self, trained_store):
        bp = BeamParser(SQLiteLexer, SQLiteParser, trained_store)
        for sql in BROKEN_SQL:
            r = bp.parse(sql)
            assert isinstance(r, ParseResult)
