from gensim import models
from gensim import corpora
from pymystem3 import Mystem
from wordcloud import WordCloud

import time

import numpy as np
import nltk

PATH_FOR_INCOMMING_MESSAGE = '../data_for_topic model/incoming_data.txt'
PATH_FOR_STOP_WORDS = '../data_for_topic model/stop_words.txt'
PATH_FOR_TRAINED_MODEL = '../trained_models/model1/model1'
PATH_FOR_TRAINED_DICTIONARY = '../trained_models/model1/dict1'

PATH_FOR_SAVING_PICTURE = './'

time0 = time.time()

model = models.ldamodel.LdaModel.load(PATH_FOR_TRAINED_MODEL)
dictionary = corpora.Dictionary.load(PATH_FOR_TRAINED_DICTIONARY)

time1 = time.time()
print("time for loading model and dictionary:", time1 - time0)

# get all stop words in russian
file = open(PATH_FOR_STOP_WORDS, 'r')
stop_words = [x[:-1] for x in file.readlines()]
file.close()

# update
extra_stop_words = ['?. ', '\n', '"\n', ': ', '\': "\'', ') ', '! ', ')\n', '\://', 'vk', '', '\')))\n\'', 'https',
                    'llhhll', 'https llhhll', 'ребята', 'знать', 'давать', 'делать', 'говорить', 'написать', 'идти',
                    'неделя', 'взять', 'кто-нибудь', 'кто-то', 'никто', 'свой', 'ничто', 'дело', 'саша', 'иван',
                    'что-то', 'сразу', 'пойти', 'сюда', 'оставаться', 'денис', 'любой', 'минута', 'видеть', 'пойти',
                    'саня', 'никита', 'интересно',
                    'поздно', 'начало', 'готовый', 'слово', 'ваня', 'короче', 'сходить', 'страница', 'откуда', 'пить',
                    'стол', 'евсеев', 'слышать',
                    'лежать', 'какой-то', 'нужный', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', '', '', '', ''
                    ]
numbers = [str(i) for i in range(100)]
stop_words.extend(extra_stop_words)
stop_words.extend(numbers)


def get_texts(data, ngr: int = None):
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

    return (texts)


def get_list_from_string(s: str) -> list:
    b = []
    tmp = s.split('\"')
    for i in range(len(tmp)):
        if i % 2 != 0:
            b.append(tmp[i])
    return b


def get_picture(message: str = None):  # if None it reads a message from file. Else you pass image as string
    if message is None:
        file = open(PATH_FOR_INCOMMING_MESSAGE, 'r')
        incom_data = [x[:-1] for x in file.readlines()]
        file.close()
    else:
        incom_data = [message]

    incom_texts = get_texts(incom_data)

    incom_corpus = [dictionary.doc2bow(text) for text in incom_texts]

    model.update(incom_corpus, passes=10)

    l = model.get_document_topics(incom_corpus[0])
    ll = [x[1] for x in l]
    topic_index = l[ll.index(np.max(ll))][0]

    topic_words = model.show_topics()[topic_index][1]

    wordcloud = WordCloud(width=400, height=200).generate(' '.join(get_list_from_string(topic_words)))
    return wordcloud.to_image()


time2 = time.time()
print('time for small staff:', time2 - time1)

tmp_message = 'Я просил скинуть мне те сканы с задачками от руки написанными но она сказала что все задачи есть в лекциях'

get_picture(tmp_message).save(PATH_FOR_SAVING_PICTURE + 'img.jpg')
print('time for updating model and saving picture:', time.time() - time2)
