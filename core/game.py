from __future__ import annotations
from typing import List, Optional, Dict
import random as rnd
from dataclasses import dataclass

import numpy as np

from .meters import SimilarityMeter, CosineMeter
from .hints import HintEngine, Hint


@dataclass
class Guess:
    word: str
    rank: int
    score: float # [0, 100]
    is_win: bool


class GameState:
    """Class representing the state of the game, including the target word, guesses, and hint engine."""
    def __init__(self, words: List[str], matrix: np.ndarray,
                 meter: SimilarityMeter, target: str) -> None:
        """
        Args:
            words: List of vocabulary words.
            matrix: Embedding matrix where each row corresponds to a word in `words`.
            meter: Similarity meter used for ranking guesses.
            target: The target word to be guessed.
        """
        self.words = words
        self.matrix = matrix
        self.meter = meter
        self.target = target

        self._target_emb = matrix[words.index(target)]
        self._rank_cache: Dict[str, int] = {}
        self._guesses: List[Guess] = []
        self._hints = HintEngine(words, matrix, target)
        self.won = False

    # === helpers ===

    def _build_rank_cache(self) -> None:
        """Precomputes the rank of each word in the vocabulary based on its distance to the target."""
        distances = np.array(
            [self.meter.distance(self._target_emb, self.matrix[i])
             for i in range(len(self.words))]
        )
        order = np.argsort(distances)
        self._rank_cache = {self.words[order[i]]: i + 1 for i in range(len(self.words))}

    def _rank(self, word: str) -> int:
        """Returns the rank of the given word based on its distance to the target. Lower is better."""
        if not self._rank_cache:
            self._build_rank_cache()
        return self._rank_cache[word]

    def _score(self, rank: int) -> float:
        """Converts a rank into a score between 0 and 100. Higher is better."""
        return round(100. * (1. - (rank - 1) / max(len(self.words) - 1, 1)), 1)

    # === api ===

    def guess(self, word: str) -> Optional[Guess]:
        """Processes a user's guess. Returns a Guess object if the word is valid (else None)."""
        w = word.lower().strip()
        if w not in self.words:
            return None
        rank = self._rank(w)
        g = Guess(word=w, rank=rank, score=self._score(rank), is_win=(w == self.target))
        self._guesses.append(g)
        if g.is_win:
            self.won = True
        return g

    def hint(self, kind: str) -> Hint:
        """Generates a hint of the specified kind ("direction" or "composition")."""
        return self._hints.direction() if kind == "direction" else self._hints.composition()

    def change_meter(self, meter: SimilarityMeter) -> None:
        """Changes the similarity meter used for ranking guesses."""
        self.meter = meter
        self._rank_cache = {}
        # recompute ranks for existing guesses
        for g in self._guesses:
            r = self._rank(g.word)
            g.rank = r
            g.score = self._score(r)

    # === proprties ===

    @property
    def guesses(self) -> List[Guess]:
        """Returns the list of guesses made so far, sorted by their rank (best guess first)."""
        return sorted(self._guesses, key=lambda g: g.rank)

    @property
    def guess_count(self) -> int:
        """Returns the number of guesses made so far."""
        return len(self._guesses)



### Factory function to create a new game state ###

def new_game(words: List[str], matrix: np.ndarray,
             meter: SimilarityMeter | None = None,
             target: str | None = None) -> GameState:
    """
    Factory function to create a new game state with the given parameters.
    Args:
        words: List of vocabulary words.
        matrix: Embedding matrix where each row corresponds to a word in `words`.
        meter: Optional similarity meter to use (defaults to CosineMeter).
        target: Optional target word to guess (defaults to a random choice from `words`).
    """
    return GameState(
        words=words,
        matrix=matrix,
        meter=meter or CosineMeter(),
        target=target or rnd.choice(words),
    )