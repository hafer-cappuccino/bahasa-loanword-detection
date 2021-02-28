from typing import List

import pandas as pd
from nltk import lm
from nltk.util import ngrams
from nltk.lm.preprocessing import padded_everygram_pipeline


class Markov:
    
    def __init__(self, data: pd.DataFrame, order: int = 3, smoothing: float = 0.1):
        """
        A Markov model that calculates the entropies of a list of sounds.
        
        :param data: the DataFrame containing the segments and borrowing scores.
        :param order: the ngram order.
        :param smoothing: the smoothing discounting value.
        """
        self.order = order
        self.smoothing = smoothing
        
        loanwords = data[data.borrowing_score == 1].value
        nativewords = data[data.borrowing_score == 0].value
        
        loanwords_train, loanwords_vocab = padded_everygram_pipeline(self.order, loanwords)
        nativewords_train, nativewords_vocab = padded_everygram_pipeline(self.order, nativewords)
        
        self.loanwords_model = lm.KneserNeyInterpolated(
            order=self.order,
            discount=self.smoothing,
            vocabulary=lm.Vocabulary(loanwords_vocab, unk_cutoff=2)
        )
        
        self.nativewords_model = lm.KneserNeyInterpolated(
            order=self.order,
            discount=self.smoothing,
            vocabulary=lm.Vocabulary(nativewords_vocab, unk_cutoff=2)
        )
        
        self.loanwords_model.fit(loanwords_train)
        self.nativewords_model.fit(nativewords_train)

    def calculate_entropies(self, model, words) -> List[float]:
        """
        Given a list of words, calculate its entropies.
        
        :param words: a list of words segmented into a list of sounds.
            For example: [m, e, ŋ, g, o, s, o, ʔ]
        
        :returns: a list of entropies.
        """
        ngrams_ = [
            list(
                ngrams(word,
                       self.order,
                       pad_left=True,
                       pad_right=True,
                       left_pad_symbol='<s>',
                       right_pad_symbol='</s>'))
            for word in words
        ]
        return [model.entropy(sounds) for sounds in ngrams_]

    def predict(self, X: pd.DataFrame) -> List[int]:
        """
        Given a list of segments, predict whether the
        given segment is a loanword (1) or not (0).

        ref: Mattis 2020. Refactored for readability.

        :param X: the test set containing a column of value representing segments.

        :returns: a list of classifications.
        """
        native_entropies = self.calculate_entropies(self.nativewords_model, X.value)
        loan_entropies = self.calculate_entropies(self.loanwords_model, X.value)
        predictions = [
            0 if loan_entropy < native_entropy else 1
            for native_entropy, loan_entropy in zip(native_entropies, loan_entropies)
        ]
        return predictions
