from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers
from keras.models import load_model
import pickle
import cleanup

model = load_model('embedding_LSTM.h5')
tokenizer = pickle.load(open('tokenizer.pickle', 'rb'))

index_to_cat = {0: 'math.MP', 1: 'math.CO', 2: 'math.AG', 3: 'math.PR', 4: 'math.AP', 5: 'math.DG', 6: 'math.IT', 7: 'math.NT', 8: 'math.DS', 9: 'math.OC', 10: 'math.FA', 11: 'math.RT', 12: 'math.NA', 13: 'math.GT', 14: 'math.QA', 15: 'math.CA', 16: 'math.GR', 17: 'math.ST', 18: 'math.RA', 19: 'math.CV', 20: 'math.AT', 21: 'math.OA', 22: 'math.AC', 23: 'math.LO', 24: 'math.MG', 25: 'math.SG', 26: 'math.SP', 27: 'math.CT', 28: 'math.KT', 29: 'math.GN', 30: 'math.GM', 31: 'math.HO'}

cat_to_index = {'math.MP': 0, 'math.CO': 1, 'math.AG': 2, 'math.PR': 3, 'math.AP': 4, 'math.DG': 5, 'math.IT': 6, 'math.NT': 7, 'math.DS': 8, 'math.OC': 9, 'math.FA': 10, 'math.RT': 11, 'math.NA': 12, 'math.GT': 13, 'math.QA': 14, 'math.CA': 15, 'math.GR': 16, 'math.ST': 17, 'math.RA': 18, 'math.CV': 19, 'math.AT': 20, 'math.OA': 21, 'math.AC': 22, 'math.LO': 23, 'math.MG': 24, 'math.SG': 25, 'math.SP': 26, 'math.CT': 27, 'math.KT': 28, 'math.GN': 29, 'math.GM': 30, 'math.HO': 31}


def abstract_category_predict(text, model=model, tokenizer=tokenizer):
    clean = cleanup.cleanup(stem_on=True)
    X = [clean.transform(text)]
    X_tt = tokenizer.texts_to_sequences(X)
    maxlen = 200
    X = pad_sequences(X_tt, maxlen=maxlen)
    y_pred = model.predict(X)
    y_pred2 = (y_pred > 0.5).astype(int)
    y_pred2 = y_pred2[0]
    Ans = []
    for i in range(len(index_to_cat)):
        if y_pred2[i] == 1:
            Ans += [index_to_cat[i]]
    return Ans

####example
#print(predict("Using schubert variety to construct degenration of MV cycles and it results in represnetation of simisimple lie algebra "))
