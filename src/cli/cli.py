import click
import warnings

from sklearn.model_selection import train_test_split

from src.cli.utils import evaluate, SEED_OPTIONS, TEST_SIZE_OPTIONS
from src.data.models import Dataset
from src.data.wold import WOLD
from src.models.gru.nn import NN
from src.models.markov import Markov
from src.models.svm import SVM


warnings.filterwarnings('ignore', category=UserWarning)
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

    model = Markov(X=dataset.X_train)
    evaluate(model, dataset)


@cli.command(name='gru')
@click.option('--test-size', **TEST_SIZE_OPTIONS)
@click.option('--seed', **SEED_OPTIONS)
@click.option(
    '--n-hidden',
    default=32,
    type=int,
    help='Number of features in a hidden state.'
)
def rnn(test_size, seed, n_hidden):
    dataset = Dataset(
        *train_test_split(
            wold.df,
            wold.df.borrowing_score,
            test_size=test_size,
            random_state=seed,
        )
    )
    train_set, test_set = train_test_split(
        wold.df,
        test_size=test_size,
        random_state=seed,
    )

    nn = NN(train_set, test_set, n_hidden)
    evaluate(nn, dataset)


@cli.command(name='all')
@click.option('--test-size', **TEST_SIZE_OPTIONS)
@click.option('--seed', **SEED_OPTIONS)
@click.pass_context
def all(ctx, test_size, seed):
    ctx.forward(svm)
    ctx.forward(markov)
    ctx.forward(rnn)


if __name__ == '__main__':
    cli()
