# -*- coding: utf-8 -*-
import random
import copy

class Markov():
    def __init__(self, input_data=''):
        self.word_chain = {}
        self.phrase_chain = {}
        self.input_data = input_data

    def create_word_chain(self):
        input_data = copy.deepcopy(self.input_data)
        input_data = ' '.join([line.strip() for line in input_data.strip().splitlines()])
        input_data = input_data.lower()
        input_data = input_data.split(' ')
        input_data = self.separate_periods(input_data)
        for i in range(len(input_data)-1):
            self.add_to_chain(input_data[i], input_data[i+1])

    def add_to_chain(self, curr_word, next_word):
        if self.word_chain.__contains__(curr_word):
            if self.word_chain[curr_word].__contains__(next_word):
                self.word_chain[curr_word][next_word] += 1
            else:
                self.word_chain[curr_word][next_word] = 1
        else:
            self.word_chain[curr_word] = {next_word: 1}

    def separate_periods(self, input_data):
        length = len(input_data)
        i = 0
        while i < length:
            word = input_data[i]
            if len(word) > 1 and word[-1] == ".":
                input_data[i] = word[:len(word)-1]
                input_data.insert(i+1, ".")
                length += 1
            i += 1
        return input_data

    def create_response(self, max_len=1000, curr_word=''):
        if curr_word == "":
            curr_word = "."
            while curr_word == ".":
                curr_word = random.choice(self.word_chain.keys())
        return_string = curr_word + " "
        while self.count_words(return_string) < 20 and not return_string.endswith(". "):
            curr_word = self.choose_next_word(self.word_chain[curr_word])
            return_string += curr_word + " "
            if return_string.endswith(". "):
                return_string = return_string[:len(return_string)-3] + "."
                break
        return return_string

    def choose_next_word(self, choices):
        next_words = []
        for word in choices.keys():
            for i in range(choices[word]):
                next_words.append(word)
        return random.choice(next_words)

    def count_words(self, string):
        return len(string.split(" "))

if __name__=='__main__':
    markov = Markov()
    markov.create_word_chain("Donald Trump was 100% right to fire James Comey. Why in the world didn’t Barack Obama fire this guy (Comey). Wow, the highest rated (by far) morning show, foxandfriends, is on the Front Lawn of the White House. Maybe I’ll have to take an unannounced trip down to see them. U.S.A. Jobs numbers are the BEST in 44 years. If my opponent (the Democrats) had won the election, they would have raised taxes substantially and increased regulations the economy, and jobs, would have been a disaster. Thank you for all of the compliments on getting the World Cup to come to the U.S.A., Mexico and Canada. I worked hard on this, along with a Great Team of talented people. We never fail, and it will be a great World Cup! A special thanks to Bob Kraft for excellent advice. The IG Report is a total disaster for Comey, his minions and sadly, the FBI. Comey will now officially go down as the worst leader, by far, in the history of the FBI. I did a great service to the people in firing him. Good Instincts. Christopher Wray will bring it proudly back.")
    print(markov.word_chain)
    print(markov.create_response(max_len=1000))
