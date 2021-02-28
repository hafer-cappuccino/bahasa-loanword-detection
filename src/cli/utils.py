from dataclasses import asdict, dataclass
from typing import Any

import matplotlib.pyplot as plt
from sklearn.base import ClassifierMixin
from sklearn.metrics import (
    classification_report,
    plot_confusion_matrix,
)

from src.data.models import Dataset


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


def evaluate(model: ClassifierMixin, dataset: Dataset):
    message = (
        f'\n 🚀 {model.__class__.__name__} classification report'
        'and confusion matrix plot'
    )

    print(message)
    print('-' * len(message))
    print(
        classification_report(
            model.predict(dataset.X_test),
            dataset.y_test,
            target_names=['native', 'loanwords'],
        )
    )
    plot_confusion_matrix(model.classifier, dataset.X_test, dataset.y_test)
    plt.show()
    print()
