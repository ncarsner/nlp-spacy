import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import zipf


text = "This is a sample text to demonstrate Zipf's Law. This text contains some repeated words, like 'text' and 'words'."
text = r"data/raw/speech_day_of_infamy.txt"

# Prepare data - Tokenize the text
words = text.lower().split()

# Prepare data - Count word frequencies
word_counts = Counter(words)

# Calculate word ranks and frequencies
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
ranks = np.arange(1, len(sorted_word_counts) + 1)
frequencies = [count for word, count in sorted_word_counts]

# Plot the Zipf's Law curve
plt.plot(ranks, frequencies, marker='.')
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.title("Zipf's Law")
plt.xscale('log')
plt.yscale('log')
plt.show()

# Fit a Zipf distribution
params = zipf.fit(frequencies)
print("Zipf distribution parameters:", params)