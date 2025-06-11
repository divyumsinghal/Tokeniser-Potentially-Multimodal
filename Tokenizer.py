from collections import defaultdict, OrderedDict
from typing import Dict, Tuple, List, DefaultDict

# Special Tokens
END_OF_WORD = "</w>"
UNKNOWN_TOKEN = "<unk>"
SPACE = " "
FORBIDDEN_SET = {UNKNOWN_TOKEN, END_OF_WORD, SPACE}

DEFAULT_ITERATIONS = 15


class Tokenizer:

    def __init__(self, iterations: int = DEFAULT_ITERATIONS):
        self.iterations = iterations
        self.merge_rules: OrderedDict[Tuple[str, str], str] = OrderedDict()
        self.vocab: Dict[Tuple[str, ...], int] = {}

    def __get_unique_charset(self, data: str) -> Dict[Tuple[str, ...], int]:
        """
        Returns a dictionary of unique characters and their frequencies in the input string.
        This function counts the occurrences of each unique character in the input string, excluding forbidden tokens.

        Args:
            data: The input string from which to extract unique characters.

        Returns:
            A dictionary where keys are tuples containing a single character (as Tuple[str, ...]) and values are their frequencies.
        """

        unique_charset: DefaultDict[Tuple[str, ...], int] = defaultdict(int)
        for char in data:
            if char not in FORBIDDEN_SET:
                unique_charset[(char,)] += 1

        # Ensure special tokens are present
        for token in (END_OF_WORD, UNKNOWN_TOKEN, SPACE):
            unique_charset[(token,)] += 1

        return unique_charset

    def __build_initial_vocab(self, data: str) -> Dict[Tuple[str, ...], int]:
        """
        Builds the initial vocabulary from the input string by splitting words into character tokens.
        Each word is converted into a tuple of its characters with an end-of-word token appended.

        Args:
            data: The input string from which to build the vocabulary.

        Returns:
            A dictionary where keys are tuples of character tokens (including the end-of-word token) and values are their frequencies.
        """

        vocab = self.__get_unique_charset(data)

        words = data.strip().split()

        for word in words:
            if word and word not in FORBIDDEN_SET:
                tokens = tuple(word) + (END_OF_WORD,)
                vocab[tokens] += 1

        return vocab

    def __build_pairwise_vocab(
        self, vocab: Dict[Tuple[str, ...], int]
    ) -> List[Tuple[Tuple[str, str], int]]:
        """
        Generates a list of token pairs and their frequencies from the vocabulary.
        This function identifies all adjacent token pairs in the vocabulary and counts their occurrences.

        Args:
            vocab: A dictionary where keys are tuples of tokens and values are their frequencies.

        Returns:
            A list of tuples, where each tuple contains a token pair and its frequency, sorted by frequency in descending order.
        """

        pairwise_vocab = defaultdict(int)

        for word, freq in vocab.items():
            for i in range(len(word) - 1):
                pair = (word[i], word[i + 1])
                pairwise_vocab[pair] += freq

        return sorted(pairwise_vocab.items(), key=lambda item: item[1], reverse=True)

    def __replace_pairs_in_vocab(
        self, vocab: Dict[Tuple[str, ...], int], pair_to_replace: Tuple[str, str]
    ) -> Dict[Tuple[str, ...], int]:
        """
        Replaces all occurrences of a specified token pair in the vocabulary with a merged token.
        This function updates the vocabulary by merging the given pair wherever it appears in token sequences.

        Args:
            vocab: A dictionary where keys are tuples of tokens and values are their frequencies.
            pair_to_replace: A tuple containing the token pair to be merged.

        Returns:
            A new dictionary with the specified token pair replaced by the merged token in all token sequences.
        """

        new_vocab = defaultdict(int)
        pair = pair_to_replace
        merged_token = "".join(pair)

        # print(f"Merging: {merged_token}")

        for token_seq, freq in vocab.items():
            new_seq = []
            i = 0
            while i < len(token_seq):
                if i < len(token_seq) - 1 and (token_seq[i], token_seq[i + 1]) == pair:
                    new_seq.append(merged_token)
                    i += 2
                else:
                    new_seq.append(token_seq[i])
                    i += 1
            new_vocab[tuple(new_seq)] += freq

        return new_vocab

    def train_vocab(self, data: str):
        """
        Trains a vocabulary by iteratively merging the most frequent token pairs in the input data.
        This function applies a specified number of merge operations to build a subword vocabulary.

        Args:
            data: The input string used to build and train the vocabulary.
            iter: The number of merge iterations to perform (default is 15).

        Returns:
            A dictionary representing the trained vocabulary, where keys are tuples of tokens and values are their frequencies.
        """

        self.vocab = self.__build_initial_vocab(data)

        for _ in range(self.iterations):
            pairwise_vocab = self.__build_pairwise_vocab(self.vocab)

            if not pairwise_vocab or pairwise_vocab[0][1] <= 0:
                print("No more pairs to merge or frequency is zero.")
                break

            most_frequent_pair = pairwise_vocab[0][0]
            merged_token = "".join(most_frequent_pair)
            self.merge_rules[most_frequent_pair] = merged_token
            self.vocab = self.__replace_pairs_in_vocab(self.vocab, most_frequent_pair)

    def get_vocab(self) -> Dict[Tuple[str, ...], int]:
        return self.vocab

    def get_merge_rules(self) -> OrderedDict:
        return self.merge_rules
