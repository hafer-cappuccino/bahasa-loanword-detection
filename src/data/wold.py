import ast
from dataclasses import asdict, dataclass
from typing import List

import bonobo
import pandas as pd
from pycldf.dataset import Dataset, Wordlist


dataset: Dataset = Dataset.from_metadata('lib/wold/cldf/cldf-metadata.json')

forms: Wordlist = list(dataset['FormTable'])


@dataclass(frozen=True)
class WordForm:
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


def extract_words():
    for form in forms:
        yield WordForm(
            value=form['Value'],
            segments=form['Segments'],
            language=form['Language_ID'],
            borrowing_score=float(form['Borrowed_score']),
            age_label=form['age_label'],
        )


def filter_indonesian_words(form: WordForm):
    if form.language == 'Indonesian':
        yield form


def load_to_df(csv):
    df: pd.DataFrame = pd.read_csv(csv)
    df['segments'] = df['segments'].apply(lambda x: ast.literal_eval(x))
    return df.to_pickle('dataframe.pkl')



if __name__ == '__main__':
    graph = bonobo.Graph()

    graph.add_chain(
        extract_words,
        filter_indonesian_words,
        asdict,
        bonobo.UnpackItems(0),  # transform from bonobo node to top-level namedtuple
        bonobo.CsvWriter(
            'out/indonesian_wordforms.csv',
            fields=('value', 'segments', 'language', 'borrowing_score', 'age_label')
        ),
    )

    bonobo.run(graph)
