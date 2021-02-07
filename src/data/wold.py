from typing import List, Tuple

import bonobo
from pycldf.dataset import Dataset


dataset: Dataset = Dataset.from_metadata('lib/wold/cldf/cldf-metadata.json')


def extract():
    forms = list(dataset['FormTable'])
    for form in forms:
        yield form

def transform(form: Tuple[str, str]):
    if form['Language_ID'] == 'Indonesian':
        print(form['Form'])

if __name__ == '__main__':
    graph = bonobo.Graph(extract, transform)
    bonobo.run(graph)
