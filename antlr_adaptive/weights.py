"""Persistent weight store mapping (decision, alt) -> weight vector."""

import json
import os

from ._features import FEATURE_DIM

WEIGHT_CLIP   = 3.0
LEARNING_RATE = 0.05


class WeightStore:
    """
    Maps (decision_index, alt) -> float vector of length FEATURE_DIM.
    Updated via perceptron rule; weights are clipped to [-WEIGHT_CLIP, +WEIGHT_CLIP].
    Persists to a JSON file between runs.
    """

    def __init__(self):
        self.weights: dict[str, list] = {}
        self.epochs: int = 0

    # -- access --------------------------------------------------------------

    def _key(self, decision: int, alt: int) -> str:
        return f"{decision}:{alt}"

    def get(self, decision: int, alt: int) -> list:
        k = self._key(decision, alt)
        if k not in self.weights:
            self.weights[k] = [0.0] * FEATURE_DIM
        return self.weights[k]

    def score(self, decision: int, alt: int, features: list) -> float:
        return sum(wi * fi for wi, fi in zip(self.get(decision, alt), features))

    # -- learning ------------------------------------------------------------

    def update(self, decision: int, alt: int, features: list, reward: float):
        w = self.get(decision, alt)
        for i in range(FEATURE_DIM):
            w[i] += LEARNING_RATE * reward * features[i]
            if w[i] > WEIGHT_CLIP:    w[i] = WEIGHT_CLIP
            elif w[i] < -WEIGHT_CLIP: w[i] = -WEIGHT_CLIP

    # -- persistence ---------------------------------------------------------

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump({"epochs": self.epochs, "weights": self.weights}, f)

    def load(self, path: str):
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            self.epochs = data.get("epochs", 0)
            self.weights = data.get("weights", {})
