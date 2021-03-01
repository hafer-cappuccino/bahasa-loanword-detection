import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from src.data.wold import WOLD


class NN:

    def __init__(
            self,
            train_set,
            test_set,
            n_hidden: int = 32,
    ):
        self.df = WOLD().df
        self.train_set = train_set.reset_index(drop=True)
        self.test_set = test_set.reset_index(drop=True)

        self.all_letters = []

        for l in self.df.segments:
            for s in l:
                if s not in self.all_letters:
                    self.all_letters.append(s)

        self.best_model = GRU(
            len(self.all_letters),
            n_hidden,
            2,  # this is a binary classification language task
        )

        self.best_model.load_state_dict(
            torch.load('src/models/gru/best_model_state.pt')
        )

    def predict(self, X):
        X = X.reset_index(drop=True)
        pred = []

        for i in range(len(X)):
            _, _, _, line_tensor = self.testing_sample(X, i)
            output = self.evaluate(line_tensor)
            guess = self.category_from_output(output)
            pred.append(guess)
        return pred

    def predict_word(self, word):
        line_tensor = self.char_tensor(word)
        output = self.evaluate(line_tensor)
        return self.category_from_output(output)

    def evaluate(self, line_tensor):
        hidden = self.best_model.initHidden()

        for i in range(line_tensor.size()[0]):
            output, hidden = self.best_model(line_tensor[i], hidden)

        return output

    def category_from_output(self, output):
        top_n, top_i = output.topk(1)
        category_i = top_i[0].item()
        return category_i

    def char_tensor(self, list_of_strings):
        tensor = torch.zeros(len(list_of_strings)).long()
        for c in range(len(list_of_strings)):
            tensor[c] = self.all_letters.index(list_of_strings[c])
        return Variable(tensor)

    def testing_sample(self, data, i):
        self.all_categories = [0, 1]
        category = int(data.borrowing_score[i])
        line = data.segments[i]
        category_tensor = torch.tensor([self.all_categories.index(category)], dtype=torch.long)
        line_tensor = self.char_tensor(line)

        return category, line, category_tensor, line_tensor

class GRU(nn.Module):
    def __init__(self, n_characters_in, hidden_size, n_characters_out, n_layers=1, batch_size=1):
        super(GRU, self).__init__()
        self.n_characters_in = n_characters_in
        self.n_characters_out = n_characters_out
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.batch_size = batch_size

        self.encoder = nn.Embedding(num_embeddings=self.n_characters_in,
                                    embedding_dim=self.hidden_size)
        self.gru = nn.GRU(input_size=self.hidden_size,
                          hidden_size=self.hidden_size,
                          num_layers=self.n_layers,
                          dropout=0.2)
        self.decoder = nn.Linear(self.hidden_size, n_characters_out)

    def forward(self, input_char, hidden):
        encoded = self.encoder(input_char)
        encoded.unsqueeze_(0)
        encoded.unsqueeze_(0)
        output, hidden = self.gru(encoded, hidden)
        output = self.decoder(output.view(1, -1))
        return output, hidden

    def initHidden(self):
        return Variable(torch.zeros(self.n_layers, self.batch_size, self.hidden_size))
