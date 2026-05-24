"""
Uses pretrained GloVe word vectors from Stanford NLP.

GloVe:
Jeffrey Pennington, Richard Socher, and Christopher D. Manning.
https://nlp.stanford.edu/projects/glove/

Pretrained vectors distributed under PDDL 1.0:
https://opendatacommons.org/licenses/pddl/1-0/
"""
import os, zipfile
import numpy as np
from pathlib import Path
import requests

from .constants import (
    GLOVE_FILE, GLOVE_URL, DATA_DIR,
    WORDS_FILE, VECS_FILE
)



def download_glove():
    if GLOVE_FILE.exists():
        print(f"{GLOVE_FILE} already present.")
        return

    zip_path = Path("glove.6B.zip")
    if not zip_path.exists():
        print("Downloading GloVe 6B (822 MB)...")
        with requests.get(GLOVE_URL, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            done = 0
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        print(f"\r  {done/total*100:.1f}%  ({done>>20} MB)", end="", flush=True)
        print()

    print("Extracting glove.6B.50d.txt...")
    with zipfile.ZipFile(zip_path) as z:
        z.extract("glove.6B.50d.txt", DATA_DIR)
    print("Done.")



def build_vocab():
    print(f"\nLoading {GLOVE_FILE}...")
    words = WORDS_FILE.read_text(encoding="utf-8").splitlines()
    word_set = set(words)

    found_words, found_vecs = [], []
    with open(GLOVE_FILE, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip().split(" ")
            if parts[0] in word_set:
                found_words.append(parts[0])
                found_vecs.append([float(x) for x in parts[1:]])

    missing = word_set - set(found_words)
    print(f"Found: {len(found_words)}/{len(words)}")
    if missing:
        print(f"Missing: {sorted(missing)}")

    order = {w: i for i, w in enumerate(words)}
    pairs = sorted(zip(found_words, found_vecs), key=lambda p: order.get(p[0], 9999))
    found_words, found_vecs = zip(*pairs)

    return list(found_words), np.array(found_vecs, dtype=np.float32)



def main():
    download_glove()
    kept_words, kept_vecs = build_vocab()

    np.save(VECS_FILE, kept_vecs)
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(kept_words))

    print(f"\nSaved {len(kept_words)} words - shape {kept_vecs.shape}")
    print(f"\t{str(VECS_FILE):<30} {os.path.getsize(VECS_FILE) // 1024} KB")

if __name__ == "__main__":
    main()