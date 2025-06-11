from itertools import pairwise
import os
import Tokenizer
import yaml

data = ""

# Load all the txt files from the "data" directory
for filename in os.listdir("data"):
    if filename.endswith(".txt"):
        with open(os.path.join("data", filename), "r") as f:
            data += f.read()


tokenizer = Tokenizer.Tokenizer(100)

# Train the tokenizer on the loaded data
tokenizer.train_vocab(data)

# Get the vocabulary and merge rules
vocab = tokenizer.get_vocab()
merge_rules = tokenizer.get_merge_rules()

# print vocab in a pretty format, sorted by frequency
print("Vocabulary:")
for token, freq in sorted(vocab.items(), key=lambda item: item[1], reverse=True):
    print(f"{token}: {freq}")

# print merge rules
print("\nMerge Rules:")
for pair, freq in sorted(merge_rules.items(), key=lambda item: item[1], reverse=True):
    print(f"{pair}: {freq}")

# save the vocab and merge rules to yaml files
# Convert tuple keys to space-separated strings
vocab_yaml = {" ".join(token): freq for token, freq in vocab.items()}
merge_rules_yaml = {" ".join(pair): merged for pair, merged in merge_rules.items()}

"""
# Write to YAML files
with open("vocab.yaml", "w") as f:
    yaml.dump({"vocab": vocab_yaml}, f, sort_keys=False)

with open("merge_rules.yaml", "w") as f:
    yaml.dump({"merge_rules": merge_rules_yaml}, f, sort_keys=False)
"""
