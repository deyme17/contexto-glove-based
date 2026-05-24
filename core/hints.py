from __future__ import annotations
from typing import Optional, Tuple, List, Set
import random as rnd
from dataclasses import dataclass

import numpy as np
from utils import emb_to_word


@dataclass
class Hint:
    kind: str               # "direction" | "composition"
    word: str               # primary hint word shown to the player
    tip1: Optional[str]     # composition only: the addend word
    tip2: Optional[str]     # composition only: the delta word


class HintEngine:
    """
    Engine for generating hints based on word embeddings. 
    Provides both direction and composition hints.
    """
    def __init__(self, words: List[str], matrix: np.ndarray, target: str) -> None:
        """Initializes the hint engine with the word list, embedding matrix, and target word."""
        self._words = words
        self._matrix = matrix
        self._target_word = target
        self._target_emb = matrix[words.index(target)]
        self._used: Set[str] = {target}

    def _random_emb(self) -> Tuple[str, np.ndarray]:
        """
        Selects a random word and returns it along with its embedding.
        Ensures the word hasn't been used as a hint before.
        """
        candidates = [w for w in self._words if w not in self._used]
        if not candidates:
            self._used.clear()
            candidates = self._words[:]
        word = rnd.choice(candidates)
        self._used.add(word)
        return word, self._matrix[self._words.index(word)]

    def direction(self) -> Hint:
        """Generates a direction hint based on a random word."""
        rand_word, rand_emb = self._random_emb()
        hint = emb_to_word(self._target_emb - rand_emb, 
                           self._words, 
                           self._matrix,
                           exclude={rand_word, self._target_word})
        return Hint(kind="direction", word=hint, tip1=None, tip2=None)

    def composition(self) -> Hint:
        """Generates a composition hint based on a random word."""
        _, rand_emb = self._random_emb()
        diff = self._target_emb - rand_emb
        tip1 = emb_to_word(rand_emb, self._words, self._matrix)
        tip2 = emb_to_word(diff, self._words, self._matrix, exclude={tip1, self._target_word})
        return Hint(kind="composition", word=tip2, tip1=tip1, tip2=tip2)