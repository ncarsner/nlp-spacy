# import string
from collections import Counter
import re

# import matplotlib.pyplot as plt
# import numpy as np
# from numpy.random import default_rng

# from scipy.special import zeta
# from scipy.stats import zipf

# import nltk
from nltk.corpus import stopwords


def read_text_file(file_path):
    """
    Read and preprocess a text file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Preprocessed file content as a string
    """
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read().lower()
        file_content = [word for word in file_content.split()]
        file_content = " ".join(file_content)
    return file_content


def get_stopwords(additional_words=None):
    """
    Get stopwords list with optional additional words.
    
    Args:
        additional_words: Optional list of additional stopwords
        
    Returns:
        List of stopwords
    """
    stoplist = stopwords.words("english")
    if additional_words:
        stoplist.extend(additional_words)
    return stoplist


def remove_stopwords(text, stoplist):
    """
    Remove stopwords from text.
    
    Args:
        text: Input text string
        stoplist: List of stopwords to remove
        
    Returns:
        Text with stopwords removed
    """
    clean = [word for word in text.split() if word not in stoplist]
    return " ".join(clean)


def extract_words(text):
    """
    Extract words from text using regex.
    
    Args:
        text: Input text string
        
    Returns:
        List of words
    """
    return re.findall(r"\w+", text)


def get_top_words(words, n=10):
    """
    Get the n most common words.
    
    Args:
        words: List of words
        n: Number of top words to return
        
    Returns:
        List of (word, count) tuples
    """
    return Counter(words).most_common(n)


def analyze_text(file_path, top_n=10, additional_stopwords=None):
    """
    Analyze text file and return top N words after removing stopwords.
    
    Args:
        file_path: Path to text file
        top_n: Number of top words to return
        additional_stopwords: Optional additional stopwords to remove
        
    Returns:
        List of (word, count) tuples for top N words
    """
    if additional_stopwords is None:
        additional_stopwords = ["said", "i", "it", "you", "and", "that"]
    
    file_content = read_text_file(file_path)
    stoplist = get_stopwords(additional_stopwords)
    clean_text = remove_stopwords(file_content, stoplist)
    words = extract_words(clean_text)
    return get_top_words(words, top_n)


def main():
    """Main function for Zipf's Law word frequency analysis."""
    text_file = "./data/raw/speech_day_of_infamy.txt"
    
    top_10 = analyze_text(
        text_file,
        top_n=10,
        additional_stopwords=["said", "i", "it", "you", "and", "that"]
    )

    for word, count in top_10:
        print(f"{word!r:<4} {count:^4}")


if __name__ == "__main__":
    main()
