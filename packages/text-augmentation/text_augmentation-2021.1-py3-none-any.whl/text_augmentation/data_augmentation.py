import random

import fasttext
import numpy as np
from digital_twin_distiller.concept import AbstractTask
from digital_twin_distiller.text_readers import JsonReader
from text_augmentation.wordnet_augmentation import WordNetAugmentation
from digital_twin_distiller.text_writers import JsonWriter
from gensim.models import FastText
from importlib_resources import files
from numpy.random import default_rng
from scipy.special import softmax
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

rng = default_rng()


class WordVectorAugmenter(AbstractTask):
    def __init__(self):
        self.vocabulary = None
        self.gensim_model = None
        self.fasttext_model = None
        self.topn_most_similar = 10
        self.most_similar_dict = {}
        self.original_text = None
        self.augmented_text = []
        self.protected_words = []

    def load_gensim_model(self, model_path):
        """
        Loads gensim FastText models. Only bin format is supported!
        :param fasttext_model_path: path for pretrained model in bin format is supported.
        :return:
        """
        self.gensim_model = FastText.load(model_path)

    def load_fasttext_model(self, fasttext_model_path):
        """
        Loads models from https://fasttext.cc/docs/en/crawl-vectors.html. Only bin format is supported!
        :param fasttext_model_path: path for pretrained model in bin format is supported.
        :return:
        """
        self.fasttext_model = fasttext.load_model(fasttext_model_path)

    def load_most_similar_dictionary(self, path_to_dict):
        """
        Load previously created dictionary containing most similar tokens from json file.
        :param path_to_dict:
        :return:
        """
        reader = JsonReader()
        loaded_json = reader.read(path_to_dict)
        self.most_similar_dict = loaded_json

    def save_most_similar_dictionary(self, path_to_dict):
        """
        Write most similar dictionary to json file.
        :param path_to_dict: path to save
        :return:
        """
        writer = JsonWriter()
        writer.write(self.most_similar_dict, path_to_dict)

    def build_vocab(self, text, **kwargs):
        """
        For faster processing, a vocabulary has to be created to perform similarity actions only once per token and not
        multiple times per document.
        :param text: list of strings, non-tokenized
        :param kwargs: parameters of a CountVectorizer object e.g. lowercase
        :return: None
        """
        if not kwargs:
            kwargs = {"lowercase": False}
        count_vect = CountVectorizer(**kwargs)
        count_vect.fit_transform(text)
        self.vocabulary = count_vect.vocabulary_

    def set_protected_words(self, protected_words_list: list):
        """
        Setter for protected word list.
        :param protected_words_list: list of words that cannot change during the text_augmentation process.
        :return: None
        """
        self.protected_words = protected_words_list

    def build_most_similar_dictionary(self, mode="gensim"):
        """
        Must be called when the vocabulary has been built.
        :return: A dictionary containing most similar finds. Keys are the members of the vocabulary,
        """
        if mode == "gensim":
            if not self.gensim_model:
                raise ValueError("Missing loaded gensim model. Please load gensim model!")
            for word in self.vocabulary:
                if word in self.gensim_model.wv.key_to_index:
                    if word not in self.most_similar_dict:
                        self.most_similar_dict[word] = self.gensim_model.wv.most_similar(
                            word, topn=self.topn_most_similar
                        )
                else:
                    self.most_similar_dict[word] = word
        elif mode == "fasttext":
            if not self.fasttext_model:
                raise ValueError("Missing loaded fasttext model. Please load fasttext model!")
            for word in tqdm(self.vocabulary):
                # using sets improves execution speed
                if not {word}.intersection(set(self.most_similar_dict.keys())):
                    # if word not in self.most_similar_dict:
                    top_finds = self.fasttext_model.get_nearest_neighbors(word, k=self.topn_most_similar)
                    # changing order of tuple elements
                    top_finds = [(elem[1], elem[0]) for elem in top_finds]

                    self.most_similar_dict[word] = top_finds
        else:
            raise ValueError("Wrong mode given! Please choose from 'gensim' or 'fasttext'!")

    def augment_text(self, text, augmented_size, picking_mode="weighted", protected_words=None, alpha=0.1):
        """
        Function for performing data text_augmentation.
        :param text: list of tokenized documents (list of lists) to be augmented
        :param augmented_size: the size of the augmented dataset (including the original input)
        :param picking_mode: The following modes are available now:
                weighted: Weighted picking from similar list based on softmax calculation.
                random: Uniformly distributed picking from similar list.
                first: Picks first element form similar list.
                wordnet: Performs wordnet synonym text_augmentation.
        :param protected_words: List of words that won't be changed during text_augmentation in any document.
        :return: the augmented dataset in tokenized form
        """
        if len(text) >= augmented_size:
            raise ValueError(
                "The augmented size criterion has been already met. Please increase the augmented size above the number"
                " of documents!"
            )
        if not protected_words:
            protected_words = self.protected_words
        self.original_text = text
        if picking_mode == "wordnet":
            wordnet = WordNetAugmentation()
            wordnet.load_synonyms_dict()
        for txt in text:
            self.augmented_text.append(txt)
        if self.most_similar_dict or picking_mode == "wordnet":
            while len(self.augmented_text) < augmented_size:
                for txt in text:
                    if len(self.augmented_text) >= augmented_size:
                        break
                    if picking_mode == "weighted":
                        new_doc = self.augment_doc(txt, self.weighted_probability_pick, protected_words, alpha=alpha)
                    elif picking_mode == "random":
                        new_doc = self.augment_doc(txt, self.random_pick, protected_words, alpha=alpha)
                    elif picking_mode == "first":
                        new_doc = self.augment_doc(txt, self.first_pick, protected_words, alpha=alpha)
                    elif picking_mode == "wordnet":
                        new_doc = wordnet.run(txt, n=len(txt))
                    self.augmented_text.append(new_doc)

        return self.augmented_text

    def augment_doc(self, text, picking_function, protected_words, alpha=0):
        """
        Helper function for applying different random picking types on an input text.
        :param text: list of strings, e.g a tokenized document
        :param picking_function: random function to be used during sampling
        :param protected_words: list of words that have to be kept intact
        :param alpha: probabililty of augmenting a word, must be between 0 and 1
        :return:
        """
        new_doc = []
        for word in text:
            rnd_num = random.uniform(0, 1)
            # ensuring that protected words remain intact
            if not {word}.intersection(protected_words) and self.most_similar_dict.get(word) and rnd_num <= alpha:
                new_doc.append(picking_function(self.most_similar_dict[word]))
            else:
                new_doc.append(word)

        return new_doc

    @staticmethod
    def random_pick(similar_list):
        """
        Performs uniformly distributed random selection.
        :param similar_list: must be in the following format: [("token1",weight1),("token2",weight2)]
        :return: one token from the similar_list list
        """
        if not (isinstance(similar_list, list) or isinstance(similar_list, np.ndarray) or isinstance(similar_list,
                                                                                                     tuple)):
            return similar_list
        return rng.choice(similar_list)[0]

    @staticmethod
    def first_pick(similar_list):
        """
        Picks the first element's text part from the similar_list list.
        :param similar_list: must be in the following format: [("token1",weight1),("token2",weight2)]
        :return: one token from the similar_list list
        """
        if not (isinstance(similar_list, list) or isinstance(similar_list, np.ndarray) or isinstance(similar_list,
                                                                                                     tuple)):
            return similar_list
        return similar_list[0]

    @staticmethod
    def weighted_probability_pick(similar_list):
        """
        Performs weighted random selection. Probabilities are calculated based on the application of softmax function
        on the weights.
        :param similar_list: must be in the following format: [("token1",weight1),("token2",weight2)]
        :return: one token from the similar_list list
        """
        if not (isinstance(similar_list, list) or isinstance(similar_list, np.ndarray) or isinstance(similar_list,
                                                                                                     tuple)):
            return similar_list
        words = [word[0] for word in similar_list]
        weights = [wght[1] for wght in similar_list]
        weights = softmax(weights, axis=0)
        return rng.choice(words, p=weights, replace=False)


class EasyDataAugmentation:
    """
    Minor modifications original EDA algorithm (2019) [1] https://github.com/jasonwei20/eda_nlp/blob/master/code/eda.py.

    [1] Wei, J. and Zou, K., 2019, November. EDA: Easy Data Augmentation Techniques for Boosting Performance on
    Text Classification Tasks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing
    and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) (pp. 6383-6389).
    https://www.aclweb.org/anthology/D19-1670.pdf

    """

    def __init__(self):
        self.protected_words = []
        self.augmented_text = []

    def init_wordnet(self, wordnet_path):
        self.wordnet = WordNetAugmentation()
        self.wordnet.set_wordnet_path(wordnet_path)
        self.wordnet.load_synonyms_dict()

    def set_protected_words(self, protected_words_list):
        """
        Setter for protected word list.
        :param protected_words_list: list of words that cannot change during the text_augmentation process.
        :return: None
        """
        self.protected_words = protected_words_list

    def random_deletion(self, words: list, p: float, protected_words: list = None):
        """
        Random deletion.
        Randomly delete words from the sentence with probability p.
        :param words: list of strings.
        :param p: probability of deleting random words
        :return:
        """

        # obviously, if there's only one word, don't delete it
        if len(words) == 1:
            return words
        if not protected_words:
            protected_words = self.protected_words
        # randomly delete words with probability p
        new_words = []
        for word in words:
            r = random.uniform(0, 1)
            # ensuring that protected words remain intact
            if {word}.intersection(protected_words) or r > p:
                new_words.append(word)

        # if you end up deleting all words, just return a random word
        if len(new_words) == 0:
            rand_int = random.randint(0, len(words) - 1)
            return [words[rand_int]]

        return new_words

    def random_swap(self, words, n):
        """
        Random swap.
        Randomly swap two words in the sentence n times.
        :param n: number of times the swapping is done.
        :return:
        """

        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)
        return new_words

    @staticmethod
    def swap_word(new_words):
        """
        Helper function for swapping words in a list of words.
        :param new_words: list of words.
        :return: modified document in tokenized format
        """
        random_idx_1 = random.randint(0, len(new_words) - 1)
        random_idx_2 = random_idx_1
        counter = 0
        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words) - 1)
            counter += 1
            if counter > 3:
                return new_words
        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words

    def synonym_replacement(self, words: list, n: int, protected_words: list = None):
        """
        Synonym replacement.
        Randomly replace n synonyms into the sentence.
        :param n: number of insertion
        :param protected_words: list of words that cannot be changed
        :return:
        """
        if not protected_words:
            protected_words = self.protected_words
        new_words = words.copy()
        new_words = self.wordnet.synonym_replacement(new_words, n=n, protected_words=protected_words)
        return new_words

    def random_insertion(self, words: list, n: int, protected_words: list = None):
        """
        Random insertion.
        Randomly insert n synonyms into the sentence.
        :param n: the maximum number of insertions
        :param protected_words: list of words that cannot be used for synonym selection
        :return:
        """
        if not protected_words:
            protected_words = self.protected_words
        new_words = words.copy()
        new_words = self.wordnet.synonym_insertion(new_words, n=n, protected_words=protected_words)
        return new_words

    def augment_text(
            self, text: list, augmented_size: int, mode: str = "RD", protected_words: list = None, alpha: float = 0.1
    ):
        """
        Performs a chosen EDA data text_augmentation algorithm on a given dataset.
        :param text: list of lists e.g. list of tokenized documents
        :param mode: Modes defined in EDA:
                    RD: random deletion
                    RI: random insertion
                    RS: random swap
                    SR: synonym replacement
        :protected_words: list of words that cannot be modified
        :alpha: proportion of the text to be modified by text_augmentation
        :augmented_size: the size of the augmented dataset (including the original input)
        :return: augmented text
        """
        if len(text) >= augmented_size:
            raise ValueError(
                "The augmented size criterion has been already met. Please increase the augmented size above the number"
                "of documents!"
            )
        if protected_words:
            self.protected_words = protected_words

        self.original_text = text
        for txt in text:
            self.augmented_text.append(txt)
        while len(self.augmented_text) < augmented_size:
            for txt in text:
                if len(self.augmented_text) >= augmented_size:
                    break
                n = max(1, int(alpha * len(txt)))
                if mode == "RD":
                    new_doc = self.random_deletion(txt, alpha, protected_words=protected_words)
                if mode == "RI":
                    new_doc = self.random_insertion(txt, n, protected_words=protected_words)
                if mode == "RS":
                    new_doc = self.random_swap(txt, n)
                if mode == "SR":
                    new_doc = self.synonym_replacement(txt, n, protected_words=protected_words)
                self.augmented_text.append(new_doc)


if __name__ == "__main__":
    augmenter = WordVectorAugmenter()
    most_similar_list = [
        ("Horváth", 0.907128095626831),
        ("Kozma", 0.800941014289856),
        ("Varga", 0.792798900604248),
        ("Tóth", 0.690268862247467),
        ("Zoltán", 0.5889473080635071),
        ("Tibor", 0.4880890607833862),
        ("György", 0.3872979879379272),
        ("Juhász", 0.2860651254653931),
        ("Kozákovits", 0.1843592405319214),
        ("Péter", 0.0841139674186707),
    ]
    most_similar_list2 = "szó"
    c = {
        "Horváth": 0,
        "Kozma": 0,
        "Varga": 0,
        "Tóth": 0,
        "Zoltán": 0,
        "Tibor": 0,
        "György": 0,
        "Juhász": 0,
        "Kozákovits": 0,
        "Péter": 0,
    }
    for _ in range(100):
        # print(augmenter.random_pick(most_similar_list))
        # print(augmenter.probability_pick(most_similar_list))
        # print(augmenter.random_pick(most_similar_list2))
        # print(augmenter.probability_pick(most_similar_list))
        sample = augmenter.weighted_probability_pick(most_similar_list)
        c[sample] += 1
    print(c)
