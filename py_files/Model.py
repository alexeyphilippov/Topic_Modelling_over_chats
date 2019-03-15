from gensim import corpora
from gensim import models
from pymystem3 import Mystem

import nltk


class Model:

    def __init__(self, data: list, stop_words: list, ngr: int = None, num_topics: int = 20,
                 num_passes: int = 20) -> None:

        self._texts = self._get_texts(data, stop_words, ngr)
        self._dictionary = corpora.Dictionary(self._texts)
        self._corpus = [self._dictionary.doc2bow(text) for text in self._texts]
        print('3')
        self._ldamodel = models.ldamodel.LdaModel(self._corpus, id2word=self._dictionary, num_topics=num_topics,
                                                  passes=num_passes)

    def _get_texts(self, data: list, stop_words: list, ngr: int = None) -> list:

        texts = []
        for sen in data:
            text = []
            bi_text = []
            mystem = Mystem()

            for tok in mystem.lemmatize(sen):
                if tok not in stop_words and len(tok) > 3:
                    text.append(tok)

            if ngr is not None:
                for ins in nltk.ngrams(text, ngr):
                    bi_text.append(' '.join(ins))

            if text:
                texts.append(text + bi_text)

        return texts

    def get_model(self):
        return self._ldamodel

    def get_corpus(self):
        return self._corpus

    def get_dictionary(self):
        return self._dictionary

    def save_model(self):
        self._ldamodel.save(
            '/Users/aleksejfilippov/Desktop/Python_projects/topic_model/trained_models/model1/ldamodel1')
        self._dictionary.save('/Users/aleksejfilippov/Desktop/Python_projects/topic_model/trained_models/model1/dict1')


