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

To be continued...
