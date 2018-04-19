# -*- coding: UTF-8 -*-

import json
import gzip
import os.path


class Processor:
    """
    This is used to read file in and make some process we will
    need in next procedure.
    """

    def __init__(self, file_name, prefix=''):
        def read_in(name):
            with gzip.open(self.__makename__(name), 'rb') as f:
                return json.load(f)

        self.raws = []
        self.tags = {}
        self.unambiguous = {}
        self.weights = {}
        self.accumulators = {}
        self.saves = set(['tags', 'unambiguous', 'weights'])
        self.file_name = file_name
        self.prefix = prefix
        self.__process__()
        if self.model_exist():
            self.tags = read_in('tags')
            self.unambiguous = read_in('unambiguous')
            self.weights = read_in('weights')

    def save_data(self):
        def save_to(name, obj):
            with gzip.open(self.__makename__(name), 'wb') as f:
                f.write(json.dumps(obj))

        save_to('tags', self.tags)
        save_to('unambiguous', self.unambiguous)
        save_to('weights', self.weights)

    def model_exist(self):
        return all(
            [os.path.isfile(self.__makename__(save)) for save in self.saves])

    def __makename__(self, name):
        return 'data/' + self.prefix + '_' + name + '.gz'

    def __process__(self):
        def seperate(corpus):
            index = corpus.rfind('/')
            word = corpus[:index]
            tag = corpus[index + 1:]
            return (word, tag)

        data_set = {}
        with open(self.file_name) as raw_file:
            for line in raw_file:
                sentence = [seperate(corpus) for corpus in line.split()]
                sentence.insert(0, ('kashira', 'kashira'))
                sentence.insert(0, ('kashiramae', 'kashiramae'))
                sentence.append(('owari', 'owari'))
                sentence.append(('owariato', 'owariato'))
                for index, (word, tag) in enumerate(sentence[2:-2]):
                    self.raws.append([
                        word, {
                            'tag': tag,
                            'pp': sentence[index],
                            'p': sentence[index + 1],
                            'n': sentence[index + 3],
                            'nn': sentence[index + 4]
                        }
                    ])
                    if word in data_set:
                        if tag not in data_set[word]:
                            data_set[word][tag] = 1
                        else:
                            data_set[word][tag] += 1
                    else:
                        data_set[word] = {}
                        data_set[word][tag] = 1
                    self.tags[tag] = ''
        for index, (word, counter) in enumerate(data_set.items()):
            if len(counter) == 1 and list(counter.values())[0] >= 10:
                self.unambiguous[word] = list(counter.keys())[0]
