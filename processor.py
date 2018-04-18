class Processor:
    """
    This is used to read file in and make some process we will
    need in next procedure.
    """

    def __init__(self, file_name):
        self.raws = []
        self.tags = {}
        self.words = {}
        self.unambiguous = {}
        self.weights = {}
        self.accumulators = {}
        self.file_name = file_name
        self.__process__()

    def __process__(self):
        def seperate(corpus):
            index = corpus.rfind('/')
            word = corpus[:index]
            tag = corpus[index + 1:]
            return (word, tag)

        tag_index = 0
        data_set = {}
        with open(self.file_name) as raw_file:
            for line in raw_file:
                sentence = [seperate(corpus) for corpus in line.split()]
                sentence.insert(0, ('kashira', 'kashira'))
                sentence.insert(0, ('kashiramae', 'kashiramae'))
                sentence.append(('owari', 'owari'))
                sentence.append(('owariato', 'owariato'))
                for index, (word, tag) in enumerate(sentence[2:-2]):
                    self.raws.append((word, {
                        'tag': tag,
                        'pp': sentence[index],
                        'p': sentence[index+1],
                        'n': sentence[index+3],
                        'nn': sentence[index+4]
                    }))
                    if word in data_set:
                        if tag not in data_set[word]:
                            data_set[word][tag] = 1
                        else:
                            data_set[word][tag] += 1
                    else:
                        data_set[word] = {}
                        data_set[word][tag] = 1
                    if tag not in self.tags:
                        self.tags[tag] = tag_index
                        tag_index += 1
        for index, (word, counter) in enumerate(data_set.items()):
            if len(counter) == 1 and list(counter.values())[0] >= 20:
                self.unambiguous[word] = list(counter.keys())[0]
            self.words[word] = index
