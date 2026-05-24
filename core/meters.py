from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np


class SimilarityMeter(ABC):
    """Abstract base class for similarity meters."""
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the similarity meter."""
        pass

    @abstractmethod
    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Computes the distance between two vectors."""
        pass


class CosineMeter(SimilarityMeter):
    """Similarity meter based on cosine distance."""
    @property
    def name(self) -> str:
        return "Cosine"

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        denom = np.sqrt(np.dot(a, a)) * np.sqrt(np.dot(b, b))
        if denom < 1e-12:
            return 1.
        return 1. - (np.dot(a, b) / denom)


class EuclideanMeter(SimilarityMeter):
    """Similarity meter based on Euclidean distance."""
    @property
    def name(self) -> str:
        return "Euclidean"

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.sqrt(np.sum((a - b)**2))


class ManhattanMeter(SimilarityMeter):
    """Similarity meter based on Manhattan distance."""
    @property
    def name(self) -> str:
        return "Manhattan"

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.sum(np.abs(a - b))


class ChessboardMeter(SimilarityMeter):
    """Similarity meter based on Chessboard (Chebyshev) distance."""
    @property
    def name(self) -> str:
        return "Chessboard"

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.max(np.abs(a - b))