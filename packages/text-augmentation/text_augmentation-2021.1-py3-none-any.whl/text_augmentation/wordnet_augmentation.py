import random
import re
from random import choice

from digital_twin_distiller.concept import AbstractSubTask
from importlib_resources import files

random.seed(1)


class WordNetAugmentation(AbstractSubTask):
    def __init__(self):
        self.wordnet_path = files("resources") / "HuWN_final4.xml"
        self.synonyms_dict = {}
        self.stop_words = []
        self.wordnet_domains = ["geography", "quality", "law", "color", "time_period", "time period", "factotum"]
        self.protected_words = []

    def set_wordnet_domains(self, wordnet_domains):
        self.wordnet_domains = wordnet_domains

    def set_wordnet_path(self, wordnet_path):
        self.wordnet_path = wordnet_path

    def load_synonyms_dict(self):
        try:
            with open(self.wordnet_path, encoding="ISO-8859-2") as file:
                text = file.read()
        except FileNotFoundError:
            raise FileNotFoundError("HuWN_final4.xml is missing from resources, please run download_wordnet.py to download it!")
        synset_pat = re.compile(
            r"<SYNSET>.*?<DOMAIN>(?:{})</DOMAIN>.*?</SYNSET>".format("|".join(self.wordnet_domains))
        )
        literal_pat = re.compile(r"<LITERAL>(.+?)</LITERAL>")
        sense_subpat = re.compile(r"<SENSE>.*?</SENSE>|<LNOTE>.*?</LNOTE>")
        text = sense_subpat.sub("", text)
        all_synonyms = synset_pat.findall(text)
        all_synonyms = [literal_pat.findall(elem) for elem in all_synonyms]
        all_synonyms = [elem for elem in all_synonyms if len(elem) > 1]
        self.synonyms_dict = self.create_dict(all_synonyms)
        self.synonyms_set = set(self.synonyms_dict.keys())

    @staticmethod
    def create_dict(syn_lst):
        ret_dict = {}
        for elem in syn_lst:
            for syn in elem:
                ret_dict[syn] = list(set(elem) - {syn})
        return ret_dict

    def synonym_replacement(self, words: list, n: int = None, protected_words: list = None):
        """
        Replaces synonyms in list of words atmost in n cases. NOTE: If the there isn't any synonym in the given
        document, there won't be any changes made.
        :param words: list of words to be augmented
        :param n: number of words to be replaced, defaults to 10% of document
        :param protected_words: list of words that cannot be changed
        :return: augmented text output, list of strings
        """
        if not protected_words:
            protected_words = self.protected_words
        if n is None:
            n = int(len(words) * 0.1)
        words_intersection, can_augment = self._get_potential_words(words, protected_words, n)
        if not can_augment:
            return words
        new_words = words.copy()

        random.shuffle(words_intersection)
        num_replaced = 0
        # replacing atmost n pieces of words from the intersection.
        for random_word in words_intersection:
            synonyms = self.synonyms_dict.get(random_word)
            if len(synonyms) >= 1:
                synonym = choice(list(synonyms))
                new_words = [synonym if word == random_word else word for word in new_words]
                # print("replaced", random_word, "with", synonym)
                num_replaced += 1
            if num_replaced >= n:  # only replace up to n words
                break

        # in case the synonym consists of multiple words, this ensures that the tokens do not contain space character
        sentence = " ".join(new_words)
        new_words = sentence.split(" ")

        return new_words

    def _get_potential_words(self, words, protected_words, n):
        can_augment = True
        # only deal with words that are in the synonyms set, but not in the protected words
        words_intersection = list(set(words).intersection(self.synonyms_set).difference(set(protected_words)))
        # checking if any synonyms in the given document
        if not self.synonyms_set or not words_intersection:
            print("No synonyms found. Returning original document.")
            can_augment = False

        if len(words_intersection) < n:
            print(
                "The number of found synonyms: {} is less than the required count: {}.".format(
                    len(words_intersection), n
                )
            )
        return words_intersection, can_augment

    def synonym_insertion(self, words: list, n: int = None, protected_words: list = None):
        """
        Randomly insert atmost n synonyms to random position in text. First the number of synonyms
        :param words: list of words to be augmented
        :param n: number of words to be replaced, defaults to 10% of document
        :param protected_words: list of words that cannot be used during synonym finding
        :return: augmented text output, list of strings
        """
        if n is None:
            n = int(len(words) * 0.1)
        if not protected_words:
            protected_words = self.protected_words
        words_intersection, can_augment = self._get_potential_words(words, protected_words, n)
        if not can_augment:
            return words
        new_words = words.copy()
        random.shuffle(words_intersection)
        num_replaced = 0
        for random_word in words_intersection:
            synonyms = self.synonyms_dict.get(random_word)
            if len(synonyms) >= 1:
                synonym = choice(list(synonyms))
                random_index = random.randint(0, len(new_words) - 1)
                new_words.insert(random_index, synonym)
                # print("replaced", random_word, "with", synonym)
                num_replaced += 1
            if num_replaced >= n:  # only replace up to n words
                break

        # this is stupid but it is needed
        sentence = " ".join(new_words)
        new_words = sentence.split(" ")

        return new_words

    def run(self, words, n=None, protected_words=None):
        if not protected_words:
            protected_words = self.protected_words
        return self.synonym_replacement(words, n, protected_words=protected_words)
