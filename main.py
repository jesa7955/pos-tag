#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
from tagger import Tagger
from processor import Processor


def main():
    parser = argparse.ArgumentParser(description='Part-of-Speech Tagging.')
    parser.add_argument(
        '--prefix',
        '-p',
        type=str,
        default='',
        help='specify prefix of files which will be used to store model')
    parser.add_argument(
        '--times', '-t', type=int, default=1, help='specify iteration times')
    parser.add_argument(
        '--all',
        '-a',
        action='store_true',
        help='without this switch, model will be trained by random sampled data'
    )
    parser.add_argument(
        '--file', '-f', type=str, default='', help='specify test data file')
    parser.add_argument(
        '--save', '-s', action='store_true', help='enable this to save model file')
    args = parser.parse_args()
    tagger = Tagger('data/wsj00-18.pos', args.times, not args.all, args.save, args.prefix)
    test_data = Processor(args.file)
    tagger.benchmark(test_data)


if __name__ == '__main__':
    main()
