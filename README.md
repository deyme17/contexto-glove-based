# contexto-glove-based

A Contexto-inspired word guessing game built on pretrained GloVe embeddings. The player tries to identify a hidden target word by submitting guesses and receiving feedback based on semantic similarity in vector space.

Although the current dataset is a small curated biology vocabulary, the pipeline is fully domain-agnostic: any word list can be used to construct a custom semantic game space.

---

## Core idea

Each word is mapped to a dense vector representation using pretrained GloVe embeddings. The distance between words is measured in embedding space (using cosine similarity), allowing the game to rank guesses by semantic proximity to a hidden target.

This transforms the game into a navigation problem in a continuous semantic manifold rather than a categorical search.

---

## Embeddings

The project uses Stanford NLP GloVe vectors:

- https://nlp.stanford.edu/projects/glove/
- Jeffrey Pennington, Richard Socher, Christopher D. Manning
- License: Public Domain Dedication and License (PDDL 1.0)

Model used: `glove.6B.50d.txt`

---

## Pipeline

The preprocessing script performs the following steps:

1. Downloads GloVe archive if missing
2. Extracts `glove.6B.50d.txt`
3. Loads a user-defined vocabulary from `data/words.txt`
4. Filters embeddings to only words present in that vocabulary
5. Builds a compact embedding matrix aligned with the vocabulary order

Outputs:

- `data/vectors.npy` — filtered embedding matrix
- updated `data/words.txt` — cleaned vocabulary list

---

## Key properties

- Domain-agnostic (biology, medicine, physics, general language, etc.)
- Deterministic alignment between words and embeddings
- Fully offline gameplay after preprocessing
- Efficient similarity computation via NumPy

---

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run preprocessing:

```bash
python -m utils.download_gloves
```

This will produce:

- extracted GloVe vectors  
- filtered vocabulary  
- aligned embedding matrix (`vectors.npy`)

---

## Project structure

```
contexto-glove-based/
├── data/
│   ├── words.txt          # vocabulary (one word per line)
│   └── vectors.npy        # aligned embedding matrix (produced by preprocessing)
├── core/
│   ├── game.py            # GameState, Guess dataclass, new_game() factory
│   ├── meters.py          # SimilarityMeter ABC + Cosine / Euclidean / Manhattan / Chessboard
│   └── hints.py           # HintEngine — direction and composition hints
├── gui/
│   └── window.py          # PyQt6 main window
├── utils/
│   └── download_gloves.py # preprocessing script
├── main.py                # entry point
└── requirements.txt
```

---

## Game mechanics

### Guessing

Submit any word from the vocabulary. Each guess returns:

| Field | Description |
|-------|-------------|
| `rank` | Position in vocabulary sorted by distance to target (1 = target itself) |
| `score` | `100 × (1 − (rank − 1) / (n − 1))` — percentage score in `[0, 100]` |
| `is_win` | `True` when the guess matches the target exactly |

The score provides a continuous signal: 100% means you found the target, 0% means you picked the furthest word in the vocabulary.

### Similarity metrics

The metric used to rank guesses can be changed at any time. Switching metrics recomputes all ranks and scores for every guess made so far.

| Metric | Formula |
|--------|---------|
| **Cosine** *(default)* | `1 − (a·b) / (‖a‖ ‖b‖)` |
| **Euclidean** | `‖a − b‖₂` |
| **Manhattan** | `‖a − b‖₁` |
| **Chessboard** | `‖a − b‖∞` |

Cosine distance is recommended for GloVe embeddings because it is scale-invariant and reflects directional similarity regardless of vector magnitude.

### Hints

Two hint types are available. Both are generated via arithmetic in embedding space and do not reveal the target word directly.

**Direction hint** — points toward the target from a random reference word:

> Find word `h` closest to `E_target − E_random`

The result is a word that lies in the semantic direction of the target relative to a random anchor.

**Composition hint** — decomposes the target as a sum of two words:

> Find `t1` closest to `E_random`, then `t2` closest to `E_target − E_random`  
> Hint reads: *"Your word relates to `t1` + `t2`"*

This exploits the well-known additive structure of word embeddings (e.g. `king − man + woman ≈ queen`).

---

## Architecture

### `GameState`

The central game object. Constructed via the `new_game()` factory:

```python
from core.game import new_game

state = new_game(words, matrix)           # random target, cosine metric
state = new_game(words, matrix, target="mosquito")
state = new_game(words, matrix, meter=EuclideanMeter())
```

Key methods:

```python
guess = state.guess("brain")    # returns Guess or None if word not in vocab
hint  = state.hint("direction") # or "composition"
state.change_meter(ManhattanMeter())  # reranks all previous guesses in-place
```

Ranks are computed lazily on first use and cached — subsequent lookups are O(1).

### `SimilarityMeter`

Abstract base class. Implement two methods to add a custom metric:

```python
class MyMeter(SimilarityMeter):
    @property
    def name(self) -> str:
        return "My metric"

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        ...
```

Pass an instance to `new_game()` or `state.change_meter()`.

---

## Customising the vocabulary

Replace `data/words.txt` with any newline-separated word list, then re-run preprocessing. Words absent from GloVe will be reported and dropped automatically.

```bash
# example: use a medical vocabulary
cp my_medical_words.txt data/words.txt
python -m utils.download_gloves
```

The rest of the pipeline (game logic, hints, GUI) requires no changes.

---

## Requirements

- Python ≥ 3.10
- numpy
- PyQt6
- requests *(preprocessing only)*