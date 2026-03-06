"""
antlr_adaptive
==============

Learned parse-quality scoring and guided backtracking for any ANTLR4 grammar.

Public API
----------
QualityParser   -- observe-and-learn; assigns quality scores to parse attempts
BeamParser      -- re-parse with model-preferred alternatives (needs trained weights)
RetryParser     -- exhaustive backtracking retry (no training required)
WeightStore     -- persistent (decision, alt) -> weight-vector store
ParseResult     -- unified result type returned by all three parsers
"""

from .beam import BeamParser
from .quality import QualityParser
from .retry import RetryParser
from .types import ParseResult
from .weights import WeightStore

__all__ = [
    "QualityParser",
    "BeamParser",
    "RetryParser",
    "WeightStore",
    "ParseResult",
]
