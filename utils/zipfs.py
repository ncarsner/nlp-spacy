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


text_file = "./data/raw/speech_we_shall_fight_on_the_beaches.txt"
text_file = "./data/raw/speech_day_of_infamy.txt"


def open_file():
    with open(text_file, "r", encoding="utf-8") as f:
        file_content = f.read().lower()
        file_content = [word for word in file_content.split()]
        file_content = " ".join(file_content)
    return file_content


def main(file_content):
    stoplist = stopwords.words("english")
    stoplist.extend(
        [
            "said",
            "i",
            "it",
            "you",
            "and",
            "that",
        ]
    )

    clean = [word for word in file_content.split() if word not in stoplist]
    clean_text = " ".join(clean)
    words = re.findall("\w+", clean_text)
    top_10 = Counter(words).most_common(10)

    for word, count in top_10:
        print(f"{word!r:<4} {count:^4}")


if __name__ == "__main__":
    text = open_file()
    main(text)
