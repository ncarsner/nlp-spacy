import json
import random
import spacy

# Load the small English model
nlp = spacy.load("en_core_web_sm")

DEBUG = True  # Set to True to enable debug output

def get_intent(text):
    doc = nlp(text.lower())
    if any(token.lemma_ in ["hello", "hi", "hey"] for token in doc):
        return "greeting"
    # elif any(token.lemma_ in ["bye", "goodbye", "see"] for token in doc):
    elif any(token.lemma_ in ["bye", "goodbye"] for token in doc if token.pos_ == "INTJ" or token.is_alpha and token.text.lower() in ["bye", "goodbye"]):
        return "farewell"
    elif any(token.lemma_ in ["thank", "thanks", "thankyou"] for token in doc):
        return "thanks"
    elif "your name" in text.lower():
        return "ask_name"
    else:
        return "unknown"


# Load responses from JSON file
with open('data/packaged/fundamentals.json', 'r', encoding='utf-8') as f:
    RESPONSES = json.load(f)


def respond(intent):
    responses = RESPONSES.get(intent)
    return random.choice(responses)


def print_token_labels(text):
    if DEBUG:
        doc = nlp(text)
        print("Token labels:")
        for token in doc:
            print(f"{token.text}: {token.pos_} ({token.lemma_})")


def main():
    print("Chatbot: Hi! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        # user_input = user_input.strip()
        if user_input.strip().lower() in ["bye", "exit", "quit", "x", "q", ""]:
            print("Chatbot: Goodbye!")
            break
        intent = get_intent(user_input)
        if DEBUG:
            print_token_labels(user_input)
        print("Chatbot:", respond(intent))


if __name__ == "__main__":
    main()
