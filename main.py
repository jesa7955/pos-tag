#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
from tagger import Tagger
from processor import Processor
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='Part-of-Speech Tagging.')
    parser.add_argument('--read', '-r',  action='store_true',
                       help='open this switch when you want to train a new model')
    parser.add_argument('--suffix', '-s',  type=str, default='',
                       help='specify suffix of files which will be used to store model')
    args = parser.parse_args()
    tagger = Tagger('data/wsj00-18.pos', args.read, args.suffix)
    test_data = Processor('data/wsj19-21.pos')
    tagger.benchmark(test_data)

if __name__ == '__main__':
    main()
