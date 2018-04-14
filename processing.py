#!/usr/bin/python3


class PreProcessor:
    """
    This is used to read file in and make some process we will
    need in next procedure.
    """

    def __init__(self, file_name='data/wsj00-18.pos'):
        self.__data_file__ = file_name

    def get_unambiguous(self) -> dict:
        learn_data = open(self.__data_file__)
        data_set = {}

        for line in learn_data:
            for item in line.split():
                slices = item.split('/')
                word = '/'.join(slices[:-1])
                tag = slices[-1]
                if word in data_set:
                    if tag not in data_set[word]:
                        data_set[word].add(tag)
                else:
                    data_set[word] = set()
                    data_set[word].add(tag)
        learn_data.close()

        items = list(data_set.items())
        for word, tag in items:
            if len(tag) == 1:
                data[word] = tag.pop()
            else:
                data.pop(word)
        return data_set
