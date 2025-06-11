from collections import defaultdict

# Special Tokens
end_of_word = "</w>"
unknown_token = "<unk>"
space = " "
forbidden_set = {unknown_token, end_of_word, space}


class Tokenizer:

    def get_unique_charset(self, data: str) -> dict:
        """
        Returns a dictionary of unique characters and their frequencies in the input string.
        This function counts the occurrences of each unique character in the input string, excluding forbidden tokens.

        Args:
            data: The input string from which to extract unique characters.

        Returns:
            A dictionary where keys are tuples containing a single character and values are their frequencies.
        """

        unique_charset = defaultdict(int)
        for char in data:
            if char not in forbidden_set:
                unique_charset[(char,)] += 1
        return unique_charset

    def build_initial_vocab(self, data: str) -> dict:
        """
        Builds the initial vocabulary from the input string by splitting words into character tokens.
        Each word is converted into a tuple of its characters with an end-of-word token appended.

        Args:
            data: The input string from which to build the vocabulary.

        Returns:
            A dictionary where keys are tuples of character tokens (including the end-of-word token) and values are their frequencies.
        """

        vocab = defaultdict(int)

        words = data.strip().split()

        for word in words:
            if word not in forbidden_set:
                tokens = tuple(word) + (end_of_word,)
                vocab[tokens] += 1

        return vocab

    def make_pairwise_vocab(self, vocab: dict) -> list:
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

    def replace_pairs_in_vocab(self, vocab: dict, pair_to_replace: tuple) -> dict:
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
        pair = pair_to_replace[0]
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

    def train_vocab(self, data: str, iter: int = 15) -> tuple[dict, dict]:
        """
        Trains a vocabulary by iteratively merging the most frequent token pairs in the input data.
        This function applies a specified number of merge operations to build a subword vocabulary.

        Args:
            data: The input string used to build and train the vocabulary.
            iter: The number of merge iterations to perform (default is 15).

        Returns:
            A dictionary representing the trained vocabulary, where keys are tuples of tokens and values are their frequencies.
        """

        vocab = self.build_initial_vocab(data)
        merge_rules = defaultdict(str)

        for _ in range(iter):
            pairwise_vocab = self.make_pairwise_vocab(vocab)

            if not pairwise_vocab or pairwise_vocab[0][1] == 0:
                print("No more pairs to merge or frequency is zero.")
                break

            vocab = self.replace_pairs_in_vocab(vocab, pairwise_vocab[0])
            merge_rules[pairwise_vocab[0][0]] = "".join(pairwise_vocab[0][0])

        return vocab, merge_rules
