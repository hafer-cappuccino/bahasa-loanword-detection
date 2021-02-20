from types import GeneratorType

from src.data.wold import WordForm, dataset, extract_words


def test_dataset():
    assert dataset.module == 'Wordlist'
    assert dataset.properties['dc:identifier'] == 'http://wold.clld.org'


def test_pipeline():
    extracted_words = extract_words()
    assert isinstance(extracted_words, GeneratorType)

    assert isinstance(list(extracted_words)[0], WordForm)

    for word in extracted_words:
        form = list(filter_indonesian_loanwords(extracted_words(word))).pop()
        assert form.language == 'Indonesian'
