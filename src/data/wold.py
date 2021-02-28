import ast
from dataclasses import dataclass
from typing import List

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer


@dataclass
class WOLD:
    csv_path: str = 'out/indonesian_wordforms.csv'
    df: pd.DataFrame = None
    encoder: MultiLabelBinarizer = MultiLabelBinarizer()

    def __post_init__(self):
        self.df = pd.read_csv(self.csv_path)
        self.df['segments'] = self.df['segments'].apply(lambda x: ast.literal_eval(x))

        # only consider borrowing scores 1, everything else is *not* a loanword
        self.df.loc[self.df.borrowing_score != 1.0, 'borrowing_score'] = 0
        self.df.borrowing_score = self.df.borrowing_score.astype(int)

        self.df['segments'] = self.df['segments'].apply(WOLD.fold)

    def onehot(self) -> pd.DataFrame:
        """
        Return a onehot encoding of the samples.
        """
        return self.encoder.fit_transform(self.df.segments)

    @staticmethod
    def fold(segments) -> List[str]:
        """
        Removes any segments that have two graphemes represented by a '/' in the
        segment. We have decided to take this approach since in Bahasa, the
        grapheme representation of such segments produce the same sound, i.e.
        they are ultimately the same phoneme.

        :param segments: a list of segments, that are phonemes represented by
            some grapheme.
        :return: a list of segments.
        """
        processed = []
        for segment in segments:
            segment = segment.lower()
            if segment in ('a/a', 'j/dʒ', 'k/k', 'm/m', 'r/r', 's/s', 'ss/s'):
                processed.append(segment.split('/')[-1])
            else:
                processed.append(segment)
        return processed
