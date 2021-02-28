from nn_loanwords import NN

nn = NN('indonesian_wordforms.csv')
nn.preprocess() # dataset preprocessing
nn.load_model() # loading pretrained model
true, pred = nn.predict_test()
nn.report(true, pred)
guess = nn.predict(['d', 'u', 'n', 'i', 'a'])
print(guess)