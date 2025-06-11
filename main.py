from itertools import pairwise
import os
import Tokenizer

data = ""

# Load all the txt files from the "data" directory
for filename in os.listdir("data"):
    if filename.endswith(".txt"):
        with open(os.path.join("data", filename), "r") as f:
            data += f.read()

print(f"Data: {data}")

initial_vocab = Tokenizer.build_initial_vocab(data)

# print(f"Initial vocabulary: {initial_vocab}")

pairwise_vocab = Tokenizer.make_pairwise_vocab(initial_vocab)
print(f"Pairwise vocabulary: {pairwise_vocab}")
