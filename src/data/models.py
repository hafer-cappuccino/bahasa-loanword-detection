from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass(frozen=True)
class WordForm:
    """
    A single sample from WOLD encapsulated as a dataclass
    for convenience.
    """

    # the actual word form
    value: str

    # the word form tokenized as character segments, '+' represents a space
    segments: List[str]

    # the language the word form belongs to
    language: str

    # the borrowing score of the word, range of [0, 1],
    # with 1 being clearly borrowed
    borrowing_score: float

    # The following ages were used.
    # "Prehistorical" until end of year 500.
    # "Modern" from the 8th century.
    # "Early Malay" is between Prehistorical and Modern.
    age_label: str


@dataclass
class Dataset:
    """
    A dataset split into training and test sets.
    Used with sklearn.model_selection.train_test_split.
    """
    X_train: np.array
    X_test: np.array
    y_train: np.array
    y_test: np.array
