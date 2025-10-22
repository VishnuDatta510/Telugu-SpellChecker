import re
import json  # for saving tokenized sentences

# Read the cleaned Telugu data
with open("final_cleaned_telugu_data_2.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split into sentences
sentences = [s.strip() for s in text.split('.') if s.strip()]

# Tokenize sentences into words
tokenized_sentences = [re.findall(r'[\u0C00-\u0C7F]+', s) for s in sentences]

# Build vocabulary
vocabulary = set(word for sent in tokenized_sentences for word in sent)

# Save sentences to a text file (one sentence per line)
with open("telugu_sentences_2.txt", "w", encoding="utf-8") as f:
    for sentence in sentences:
        f.write(sentence + "\n")

# Save tokenized sentences as JSON
with open("telugu_tokenized_sentences_2.json", "w", encoding="utf-8") as f:
    json.dump(tokenized_sentences, f, ensure_ascii=False, indent=2)

# Save vocabulary as text file (one word per line)
with open("telugu_vocabulary_2.txt", "w", encoding="utf-8") as f:
    for word in sorted(vocabulary):
        f.write(word + "\n")

print(f"Saved {len(sentences)} sentences to 'telugu_sentences_2.txt'")
print(f"Saved tokenized sentences to 'telugu_tokenized_sentences_2.json'")
print(f"Saved {len(vocabulary)} unique words to 'telugu_vocabulary_2.txt'")
