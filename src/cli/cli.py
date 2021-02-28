
import click

from sklearn.model_selection import train_test_split

from src.cli.utils import evaluate, SEED_OPTIONS, TEST_SIZE_OPTIONS
from src.data.models import Dataset
from src.data.wold import WOLD
from src.models.markov import Markov
from src.models.svm import SVM


wold = WOLD()


@click.group()
def cli():
    pass


@cli.command(name='svm')
@click.option('--test-size', **TEST_SIZE_OPTIONS)
@click.option('--seed', **SEED_OPTIONS)
def svm(test_size, seed):
    dataset = Dataset(
        *train_test_split(
            wold.onehot(),
            wold.df.borrowing_score,
            test_size=test_size,
            random_state=seed,
        )
    )

    model = SVM(X=dataset.X_train, y=dataset.y_train)
    evaluate(model, dataset)



@cli.command(name='markov')
@click.option('--test-size', **TEST_SIZE_OPTIONS)
@click.option('--seed', **SEED_OPTIONS)
def markov(test_size, seed):
    dataset = Dataset(
        *train_test_split(
            wold.df[['value', 'borrowing_score']],
            wold.df.borrowing_score,
            test_size=test_size,
            random_state=seed,
        )
    )

    model = Markov(data=dataset.X_train)
    evaluate(model, dataset)

if __name__ == '__main__':
    cli()
