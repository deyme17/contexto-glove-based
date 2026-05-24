from pathlib import Path


# paths
DATA_DIR = Path("data")
WORDS_FILE = DATA_DIR / "words.txt"
GLOVE_FILE = DATA_DIR / "glove.6B.50d.txt"
VECS_FILE = DATA_DIR / "vectors.npy"

# source
GLOVE_URL = "https://downloads.cs.stanford.edu/nlp/data/glove.6B.zip"