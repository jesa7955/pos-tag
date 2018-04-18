from processor import Processor
from collections import defaultdict
from tqdm import tqdm
import random


class Tagger:
    def __init__(self, train_file='data/wsj00-18.pos'):
        self.model = Processor(train_file)
        self.__perceptron__()

    def construct_feature(self, word, info) -> set:
        def add(name, *args):
            features.add('+'.join((name, ) + tuple(args)))

        features = set()
        add('bias')
        add('n word', word)
        add('n-1 word', info['p'][0])
        add('n+1 word', info['n'][0])
        add('n-2 word', info['pp'][0])
        add('n+2 word', info['nn'][0])
        return features

    def predict(self, word, info) -> str:
        if word in self.model.unambiguous:
            return self.model.unambiguous[word]
        if self.__is_number__(word):
            return 'CD'
        features = self.construct_feature(word, info)
        return self.__predict__(features)

    def __predict__(self, features) -> str:
        scores = defaultdict(int)
        for feature in features:
            if feature in self.model.weights:
                weights = self.model.weights[feature]
                for tag, weight in weights.items():
                    scores[tag] += weight * 1.0
        return max(scores.items(), key=lambda x: x[1])[0]

    def __perceptron__(self):
        T = len(self.model.raws)
        for t in tqdm(range(len(self.model.raws))):
            #word, info = self.model.raws[t]
            word, info = random.choice(self.model.raws)
            features = self.construct_feature(word, info)
            for feature in features:
                self.__construct_vector__(self.model.weights, feature)
                self.__construct_vector__(self.model.accumulators, feature)
            guess = self.__predict__(features)
            correct = info['tag']
            if guess != correct:
                for feature in features:
                    self.model.weights[feature][correct] += 1.0
                    self.model.weights[feature][guess] -= 1.0
                    self.model.accumulators[feature][correct] += t / T * 1.0
                    self.model.accumulators[feature][guess] += -t / T * 1.0
        for feature, weights in self.model.weights.items():
            for tag in self.model.tags:
                weights[tag] -= self.model.accumulators[feature][tag]

    def __construct_vector__(self, vector, feature_name):
        if feature_name not in vector:
            vector[feature_name] = {}
            for tag in self.model.tags:
                vector[feature_name][tag] = 0.0

    def __is_number__(self, word) -> bool:
        try:
            float(word)
            return True
        except ValueError:
            return False

    def __is_capitalized__(self, word) -> bool:
        return any(
            list(map(lambda char: char == char.capitalized(), list(word))))
