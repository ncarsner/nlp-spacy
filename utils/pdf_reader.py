# import nltk
# nltk.download('stopwords')

import PyPDF2
import re
from collections import Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt


def get_common_words_from_pdf(file_path, num_words=5, custom_stop_words=None):
    # Read the PDF file
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()

    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = text.lower()

    # Tokenize the text
    words = text.split()

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    stop_words.update(set(word for word in words if len(word) == 1 or word.isdigit()))

    # Include custom stop words
    if custom_stop_words is not None:
        stop_words.update(set(custom_stop_words))

    # render qualifying words list
    words = [word for word in words if word not in stop_words]

    # Count the frequency of each word
    word_counter = Counter(words)

    # Get the most common words
    most_common_words = word_counter.most_common(num_words)

    return most_common_words


# Example usage
pdf_file_path = "./data/raw/mlb_rules_2023.pdf"
num_words = 20
additional_stop_words = ["base", "ball"]
most_common_words = get_common_words_from_pdf(
    pdf_file_path, num_words=num_words, custom_stop_words=additional_stop_words
)

print("Most common words (excluding stopwords):")
for word, count in most_common_words:
    print(f"{word}: {count}")


# Plot the most common words
def plot_common_words(common_words):
    words, counts = zip(*common_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color="skyblue")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Most Common Words")
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.show()


def main():
    file_path = "./data/raw/mlb_rules_2023.pdf"
    num_words = 15
    additional_stop_words = ["base", "ball"]
    most_common_words = get_common_words_from_pdf(
        file_path, num_words=num_words, custom_stop_words=additional_stop_words
    )

    print("Most common words (excluding stopwords):")
    for word, count in most_common_words:
        print(f"{word}: {count}")


    plot_common_words(most_common_words)


if __name__ == "__main__":
    main()
