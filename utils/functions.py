import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import zipf
import string


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def main():
    """Main function for Zipf's Law analysis"""
    source_file = "./data/raw/speech_day_of_infamy.txt"

    # Read the text file
    with open(source_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Prepare data - Tokenize the text
    words = text.lower().split()

    # Prepare data - Count word frequencies
    word_counts = Counter(words)

    # Calculate word ranks and frequencies
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    ranks = np.arange(1, len(sorted_word_counts) + 1)
    frequencies = [count for word, count in sorted_word_counts]

    # Plot the Zipf's Law curve
    plt.plot(ranks, frequencies, marker=".")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.title("Zipf's Law")
    plt.xscale("log")
    plt.yscale("log")
    plt.show()

    # Fit a Zipf distribution
    a, loc, scale = zipf.fit(frequencies, floc=0)
    zipf.fit(frequencies, floc=0)
    print("Zipf distribution parameters: a =", a, ", loc =", loc, ", scale =", scale)


if __name__ == "__main__":
    main()
