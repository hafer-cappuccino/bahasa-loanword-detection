import pytest
from src.data.wold import dataset


@pytest.fixture(scope='function')
def wold_cldf():
    return dataset
