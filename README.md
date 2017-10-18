# TRADERS_DICTIONARY

This repository contains the trader names dictionary used to prepare data for [trase.earth](https://trase.earth).

`traders.csv` contains trader names in the following format `NAME;CORRECT_NAME`. It includes both typos and subsidiaries, without distinguishing the two.

`check_trader_names.py` is a small Python script that can be used to apply the dictionary on a new list of traders names, returning a list of corrected names.

To use the script, put the file containing the trader names to be checked (e.g. `in.txt`) in the repository (the file should contain one name per line), and run the following:

```
python2 check_trader_names.py input.txt output.txt
```

First, close matches are presented, and if none are found or chosen, the full list of existing trader names is given, allowing to choose a match.

When the name to be checked is already in the dictionary, it is replaced by the correct name in the output file.

When a new match with an existing correct name is found, the dictionary is updated with the new name.

When a new name without match is encountered, it is added to the dictionary.