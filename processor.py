import json

class Processor:
    """
    This is used to read file in and make some process we will
    need in next procedure.
    """

    def __init__(self, file_name, read=False, suffix=''):
        def read_in(name):
            with open('data/'+self.suffix+'_'+name) as f:
                return json.load(f)

        self.raws = []
        self.tags = {}
        self.unambiguous = {}
        self.weights = {}
        self.accumulators = {}
        self.file_name = file_name
        self.suffix = suffix
        self.__process__()
        if read:
            self.tags = read_in('tags.json')
            self.unambiguous = read_in('unambiguous.json')
            self.weights = read_in('weights.json')

    def save_data(self):
        def save_to(name, obj):
            with open('data/'+self.suffix+'_'+name, 'w') as f:
                f.write(json.dumps(obj))

        save_to('tags.json', self.tags)
        save_to('unambiguous.json', self.unambiguous)
        save_to('weights.json', self.weights)

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
                    self.raws.append([word, {
                        'tag': tag,
                        'pp': sentence[index],
                        'p': sentence[index+1],
                        'n': sentence[index+3],
                        'nn': sentence[index+4]
                    }])
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
