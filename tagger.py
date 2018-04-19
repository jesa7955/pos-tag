# -*- coding: UTF-8 -*-

from processor import Processor
from collections import defaultdict
from tqdm import tqdm
import random
import json


class Tagger:
    def __init__(self, file_name, times=1, random=True, prefix=''):
        self.context = {}
        self.__reset_context__()
        self.times = times
        self.random = random
        print(prefix + "のモデルを準備中")
        self.model = Processor(file_name, prefix)
        if self.model.model_exist():
            print("モデルを読み込んだ")
        else:
            print("モデルをトレーニング中")
            self.__perceptron__()

    def __reset_context__(self):
        self.context['pp_tag'] = 'kashiramae'
        self.context['p_tag'] = 'kashira'

    def __predict__(self, features):
        scores = defaultdict(float)
        for feature in features:
            if feature in self.model.weights:
                weights = self.model.weights[feature]
                for tag, weight in weights.items():
                    scores[tag] += weight * 1.0
        if len(scores) == 0:
            guess = random.sample(self.model.tags, 1)[0]
        else:
            guess = max(scores.items(), key=lambda x: x[1])[0]
        return guess

    def __perceptron__(self):
        length = len(self.model.raws)
        T = length * self.times
        for t in tqdm(range(T)):
            if self.random:
                word, info = random.choice(self.model.raws)
            else:
                word, info = self.model.raws[t%length]
            features = self.__construct_feature__(word, info)
            for feature in features:
                self.__construct_vector__(self.model.weights, feature)
                self.__construct_vector__(self.model.accumulators, feature)
            guess = self.__predict__(features)
            correct = info['tag']
            if guess != correct:
                for feature in features:
                    self.model.weights[feature][correct] += 1.0
                    self.model.weights[feature][guess] -= 1.0
                    self.model.accumulators[feature][correct] += t * 1.0 / float(T)
                    self.model.accumulators[feature][guess] -= t * 1.0 / float(T)
        for feature, weights in self.model.weights.items():
            for tag in self.model.tags:
                weights[tag] -= self.model.accumulators[feature][tag]
        self.model.save_data()

    def __construct_vector__(self, vector, feature_name):
        if feature_name not in vector:
            vector[feature_name] = defaultdict(float)

    def __is_number__(self, word):
        try:
            float(word)
            return True
        except ValueError:
            return False

    def __is_capitalized__(self, word):
        return any(
            list(map(lambda char: char == char.capitalized(), list(word))))

    def __construct_feature__(self, word, info, context=False):
        def add(name, *args):
            features.add('+'.join((name, ) + tuple(args)))

        features = set()
        add('bias')
        add('n word', word)
        add('n prefix2', word[:2])
        add('n prefix3', word[:3])
        add('n suffix', word[-3:])
        add('n-1 suffix', info['p'][0][-3:])
        add('n+1 suffix', info['n'][0][-3:])
        add('n-1 word', info['p'][0])
        add('n+1 word', info['n'][0])
        add('n-2 word', info['pp'][0])
        add('n+2 word', info['nn'][0])
        if context: # When verifying the trained model, use context
            add('n-1 tag', self.context['p_tag'])
            add('n-2 tag', self.context['pp_tag'])
        else: # When traning a new model, use inforamtion from table
            add('n-1 tag', info['p'][1])
            add('n-2 tag', info['pp'][1])
        return features

    def benchmark(self, data):
        correct = 0
        print("結果を検証中")
        for index in tqdm(range(len(data.raws))):
            word, info = data.raws[index]
            guess = self.predict(word, info)
            if guess == info['tag']:
                correct += 1
        print("正解率は{0:.2f}%です".format(100.0 * correct/len(data.raws)))

    def predict(self, word, info):
        if word in self.model.unambiguous:
            guess = self.model.unambiguous[word]
        elif self.__is_number__(word):
            guess =  'CD'
        else:
            features = self.__construct_feature__(word, info, True)
            guess = self.__predict__(features)
        # Maintain the context variable
        if info['n'][0] == 'owari': # Reset the context values when taggin a new line
            self.__reset_context__()
        else: # Update context
            self.context['pp_tag'] = self.context['p_tag']
            self.context['p_tag'] = guess
        return guess
