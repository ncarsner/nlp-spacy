import string
from collections import Counter
import re

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import default_rng

from scipy.special import zeta
from scipy.stats import zipf

import nltk
from nltk.corpus import stopwords


# rng = default_rng()
# vals = rng.standard_normal(10)
# more_vals = rng.standard_normal(10)

text_file = r'C:\Users\AG20D13\Documents\speech_we_shall_fight_on_the_beaches.txt'
# text_file = r'C:\Users\AG20D13\Documents\speech_day_of_infamy.txt'
# text_file = r'C:\Users\AG20D13\Documents\speech_we_choose_to_go_to_the_moon.txt'
# text_file = r'C:\Users\AG20D13\Documents\speech_i_have_a_dream.txt'

def open_file():
    with open(text_file, 'r', encoding='utf-8') as f:
        file_content = f.read().lower()
        file_content = [word for word in file_content.split()]
        file_content = ' '.join(file_content)
    return file_content

def main(file_content):
   stoplist = stopwords.words('english') # Bring in the default English NLTK stop words
   stoplist.extend(["said", "i", "it", "you", "and","that",])
   # print(stoplist)
   clean = [word for word in file_content.split() if word not in stoplist]
   clean_text = ' '.join(clean)
   words = re.findall('\w+', clean_text)
   top_10 = Counter(words).most_common(10)
   for word,count in top_10:
       print(f'{word!r:<4} {count:^4}')

if __name__ == "__main__":
   text = open_file()
   main(text)


# # SIMPLE COUNTER
# from collections import Counter

# with open(text_file, 'r', encoding='utf-8') as f:
#     file_content = f.read()
#     excluded = ['the','and','of','a','to','in','we','that']
#     words = [word.lower() for word in file_content.split() if word not in excluded]
#     print(Counter(words).most_common(10))



# a = 4.0
# n = 20_000
# s = np.random.zipf(a, n)

# count = np.bincount(s)
# k = np.arange(1, s.max() + 1)

# plt.bar(k, count[1:], alpha=0.5, label='sample count')
# plt.plot(k, n*(k**-a)/zeta(a), 'k.-', alpha=0.5, label='expected count')
# plt.semilogy()
# plt.grid(alpha=0.4)
# plt.legend()
# plt.title(f'Zipf sample, a={a}, size={n}')
# plt.show()

