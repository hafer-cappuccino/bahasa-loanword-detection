import pytest

from src.data.wold import dataset



@pytest.fixture(scope='module')
def wold_cldf_wordforms():
    return list(dataset['FormTable'])[100]
