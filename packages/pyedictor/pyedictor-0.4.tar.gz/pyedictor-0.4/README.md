# PyEDICTOR: Simple Access to EDICTOR Databases

## Installation:

```
$ pip install pyedictor
```

## Usage

```python
>>> from pyedictor import fetch
>>> wl = fetch("deepadungpalaung", to_lingpy=True)
>>> print(wl.width)
16
```

To load as a LexStat wordlist:

```python
>>> from lingpy import *
>>> from pyedictor import fetch
>>> lex = fetch("deepadungpalaung", to_lingpy=True, transform=LexStat)
```

To convert your dataset to EDICTOR format from CLDF:

```
$ edictor wordlist -d cldf/cldf-metadata.json mydataset
```

This will create a wordlist file `mydataset.tsv` from your CLDF data located in `cldf/cldf-metadata.json`.


