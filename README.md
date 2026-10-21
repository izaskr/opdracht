# Assignment for the psychometric data scientist position at Cito
This repository presents my solution for the take-home assignment received by Cito. 

Code author: Iza Skrjanec

## Requirements
It is advised to install dependencies into a new virtual environment.
```
pip install stanza wn scikit-learn sentence-transformers pandas pillow matplotlib
```

Additionally, install the following models for stanza (for lemmatization) and wn (WordNet for synonym extraction):

```
import stanza
stanza.download("nl")

import wn
wn.download("omw:2.0")
```

The paths are currently hard-coded to the author of the code, but can be changed by replacing `/home/skrjanec` accordingly.

## Solution

I implemented solutions addressing automated scoring (items 3 and 4) and similarity (items 1, 2, 4).
Automated scoring is based on string matching (including lemma and synonym matches).
Similarity analysis is based on k-means clustering of sentence embeddings (computed with the model NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers).

More information about the model: https://huggingface.co/NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers


## Usage on new data

The script `main.py` includes code for treating new responses. It assumes 4 items. Run `python main.py` to evaluate new responses. The assigned scores and clusters are written to `/results`"
