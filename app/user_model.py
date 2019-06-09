import math
from collections import defaultdict


class WilsonModel:
    def __init__(self, vocab, start_level=1):
        self.vocab = vocab
        self.level = start_level
        self.word_to_tries = {word: 0 for word in vocab}
        self.word_to_success = {word: 0 for word in vocab}

    def update(self, read, highlighted):
        #remove duplicate words in read
        for word in read:
            self.word_to_tries[word] += 1
            if word not in highlighted:
                self.word_to_success[word] += 1

    def score(self, word):
        n = self.word_to_tries[word]
        if n == 0:
            return 0

        success = self.word_to_success[word]
        fail = n - success
        z = 1.96    # confidence interval of 0.95
        phat = success / n

        # lower bound of wilson score
        return (phat + (z**2 / 2*n) - z*((phat * (1-phat) + z**2 / 4*n) / n)**(0.5)) / (1 + z**2 / n)


class EloModel:
    def __init__(self, start_level=1, k=0.5):
        self.level = start_level
        self.k = k

    def update(self, read, highlighted):
        #remove duplicate words in read
        expected = 0
        actual = 0
        for word in read:
            word_level = get_word_level(word)
            expected += 1 / (1 + 10**((word_level - self.level)/400))
            if word not in highlighted:
                actual += 1
            else:
                actual -= 1

        self.level += self.k * (actual - expected)
        self.level = min(self.level, 1)

    def score(self):
        return self.level


if __name__ == '__main__':
    vocab = ['hello' , 'hi', 'goodbye']
    model = WilsonModel(vocab)
    model.update(['hello', 'hello', 'hello'],
                 [])
    for word in vocab:
        print(model.wilson_score(word))

