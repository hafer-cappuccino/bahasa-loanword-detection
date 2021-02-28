from types import GeneratorType

from src.data.etl import cldf_dataset, extract_words, filter_indonesian_words
from src.data.models import WordForm


def test_dataset():
    assert cldf_dataset.module == 'Wordlist'
    assert cldf_dataset.properties['dc:identifier'] == 'http://wold.clld.org'


def test_pipeline():
    extracted_words = extract_words()
    assert isinstance(extracted_words, GeneratorType)

    assert isinstance(list(extracted_words)[0], WordForm)

    for word in extracted_words:
        form = list(filter_indonesian_words(extracted_words(word))).pop()
        assert form.language == 'Indonesian'
