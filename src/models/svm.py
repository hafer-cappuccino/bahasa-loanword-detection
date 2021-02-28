from typing import List

import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC


class SVM:

    def __init__(self, X: np.array, y: np.array):
        """
        A language model that uses a bag of sounds as features.
        These bag of sounds data is one-hot encoded.

        X, y and should be the training set.

        :param X: the input vector with a shape of (num_samples, num_features).
        :param y: the output vector with a shape of (num_samples,). The output
            is either a 1 ("loanword") or 0.
        """
        self.X, self.y = X, y
        self.classifier = LinearSVC()
        self.classifier.fit(self.X, self.y)

    def predict(self, X: np.array) -> List[str]:
        """
        Given a list of samples, return a list of predictions.

        `X` here should be the test set.

        :param X: the input vector with a shape of (num_samples, num_features).
        :param y: the output vector with a shape of (num_samples,).

        :returns: a list of classifications.
        """
        return self.classifier.predict(X)
