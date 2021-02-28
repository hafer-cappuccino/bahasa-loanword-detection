from dataclasses import asdict, dataclass
from typing import Any, Union

import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
)
from tabulate import tabulate

from src.data.models import Dataset
from src.models.markov import Markov
from src.models.svm import SVM




@dataclass
class ClickOptions:
    default: Any
    help: str
    type: Any


TEST_SIZE_OPTIONS = asdict(
    ClickOptions(
        0.2,
        'The size of the test set proportional to the entire dataset.',
        float,
    )
)


SEED_OPTIONS = asdict(
    ClickOptions(
        42,
        'The seed number to reproduce the shuffled and split dataset.',
        int,
    )
)


def evaluate(model: Union[Markov, SVM], dataset: Dataset):
    message = (
        f'\n 🚀 {model.__class__.__name__}'
    )

    print(message)
    print('-' * len(message))
    print('Classification Report')
    print(
        classification_report(
            model.predict(dataset.X_test),
            dataset.y_test,
            target_names=['native', 'loanwords'],
        )
    )

    print('\nConfusion Matrix')

    df = pd.DataFrame(
        confusion_matrix(dataset.y_test, model.predict(dataset.X_test)),
        columns=['P', 'N'],
        index=['P', 'N'],
    )

    print(tabulate(df, headers='keys', tablefmt='psql'))
