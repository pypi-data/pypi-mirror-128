from difflib import SequenceMatcher
from itertools import zip_longest
from statistics import mean
from typing import Iterable, Union

import pandas as pd


def stringify(seq: Union[Iterable, None], start: int = 1) -> str:
    """ Turns a row of data into a string.

    @param seq: Sequence to be transformed into a string
    @param start: Integer 1 by default, skips the index value
    @return: string of data
    """
    if seq is not None:
        return " ".join(map(str, seq[start:]))
    else:
        return ""


def csv_similarity_score(csv_true: str, csv_test: str, delimiter: str = ",") -> float:
    """ Compares the source of truth to the test case. Returns a score in
        range [0.0, 1.0] where 0.0 indicates no matching data and 1.0 indicates
        an exact match of all data.

    @param csv_true: Source of truth: path to csv file
    @param csv_test: Test cases: path to csv file
    @param delimiter: Expected CSV delimiter, default = ','
    @return: Returns average similarity score, always between 0.0 and 1.0
    """
    true = pd.read_csv(csv_true, delimiter=delimiter)
    test = pd.read_csv(csv_test, delimiter=delimiter)

    scores = (
        SequenceMatcher(a=stringify(a), b=stringify(b)).ratio()
        for a, b in zip_longest(true.values, test.values)
    )

    return mean(scores)
