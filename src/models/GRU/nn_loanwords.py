import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class NN:

    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)

    def preprocess(self):
        new_dfseg = []

        for i in self.df.segments:
            new_dfseg.append(eval(i))

        self.df.segments = new_dfseg

        segments_prep = []

        for word in self.df.segments:
            phonemes = []
            for i in word:
                if 'A/a' == i or 'K/k' == i or 'M/m' == i or 'R/r' == i or 'S/s' == i or 'ss/s' == i:
                    i = i.replace(i, i[-1])
                    phonemes.append(i)
                if 'J/dʒ' in i:
                    i = i.replace(i, 'dʒ')
                    phonemes.append(i)
                else:
                    phonemes.append(i)

            segments_prep.append(phonemes)
        self.df.segments = segments_prep
        classes = []

        for s in self.df.borrowing_score:
            if s == 1.0:
                classes.append(s)
            else:
                classes.append(0.0)
        self.df.borrowing_score = classes
        self.all_letters = []

        for l in self.df.segments:
            for s in l:
                if s not in self.all_letters:
                    self.all_letters.append(s)
        self.n_letters = len(self.all_letters)
        train_set, test_set = train_test_split(self.df, test_size=0.2, random_state=42)

        self.train_set = train_set.reset_index(drop=True)
        self.test_set = test_set.reset_index(drop=True)
        print("Preprocessing is done!")

    def load_model(self):
        n_hidden = 32
        n_classes = 2
        self.best_model = GRU(self.n_letters, n_hidden, n_classes)
        self.best_model.load_state_dict(torch.load('best_model_state.pt'))

    def predict_test(self):
        true = []
        pred = []

        n_confusion = len(self.test_set)
        for i in range(n_confusion):
            category, line, category_tensor, line_tensor = self.testing_sample(self.test_set, i)
            output = self.evaluate(line_tensor)
            guess = self.category_from_output(output)
            true.append(category)
            pred.append(guess)
        print("All predictions are done!")
        return true, pred

    def predict(self, word):

        line_tensor = self.char_tensor(word)

        output = self.evaluate(line_tensor)
        guess = self.category_from_output(output)
        return guess

    def report(self, true, pred):
        target_names = ['class 0', 'class 1']
        print(classification_report(true, pred, target_names=target_names))


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