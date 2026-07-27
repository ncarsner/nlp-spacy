#!/usr/bin/env python3
"""
Sentence Type Classifier

A command-line tool that classifies sentences as:
- Declarative: Makes a statement
- Interrogative: Asks a question
- Imperative: Gives a command or request
- Exclamatory: Expresses strong emotion

Uses spaCy for NLP processing and NLTK for tokenization.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

import spacy
import nltk
from nltk.tokenize import sent_tokenize
import docx


class SentenceTypeClassifier:
    """Classifies sentences into declarative, interrogative, imperative, and exclamatory types."""
    
    def __init__(self, spacy_model: str = "en_core_web_sm"):
        """
        Initialize the classifier with a spaCy model.
        
        Args:
            spacy_model: Name of the spaCy model to use
        """
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            print(f"Error: spaCy model '{spacy_model}' not found.", file=sys.stderr)
            print(f"Please install it with: python -m spacy download {spacy_model}", file=sys.stderr)
            sys.exit(1)
        
        # Ensure NLTK punkt tokenizer is available
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            print("Downloading NLTK punkt_tab tokenizer...", file=sys.stderr)
            nltk.download('punkt_tab', quiet=True)
    
    def classify_sentence(self, sentence: str) -> str:
        """
        Classify a single sentence into one of four types.
        
        Args:
            sentence: The sentence to classify
            
        Returns:
            The sentence type: 'exclamatory', 'interrogative', 'imperative', or 'declarative'
        """
        sentence = sentence.strip()
        if not sentence:
            return 'unknown'
        
        # Check for exclamatory (ends with !)
        if sentence.endswith('!'):
            return 'exclamatory'
        
        # Check for interrogative (ends with ?)
        if sentence.endswith('?'):
            return 'interrogative'
        
        # Use spaCy to analyze the sentence structure
        doc = self.nlp(sentence)
        
        # Check for imperative sentences
        # Imperative sentences typically:
        # 1. Start with a base form verb (VB)
        # 2. Have no explicit subject or the subject is implied "you"
        # 3. Give commands or requests
        
        if len(doc) > 0:
            # Get the first token (ignoring leading punctuation/whitespace)
            first_token = None
            for token in doc:
                if token.pos_ not in ['PUNCT', 'SPACE']:
                    first_token = token
                    break
            
            if first_token:
                # Check if starts with base verb (VB) - strong indicator of imperative
                if first_token.tag_ == 'VB':
                    # Additional check: imperative sentences often lack a subject
                    has_subject = any(token.dep_ in ['nsubj', 'nsubjpass'] for token in doc)
                    if not has_subject:
                        return 'imperative'
                
                # Check for imperative with "please"
                if first_token.text.lower() == 'please':
                    return 'imperative'
                
                # Check for "let's" or "let us" constructions
                if first_token.text.lower() in ['let', "let's"]:
                    return 'imperative'
        
        # Default to declarative
        return 'declarative'
    
    def classify_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Classify all sentences in a block of text.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of tuples (sentence, sentence_type)
        """
        # Use NLTK to tokenize into sentences
        sentences = sent_tokenize(text)
        
        results = []
        for sentence in sentences:
            sentence_type = self.classify_sentence(sentence)
            results.append((sentence, sentence_type))
        
        return results


def read_text_from_file(filepath: str) -> str:
    """
    Read text from a file. Supports plain text (.txt) and Word documents (.docx).
    
    Args:
        filepath: Path to the text or Word document file
        
    Returns:
        The contents of the file as a UTF-8 string
    """
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if path.suffix.lower() == '.docx':
        try:
            doc = docx.Document(str(path))
            return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            print(f"Error reading Word document '{filepath}': {e}", file=sys.stderr)
            sys.exit(1)
    
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def print_results(results: List[Tuple[str, str]], show_stats: bool = False, output_file: str | None = None) -> None:
    """
    Print the classification results.
    
    Args:
        results: List of (sentence, sentence_type) tuples
        show_stats: Whether to show statistics summary
        output_file: Optional path to write output to a file
    """
    # Determine output destination
    if output_file:
        try:
            f = open(output_file, 'w', encoding='utf-8')
        except Exception as e:
            print(f"Error: Could not open output file '{output_file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        f = sys.stdout
    
    print("\n" + "=" * 80, file=f)
    print("SENTENCE TYPE ANALYSIS", file=f)
    print("=" * 80 + "\n", file=f)
    
    # Count sentence types
    type_counts = {
        'declarative': 0,
        'interrogative': 0,
        'imperative': 0,
        'exclamatory': 0
    }
    
    for i, (sentence, sentence_type) in enumerate(results, 1):
        type_counts[sentence_type] = type_counts.get(sentence_type, 0) + 1
        
        # Print with color-coded labels
        type_label = sentence_type.upper()
        print(f"[{i}] {type_label}", file=f)
        print(f"    {sentence}", file=f)
        print(file=f)
    
    if show_stats:
        print("=" * 80, file=f)
        print("STATISTICS", file=f)
        print("=" * 80, file=f)
        total = len(results)
        for stype in ['declarative', 'interrogative', 'imperative', 'exclamatory']:
            count = type_counts[stype]
            percentage = (count / total * 100) if total > 0 else 0
            print(f"{stype.capitalize():15} {count:3d} ({percentage:5.1f}%)", file=f)
        print(f"{'Total':15} {total:3d}", file=f)
        print(file=f)
    
    # Close file if we opened one
    if output_file:
        f.close()
        print(f"Results written to: {output_file}")


def main():
    """Main entry point for the command-line tool."""
    parser = argparse.ArgumentParser(
        description="Classify sentences as declarative, interrogative, imperative, or exclamatory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello! How are you? Please sit down. I am fine."
  %(prog)s --file speech.txt
  %(prog)s --file speech.txt --stats
  %(prog)s --file speech.txt --stats --output results.txt
  %(prog)s --file document.docx
  %(prog)s --file document.docx --stats
  %(prog)s --text "What is your name?" -o output.txt
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'text',
        nargs='?',
        help='Text to analyze (as a direct argument)'
    )
    input_group.add_argument(
        '-f', '--file',
        help='Path to a text or Word document (.docx) file to analyze'
    )
    input_group.add_argument(
        '-t', '--text',
        help='Text to analyze (as a named argument)'
    )
    
    # Options
    parser.add_argument(
        '-s', '--stats',
        action='store_true',
        help='Show statistics summary'
    )
    parser.add_argument(
        '-o', '--output',
        help='Path to output file (if not specified, prints to stdout)'
    )
    parser.add_argument(
        '-m', '--model',
        default='en_core_web_sm',
        help='spaCy model to use (default: en_core_web_sm)'
    )
    
    args = parser.parse_args()
    
    # Get the text to analyze
    if args.file:
        text = read_text_from_file(args.file)
    elif args.text:
        text = args.text
    else:
        text = args.text if args.text else ""
    
    if not text or not text.strip():
        print("Error: No text provided to analyze.", file=sys.stderr)
        sys.exit(1)
    
    # Initialize classifier and process text
    classifier = SentenceTypeClassifier(spacy_model=args.model)
    results = classifier.classify_text(text)
    
    # Print results
    print_results(results, show_stats=args.stats, output_file=args.output)


if __name__ == "__main__":
    main()
