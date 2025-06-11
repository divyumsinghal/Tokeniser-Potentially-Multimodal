from collections import defaultdict

# Special Tockens
end_of_word = "</w>"
unknown_token = "<unk>"


def get_unique_charset(data: str) -> set:
    """Returns the set of unique characters in the input string.

    This function extracts all unique characters from the provided string and returns them as a set.

    Args:
        data: The input string from which to extract unique characters.

    Returns:
        A set containing all unique characters found in the input string.
    """

    unique_charset = set(data)
    unique_charset.add(end_of_word)
    unique_charset.add(unknown_token)
    return unique_charset


def build_initial_vocab(data: str) -> dict:
    """Builds an initial vocabulary from the input string.

    This function creates a dictionary where each unique character in the input string is mapped to its index.

    Args:
        data: The input string from which to build the vocabulary.

    Returns:
        A dictionary mapping each unique character to its frequency.
    """

    vocab = defaultdict(int)
    unique_chars = get_unique_charset(data)

    words = data.split(" ")

    for word in words:
        word_as_a_character_list = tuple(list(word) + [end_of_word])
        vocab[word_as_a_character_list] += 1

    return vocab


def make_pairwise_vocab(vocab: dict) -> list:
    """Creates a pairwise vocabulary from the initial vocabulary.

    This function generates a new vocabulary where each entry is a tuple of characters and their frequency.

    Args:
        vocab: The initial vocabulary mapping characters to their frequencies.

    Returns:
        A dictionary mapping pairs of characters to their frequency.
    """

    pairwise_vocab = defaultdict(int)

    for word, frequency in vocab.items():
        for i in range(len(word) - 1):
            pair = (word[i], word[i + 1])
            pairwise_vocab[pair] += frequency

    return sorted(pairwise_vocab.items(), key=lambda item: item[1], reverse=True)
