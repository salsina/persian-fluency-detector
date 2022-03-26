class PersianSyllableCounter:
    def __init__(self):
        self.vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
        self.persian_phonetics_dictionary = {}
        self.persian_syllables_dictionary = {}
        self.persian_syllables_basedOnLength_dictionary = {}
        self.initialize_dictionaries()

    def count_syllables_in_word(self, word):
        ans = 0
        for letter in word:
            if letter in self.vowels:
                ans += 1
        return ans

    def initialize_dictionaries(self):
        f = open('persian_phonetics.txt', encoding="utf8") 
        lines = f.readlines()
        for line in lines:
            word, phonetic = line.split()
            self.persian_phonetics_dictionary[word] = phonetic
            word_syllables = self.count_syllables_in_word(phonetic)
            self.persian_syllables_dictionary[word] = word_syllables
            word_len = len(word)
            if word_len in self.persian_syllables_basedOnLength_dictionary:
                self.persian_syllables_basedOnLength_dictionary[word_len].append(word_syllables)
            else:
                self.persian_syllables_basedOnLength_dictionary[word_len] = [word_syllables]

        for word_len in self.persian_syllables_basedOnLength_dictionary.keys():
            lengths = self.persian_syllables_basedOnLength_dictionary[word_len]
            self.persian_syllables_basedOnLength_dictionary[word_len] = round(sum(lengths)/ len(lengths))

    def pridict_syllable(self, word):
        word_len = len(word)
        if word_len == 1:
            return 1
        if word_len in self.persian_syllables_basedOnLength_dictionary:
            return self.persian_syllables_basedOnLength_dictionary[word_len]
        return self.pridict_syllable(word[1:])

    def count_syllables_in_text(self, text):
        ans = 0
        splitted_text = text.split()
        for word in splitted_text:
            if word in self.persian_syllables_dictionary:
                ans += self.persian_syllables_dictionary[word]
            else:
                ans += self.pridict_syllable(word)
        return ans

# sample use
# text = 'امروز می خواهم بروم به پارک'
# psc = PersianSyllableCounter()
# print(psc.count_syllables_in_text(text))
# output is --> 10