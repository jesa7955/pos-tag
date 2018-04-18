#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tagger import Tagger
from processor import Processor
from tqdm import tqdm

def benchmark(tagger, test_data):
    correct = 0
    print("結果を検証中")
    for index in tqdm(range(len(test_data))):
        word, info = test_data[index]
        guess = tagger.predict(word, info)
        if guess == info['tag']:
            correct += 1
    print("正解率は{0}%です".format(100.0 * correct/len(test_data)))

def main():
    print("モデルをトレーニング中")
    tagger = Tagger('data/wsj00-18.pos')
    test_data = Processor('data/wsj19-21.pos')
    benchmark(tagger, test_data.raws)

if __name__ == '__main__':
    main()
