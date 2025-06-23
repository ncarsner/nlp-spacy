import spacy
import random
from collections import Counter

"""
Reference Table for Token Components:
- Text   : The original token text from the phrase.
- POS    : Part-of-speech tag for the token, indicating its grammatical role in the sentence.
    Common POS tags include:
    - NOUN  : Noun (e.g., "dog", "happiness")
    - PROPN : Proper noun (e.g., "John", "Paris")
    - PRON  : Pronoun (e.g., "he", "they")
    - VERB  : Verb (e.g., "run", "is")
    - AUX   : Auxiliary verb (e.g., "be", "have")
    - ADJ   : Adjective (e.g., "happy", "red")
    - ADV   : Adverb (e.g., "quickly", "very")
    - DET   : Determiner (e.g., "the", "a")
    - ADP   : Adposition (prepositions and postpositions, e.g., "in", "on")
    - CONJ  : Conjunction (e.g., "and", "but")
    - CCONJ : Coordinating conjunction (e.g., "and", "or")
    - SCONJ : Subordinating conjunction (e.g., "because", "although")
    - PART  : Particle (e.g., "up", "down" in phrasal verbs like "give up")
    - NUM   : Numeral (e.g., "one", "100")
    - INTJ  : Interjection (e.g., "wow", "ouch")
    - PUNCT : Punctuation (e.g., ".", ",", "!")
    - SYM   : Symbol (e.g., "$", "%", "#")
    - X     : Other (tokens that do not fit into the above categories)
    - SPACE : Space (whitespace characters, not usually included in analysis)
- Lemma  : The base or dictionary form of the token
    (e.g., 'be' for 'is').
- Dep    : Syntactic dependency label, indicating the token's grammatical role
    Common dependency labels include:
    - nsubj : Nominal subject (e.g., "I" in "I eat")
    - ROOT  : Root of the sentence (the main verb, e.g., "eat" in "I eat")
    - obj   : Object (e.g., "apple" in "I eat an apple")
    - amod  : Adjectival modifier (e.g., "red" in "the red apple")
    - advmod: Adverbial modifier (e.g., "quickly" in "he runs quickly")
    - prep  : Prepositional modifier (e.g., "in" in "in the park")
    - pcomp : Prepositional complement (e.g., "park" in "in the park")
    - det   : Determiner (e.g., "the" in "the apple")
    - advcl : Adverbial clause modifier (a clause functioning as an adverb, e.g., "when he arrived" in "I left when he arrived")
    - cc    : Coordinating conjunction (e.g., "and", "or", "but")
    - conj  : Conjunct (the second or later element in a coordinated phrase, e.g., "cats" in "dogs and cats")
    - det   : Determiner (e.g., "the", "a", "an")
    - attr  : Attribute (a nominal predicate, e.g., "a doctor" in "He is a doctor")
- Head Text  : The text of the token's syntactic parent.
    (the word this token is attached to in the parse tree).
- Entity : Named entity type if the token is part of a recognized entity.
    Common entity types include:
    - PERSON : Person names (e.g., "John Doe")
    - ORG    : Organizations (e.g., "NFL", "United Nations")
    - GPE    : Geopolitical entities (countries, cities, etc., e.g., "France", "New York")
    - DATE   : Dates (e.g., "January 1, 2020")
    - TIME   : Times (e.g., "12:00 PM")
    - MONEY  : Monetary values (e.g., "$100", "€50")
    - PERCENT: Percentages (e.g., "50%")
    - NORP   : Nationalities or religious/political groups (e.g., "American", "Christian")
    - FAC    : Facilities (e.g., "Eiffel Tower", "Golden Gate Bridge")
    '-' if not part of any entity.

Other useful Token attributes and methods:
- idx        : Index of the token in the original text (character offset).
- is_alpha   : True if the token consists of alphabetic characters.
- is_stop    : True if the token is a stop word (common word, usually filtered out).
- is_digit   : True if the token consists of digits.
- is_title   : True if the token is in title case.
- is_lower   : True if the token is in lowercase.
- is_upper   : True if the token is in uppercase.
- shape_     : The word shape (e.g., 'Xxxx', 'dd', etc.).
- like_num   : True if the token resembles a number.
- like_email : True if the token resembles an email address.
- like_url   : True if the token resembles a URL.
- morph      : Morphological features of the token (e.g., tense, number).
- children   : Iterator of the token's syntactic children.
- ancestors  : Iterator of the token's syntactic ancestors.
- lefts      : Iterator of left children in the dependency parse.
- rights     : Iterator of right children in the dependency parse.
- sent       : The sentence span containing the token.
- nbor()     : Get the neighboring token at a given offset.
- similarity(): Compute similarity to another token, span, or doc.

"""

# Load the small English model
nlp = spacy.load("en_core_web_sm")

DEBUG = True  # Set to True to enable debug output

phrases = [
    "Do or do not, there is no try.",
    "To be, or not to be, that is the question.",
    "The only thing we have to fear is fear itself.",
    "In the beginning, God created the heavens and the earth.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "A journey of a thousand miles begins with a single step.",
    "It was the best of times, it was the worst of times.",
    "Call me Ishmael.",
    "All happy families are alike; each unhappy family is unhappy in its own way.",
    "It was a bright cold day in April, and the clocks were striking thirteen.",
]

if __name__ == "__main__":
    # Randomly select a phrase
    selected_phrase = random.choice(phrases)
    print(f"Selected phrase: {selected_phrase}")

    # Process the selected phrase with spaCy
    doc = nlp(selected_phrase)

    # Filter out punctuation tokens
    tokens_no_punct = [token for token in doc if token.pos_ != "PUNCT"]

    print("\nDetailed token analysis (excluding punctuation):")

    # Determine max lengths for each column based on the selected phrase
    max_text = max(len(token.text) for token in tokens_no_punct + [doc[0]])
    max_pos = max(len(token.pos_) for token in tokens_no_punct + [doc[0]])
    max_lemma = max(len(token.lemma_) for token in tokens_no_punct + [doc[0]])
    max_dep = max(len(token.dep_) for token in tokens_no_punct + [doc[0]])
    max_head = max(len(token.head.text) for token in tokens_no_punct + [doc[0]])
    max_ent = max(len(token.ent_type_) if token.ent_type_ else 1 for token in tokens_no_punct + [doc[0]])

    # Add some padding for readability
    pad = 2
    fmt = (
        f"{{:<{max_text + pad}}} "
        f"{{:<{max_pos + pad}}} "
        f"{{:<{max_lemma + pad}}} "
        f"{{:<{max_dep + pad}}} "
        f"{{:<{max_head + pad}}} "
        f"{{:<{max_ent + pad}}}"
    )

    header = fmt.format("Text", "POS", "Lemma", "Dep", "Head Text", "Entity")
    print(header)
    print("-" * len(header))
    for token in tokens_no_punct:
        ent = token.ent_type_ if token.ent_type_ else "-"
        print(fmt.format(token.text, token.pos_, token.lemma_, token.dep_, token.head.text, ent))

    # Count POS and lemma occurrences
    pos_counts = Counter(token.pos_ for token in tokens_no_punct)
    lemma_counts = Counter(token.lemma_ for token in tokens_no_punct)

    # Get the most common POS and lemma
    most_common_pos = pos_counts.most_common(1)
    most_common_lemma = lemma_counts.most_common(1)

    # Number of most common POS tags to display
    N_MOST_COMMON_POS = 2

    print(f"\nTop {N_MOST_COMMON_POS} most common POS (excluding punctuation):")
    for pos, count in pos_counts.most_common(N_MOST_COMMON_POS):
        print(f"{pos}: {count}")
    if not pos_counts:
        print("No POS found.")

    print("\nMost common lemma (excluding punctuation):")
    if most_common_lemma:
        print(f"{most_common_lemma[0][0]}: {most_common_lemma[0][1]}")
    else:
        print("No lemma found.")

"""
This script analyzes a randomly selected phrase using spaCy's English language model, providing a detailed breakdown of each token's linguistic features and summarizing the most common part-of-speech (POS) tags and lemmas.

Features:
- Randomly selects a phrase from a predefined list of famous quotes.
- Processes the phrase with spaCy, excluding punctuation tokens from analysis.
- Prints a reference table explaining key token attributes (e.g., POS, lemma, dependency, entity type).
- Dynamically formats and displays a table of token details, including:
    - Text: Original token text.
    - POS: Part-of-speech tag.
    - Lemma: Base form of the token.
    - Dep: Syntactic dependency label.
    - Head Text: The syntactic parent token.
    - Entity: Named entity type or '-' if not applicable.
- Counts and displays the most common POS tag and lemma in the phrase (excluding punctuation).
- Includes debug output for easier inspection of token attributes.

Intended Usage:
Run this script directly to analyze a randomly chosen phrase and view a summary of its linguistic components. Requires the spaCy library and the 'en_core_web_sm' model to be installed.
"""
# This code is a standalone script and does not require any additional files or modules.
