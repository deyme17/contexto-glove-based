import sys
import numpy as np
from typing import List, Optional, Set
from .constants import WORDS_FILE, VECS_FILE



def emb_to_word(emb: np.ndarray, words: List[str], matrix: np.ndarray,
                exclude: Optional[Set[str]] = None) -> str:
    """Return the word whose embedding is closest (cosine) to emb."""
    norms = np.linalg.norm(matrix, axis=1)
    emb_norm = np.linalg.norm(emb)
    safe_norms = np.where(norms > 1e-10, norms, 1.0)
    safe_emb = emb_norm if emb_norm > 1e-10 else 1.0
    sims = (matrix @ emb) / (safe_norms * safe_emb)

    if exclude:
        for w in exclude:
            if w in words:
                sims[words.index(w)] = -2.0

    return words[int(np.argmax(sims))]



def autocomplete(prefix: str, words: List[str], limit: int = 8) -> List[str]:
    p = prefix.lower()
    return [w for w in words if w.startswith(p)][:limit]



def load_data() -> tuple[list[str], np.ndarray]:
    """Load vocabulary and embeddings."""
    missing = [p for p in (WORDS_FILE, VECS_FILE) if not p.exists()]
    if missing:
        print("Missing data files:")
        for p in missing:
            print(f"\t{p}")
        print("\nRun download_gloves.py first to download the GloVe vectors.")
        sys.exit(1)

    words = WORDS_FILE.read_text(encoding="utf-8").splitlines()
    matrix = np.load(VECS_FILE)

    if len(words) != matrix.shape[0]:
        print(
            f"Data mismatch: {len(words)} words but {matrix.shape[0]} vectors.\n"
            "Re-run download_gloves.py to rebuild the data files."
        )
        sys.exit(1)

    print(f"Loaded {len(words)} words | embedding dim = {matrix.shape[1]}")
    return words, matrix