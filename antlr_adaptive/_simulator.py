"""ANTLR ATN simulator subclasses and error listener."""

from antlr4 import ParserATNSimulator
from antlr4.error.ErrorListener import ErrorListener

from ._features import extract_features


class FeedbackErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, col, msg, e):
        self.errors.append({"line": line, "col": col, "msg": msg})


class ObservingATNSimulator(ParserATNSimulator):
    """
    Records every adaptivePredict call without changing ANTLR's choice.
    Used by QualityParser to build a trace for weight updates.
    trace: list of (decision, alt, features)
    """

    def __init__(self, parser, atn, decision_to_dfa, shared_context_cache):
        super().__init__(parser, atn, decision_to_dfa, shared_context_cache)
        self.trace: list = []

    def adaptivePredict(self, input, decision, outerContext):
        antlr_alt = super().adaptivePredict(input, decision, outerContext)
        features = extract_features(input, decision, outerContext)
        self.trace.append((decision, antlr_alt, features))
        return antlr_alt


class ForcedATNSimulator(ParserATNSimulator):
    """
    Overrides specific decisions with pre-chosen alternatives.
    forced = {decision_index: alt_to_force}
    All other decisions fall through to ANTLR's normal prediction.
    trace: list of (decision, chosen_alt, antlr_alt, features)
    """

    def __init__(self, parser, atn, decision_to_dfa, shared_context_cache,
                 forced: dict, store=None):
        super().__init__(parser, atn, decision_to_dfa, shared_context_cache)
        self.forced = forced
        self.store = store
        self.trace: list = []

    def adaptivePredict(self, input, decision, outerContext):
        antlr_alt = super().adaptivePredict(input, decision, outerContext)
        features = extract_features(input, decision, outerContext)
        chosen = self.forced.get(decision, antlr_alt)
        self.trace.append((decision, chosen, antlr_alt, features))
        return chosen
