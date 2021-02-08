from dataclasses import asdict, dataclass
from typing import List, Tuple

import bonobo
from pycldf.dataset import Dataset


dataset: Dataset = Dataset.from_metadata('lib/wold/cldf/cldf-metadata.json')


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


def extract_words():
    forms = list(dataset['FormTable'])
    for form in forms:
        yield WordForm(
            value=form['Value'],
            segments=form['Segments'],
            language=form['Language_ID'],
            borrowing_score=float(form['Borrowed_score'])
        )


def filter_indonesian_words(form: WordForm):
    if form.language == 'Indonesian':
        yield asdict(form)


# TODO: Add to the pipeline
def filter_indonesian_loanwords(form: WordForm):
    if form.borrowing_score == 1.0:
        yield form


def load_to_dataframe(form):
    pass



if __name__ == '__main__':
    graph = bonobo.Graph()

    graph.add_chain(
        extract_words,
        filter_indonesian_words,
        bonobo.UnpackItems(0),  # transform from bonobo node to top-level namedtuple
        bonobo.CsvWriter(
            'indonesian_wordforms.csv',
            fields=('value', 'segments', 'borrowing_score')
        )
    )

    bonobo.run(graph)
