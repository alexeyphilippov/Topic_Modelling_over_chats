from py_files.Model import Model


PATH_FOR_STORED_MESSAGES = '/Users/aleksejfilippov/Desktop/Python_projects/data_for_topic model/data_messages.txt'
PATH_FOR_STOP_WORDS = '/Users/aleksejfilippov/Desktop/Python_projects/data_for_topic model/stop_words.txt'

file = open(PATH_FOR_STORED_MESSAGES, 'r')
file.close()

# get data with a lot of messages in russian
file = open(PATH_FOR_STORED_MESSAGES, 'r')
data_rus = []
for line in file.readlines():
    if 20 < len(line) < 100:
        data_rus.append(line.lower())
file.close()

# get all stop words in russian
file = open(PATH_FOR_STOP_WORDS, 'r')
stop_words = [x[:-1] for x in file.readlines()]
file.close()

# update
extra_stop_words = ['?. ', '\n', '"\n', ': ', '\': "\'', ') ', '! ', ')\n', '\://', '', '', '', '', '', '', '']
numbers = [str(i) for i in range(100)]
stop_words.extend(extra_stop_words)
stop_words.extend(numbers)


model_c = Model(data_rus, stop_words)
model = model_c.get_model()

