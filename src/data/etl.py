from dataclasses import asdict

import bonobo
from pycldf.dataset import Dataset, Wordlist

from src.data.models import WordForm


cldf_dataset: Dataset = Dataset.from_metadata('lib/wold/cldf/cldf-metadata.json')

forms: Wordlist = list(cldf_dataset['FormTable'])


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
