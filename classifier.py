#!/usr/bin/python3

class Tager:
    """
    """

    def __init__(self, classifier, unambiguous_set):
        self.__classifier__ = classifier
        self.__unambiguous__ = unambiguous_set

    def __is_number__(self, word):
        try:
            float(word)
            return True
        except ValueError:
            return False

    def tag(self, word):
        if word in unambiguous_set:
            return unambiguous_set[word]
        if self.__is_number__(word):
            return 'CD'
