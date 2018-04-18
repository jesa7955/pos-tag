from processor import Processor
from collections import defaultdict
from tqdm import tqdm
import random


class Tagger:
    def __init__(self, train_file='data/wsj00-18.pos'):
        self.model = Processor(train_file)
        self.context = {}
        self.__reset_context__()
        self.__perceptron__()

    def construct_feature(self, word, info, context=None):
        def add(name, *args):
            features.add('+'.join((name, ) + tuple(args)))

        features = set()
        add('bias')
        add('n word', word)
        add('n prefix2', word[:2])
        add('n prefix3', word[:3])
        add('n suffix3', word[-3:])
        add('n-1 word', info['p'][0])
        add('n+1 word', info['n'][0])
        add('n-2 word', info['pp'][0])
        add('n+2 word', info['nn'][0])
        #if not context: # When traning a new model, use inforamtion from table
        #    add('n-1 tag', info['p'][1])
        #    add('n-2 tag', info['pp'][1])
        #else: # When verifying the trained model, use context
        #    add('n-1 tag', context['p_tag'])
        #    add('n-2 tag', context['pp_tag'])
        return features

    def predict(self, word, info):
        if word in self.model.unambiguous:
            guess = self.model.unambiguous[word]
        elif self.__is_number__(word):
            guess =  'CD'
        else:
            features = self.construct_feature(word, info, self.context)
            guess = self.__predict__(features)
            #if info['n'][0] == 'owari': # Reset the context values when taggin a new line
            #    self.context['p_tag'] = 'kashira'
            #    self.context['pp_tag'] = 'kashiramae'
            #else: # Update context
            #    self.context['pp_tag'] = self.context['p_tag']
            #    self.context['p_tag'] = guess
        return guess

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
        return max(scores.items(), key=lambda x: x[1])[0]

    def __perceptron__(self):
        length = len(self.model.raws)
        T = length * 5
        for t in tqdm(range(T)):
            word, info = self.model.raws[t%length]
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
                    self.model.accumulators[feature][correct] += t * 1.0 / float(T)
                    self.model.accumulators[feature][guess] -= t * 1.0 / float(T)
        for feature, weights in self.model.weights.items():
            for tag in self.model.tags:
                weights[tag] -= self.model.accumulators[feature][tag]

    def __construct_vector__(self, vector, feature_name):
        if feature_name not in vector:
            vector[feature_name] = {}
            for tag in self.model.tags:
                vector[feature_name][tag] = 0.0

    def __is_number__(self, word):
        try:
            float(word)
            return True
        except ValueError:
            return False

    def __is_capitalized__(self, word):
        return any(
            list(map(lambda char: char == char.capitalized(), list(word))))
