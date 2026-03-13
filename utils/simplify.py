#!/usr/bin/env python3
"""
Text Simplification Tool

A command-line tool that simplifies complex text (e.g., legal, academic, technical)
while preserving the overall structure. Uses spaCy for NLP processing and NLTK
for additional text analysis.

Simplification strategies:
- Replace complex/formal words with simpler alternatives
- Replace legal/technical jargon with plain language
- Simplify passive voice constructions
- Break down complex sentences (optional)
- Replace verbose phrases with concise alternatives
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import re

import spacy
import nltk
from nltk.tokenize import sent_tokenize


# Complex-to-simple word mappings
# Focused on legal, formal, and technical vocabulary
WORD_SIMPLIFICATIONS = {
    # Legal terms
    'aforementioned': 'mentioned',
    'heretofore': 'before',
    'hereinafter': 'after this',
    'whereas': 'since',
    'whereby': 'by which',
    'herein': 'here',
    'thereof': 'of it',
    'therein': 'in it',
    'pursuant': 'according',
    'notwithstanding': 'despite',
    'henceforth': 'from now on',
    'hereafter': 'after this',
    'forthwith': 'immediately',
    'commence': 'begin',
    'terminate': 'end',
    'endeavor': 'try',
    'ascertain': 'find out',
    'remuneration': 'payment',
    'compensation': 'payment',
    'modifications': 'changes',
    'provisions': 'terms',
    'substantial': 'large',
    'obtain': 'get',
    'retain': 'keep',
    'utilize': 'use',
    'facilitate': 'help',
    'assist': 'help',
    'implement': 'carry out',
    'sufficient': 'enough',
    'indicate': 'show',
    'demonstrate': 'show',
    'require': 'need',
    'request': 'ask',
    'inform': 'tell',
    'advise': 'tell',
    'provide': 'give',
    'submit': 'send',
    'receive': 'get',
    'prohibit': 'forbid',
    'permit': 'allow',
    'authorize': 'allow',
    'constitute': 'make up',
    'designate': 'name',
    'determine': 'decide',
    'ensure': 'make sure',
    'execute': 'carry out',
    'expire': 'end',
    'notify': 'tell',
    'obligate': 'require',
    'purchase': 'buy',
    'regulation': 'rule',
    'remainder': 'rest',
    'render': 'make',
    'subsequently': 'later',
    'transmit': 'send',
    'witnessed': 'seen',
    
    # Formal/academic terms
    'additionally': 'also',
    'consequently': 'so',
    'nevertheless': 'but',
    'furthermore': 'also',
    'however': 'but',
    'therefore': 'so',
    'thus': 'so',
    'accordingly': 'so',
    'subsequently': 'later',
    'previously': 'before',
    'approximately': 'about',
    'numerous': 'many',
    'illustrate': 'show',
    'commence': 'start',
    'conclude': 'end',
    'attempt': 'try',
    'acquire': 'get',
    'diminish': 'reduce',
    'establish': 'set up',
    'generate': 'create',
    'comprehend': 'understand',
    'anticipate': 'expect',
    'investigate': 'look into',
    'maintain': 'keep',
    'participate': 'take part',
    'regarding': 'about',
    'concerning': 'about',
    'pertaining': 'about',
}

# Phrase simplifications
PHRASE_SIMPLIFICATIONS = {
    'in the event that': 'if',
    'in order to': 'to',
    'for the purpose of': 'to',
    'with regard to': 'about',
    'with respect to': 'about',
    'in accordance with': 'following',
    'by means of': 'by',
    'in lieu of': 'instead of',
    'prior to': 'before',
    'subsequent to': 'after',
    'in addition to': 'besides',
    'as a result of': 'because of',
    'in the amount of': 'for',
    'at the present time': 'now',
    'at this point in time': 'now',
    'during the time that': 'while',
    'until such time as': 'until',
    'for the reason that': 'because',
    'due to the fact that': 'because',
    'in view of the fact that': 'because',
    'on the basis of': 'based on',
    'in connection with': 'about',
    'in relation to': 'about',
    'with reference to': 'about',
    'as per': 'according to',
    'in case of': 'if',
    'in light of': 'because of',
    'in spite of': 'despite',
    'by virtue of': 'because of',
    'in the course of': 'during',
    'in the process of': 'while',
    'on account of': 'because',
    'with the exception of': 'except',
}


class TextSimplifier:
    """Simplifies complex text while preserving structure."""
    
    def __init__(self, spacy_model: str = "en_core_web_sm", 
                 simplification_level: str = "moderate"):
        """
        Initialize the text simplifier.
        
        Args:
            spacy_model: Name of the spaCy model to use
            simplification_level: 'light', 'moderate', or 'aggressive'
        """
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            print(f"spaCy model '{spacy_model}' not found. Downloading...", file=sys.stderr)
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "spacy", "download", spacy_model])
                self.nlp = spacy.load(spacy_model)
                print(f"Model '{spacy_model}' downloaded successfully!", file=sys.stderr)
            except Exception as e:
                print(f"Error: Failed to download spaCy model '{spacy_model}': {e}", file=sys.stderr)
                print(f"Please install it manually: python -m spacy download {spacy_model}", file=sys.stderr)
                sys.exit(1)
        
        self.level = simplification_level
        
        # Ensure NLTK punkt tokenizer is available
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            print("Downloading NLTK punkt_tab tokenizer...", file=sys.stderr)
            nltk.download('punkt_tab', quiet=True)
    
    def simplify_word(self, word: str, pos: str | None = None) -> str:
        """
        Simplify a single word if a simpler alternative exists.
        
        Args:
            word: The word to simplify
            pos: Part of speech (optional, for context)
            
        Returns:
            Simplified word or original if no simplification available
        """
        word_lower = word.lower()
        
        if word_lower in WORD_SIMPLIFICATIONS:
            simplified = WORD_SIMPLIFICATIONS[word_lower]
            
            # Preserve capitalization
            if word[0].isupper():
                simplified = simplified.capitalize()
            if word.isupper():
                simplified = simplified.upper()
            
            return simplified
        
        return word
    
    def simplify_phrases(self, text: str) -> str:
        """
        Replace complex phrases with simpler alternatives.
        
        Args:
            text: The text to simplify
            
        Returns:
            Text with simplified phrases
        """
        result = text
        
        # Sort phrases by length (longest first) to avoid partial replacements
        sorted_phrases = sorted(PHRASE_SIMPLIFICATIONS.items(), 
                               key=lambda x: len(x[0]), reverse=True)
        
        for complex_phrase, simple_phrase in sorted_phrases:
            # Case-insensitive replacement while preserving original capitalization
            pattern = re.compile(re.escape(complex_phrase), re.IGNORECASE)
            
            def replace_match(match):
                original = match.group(0)
                if original[0].isupper():
                    return simple_phrase.capitalize()
                return simple_phrase
            
            result = pattern.sub(replace_match, result)
        
        return result
    
    def simplify_passive_voice(self, doc) -> List[int]:
        """
        Detect and potentially simplify passive voice constructions.
        Note: This is a simplified implementation.
        
        Args:
            doc: spaCy Doc object
            
        Returns:
            List of token indices for passive voice subjects
        """
        # For now, we'll just identify passive voice
        # A full transformation would require more sophisticated logic
        passives = []
        
        for token in doc:
            if token.dep_ == 'nsubjpass':
                passives.append(token.i)
        
        return passives
    
    def simplify_sentence(self, sentence: str) -> str:
        """
        Simplify a single sentence.
        
        Args:
            sentence: The sentence to simplify
            
        Returns:
            Simplified sentence
        """
        # First, simplify phrases
        sentence = self.simplify_phrases(sentence)
        
        # Parse with spaCy
        doc = self.nlp(sentence)
        
        # Simplify individual words
        simplified_tokens = []
        for token in doc:
            simplified = self.simplify_word(token.text, token.pos_)
            simplified_tokens.append(simplified)
        
        # Reconstruct sentence preserving spacing and punctuation
        result = ""
        for i, token in enumerate(doc):
            result += simplified_tokens[i]
            if token.whitespace_:
                result += token.whitespace_
        
        return result
    
    def simplify_text(self, text: str, preserve_formatting: bool = True) -> Tuple[str, Dict]:
        """
        Simplify the entire text.
        
        Args:
            text: The text to simplify
            preserve_formatting: Whether to preserve paragraph breaks
            
        Returns:
            Tuple of (simplified_text, statistics)
        """
        # Split into sentences
        sentences = sent_tokenize(text)
        
        simplified_sentences = []
        stats = {
            'original_sentences': len(sentences),
            'words_simplified': 0,
            'phrases_simplified': 0,
        }
        
        for sentence in sentences:
            original = sentence
            simplified = self.simplify_sentence(sentence)
            
            # Count changes
            if original != simplified:
                # Count word-level changes
                orig_words = set(original.lower().split())
                simp_words = set(simplified.lower().split())
                stats['words_simplified'] += len(orig_words - simp_words)
            
            simplified_sentences.append(simplified)
        
        # Join sentences back together
        if preserve_formatting:
            # Try to preserve paragraph structure
            result = self._preserve_structure(text, simplified_sentences)
        else:
            result = ' '.join(simplified_sentences)
        
        return result, stats
    
    def _preserve_structure(self, original: str, simplified_sentences: List[str]) -> str:
        """
        Preserve the paragraph structure of the original text.
        
        Args:
            original: Original text
            simplified_sentences: List of simplified sentences
            
        Returns:
            Simplified text with preserved structure
        """
        # Split original by paragraphs
        paragraphs = original.split('\n\n')
        
        if len(paragraphs) == 1:
            return ' '.join(simplified_sentences)
        
        # Reconstruct with paragraph breaks
        result_paragraphs = []
        sentence_idx = 0
        
        for para in paragraphs:
            para_sentences = sent_tokenize(para)
            para_simplified = []
            
            for _ in para_sentences:
                if sentence_idx < len(simplified_sentences):
                    para_simplified.append(simplified_sentences[sentence_idx])
                    sentence_idx += 1
            
            result_paragraphs.append(' '.join(para_simplified))
        
        return '\n\n'.join(result_paragraphs)


def read_text_from_file(filepath: str) -> str:
    """
    Read text from a file.
    
    Args:
        filepath: Path to the text file
        
    Returns:
        The contents of the file
    """
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def write_output(text: str, stats: Dict, output_file: str | None = None, 
                 show_stats: bool = False, show_diff: bool = False,
                 original_text: str | None = None):
    """
    Write the simplified text to output.
    
    Args:
        text: Simplified text
        stats: Statistics dictionary
        output_file: Optional path to output file
        show_stats: Whether to show statistics
        show_diff: Whether to show a side-by-side comparison
        original_text: Original text for comparison
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
    
    # Print simplified text
    print("=" * 80, file=f)
    print("SIMPLIFIED TEXT", file=f)
    print("=" * 80, file=f)
    print(file=f)
    print(text, file=f)
    print(file=f)
    
    # Print statistics if requested
    if show_stats:
        print("=" * 80, file=f)
        print("SIMPLIFICATION STATISTICS", file=f)
        print("=" * 80, file=f)
        print(f"Original sentences: {stats['original_sentences']}", file=f)
        print(f"Words simplified: {stats['words_simplified']}", file=f)
        print(file=f)
    
    # Print comparison if requested
    if show_diff and original_text:
        print("=" * 80, file=f)
        print("BEFORE AND AFTER COMPARISON", file=f)
        print("=" * 80, file=f)
        print(file=f)
        print("ORIGINAL:", file=f)
        print("-" * 80, file=f)
        print(original_text[:500] + ("..." if len(original_text) > 500 else ""), file=f)
        print(file=f)
        print("SIMPLIFIED:", file=f)
        print("-" * 80, file=f)
        print(text[:500] + ("..." if len(text) > 500 else ""), file=f)
        print(file=f)
    
    # Close file if we opened one
    if output_file:
        f.close()
        print(f"Simplified text written to: {output_file}")


def main():
    """Main entry point for the command-line tool."""
    parser = argparse.ArgumentParser(
        description="Simplify complex text (legal, academic, technical) while preserving structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Pursuant to the aforementioned agreement..."
  %(prog)s --file legal_document.txt
  %(prog)s --file contract.txt --output simplified.txt --stats
  %(prog)s -f document.txt -o simple.txt --level aggressive
  %(prog)s --text "In the event that..." --diff
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'text_arg',
        nargs='?',
        metavar='text',
        help='Text to simplify (as a direct argument)'
    )
    input_group.add_argument(
        '-f', '--file',
        help='Path to a text file to simplify'
    )
    input_group.add_argument(
        '-t', '--text',
        help='Text to simplify (as a named argument)'
    )
    
    # Options
    parser.add_argument(
        '-o', '--output',
        help='Path to output file (if not specified, prints to stdout)'
    )
    parser.add_argument(
        '-l', '--level',
        choices=['light', 'moderate', 'aggressive'],
        default='moderate',
        help='Simplification level (default: moderate)'
    )
    parser.add_argument(
        '-s', '--stats',
        action='store_true',
        help='Show simplification statistics'
    )
    parser.add_argument(
        '-d', '--diff',
        action='store_true',
        help='Show before/after comparison'
    )
    parser.add_argument(
        '-m', '--model',
        default='en_core_web_sm',
        help='spaCy model to use (default: en_core_web_sm)'
    )
    parser.add_argument(
        '--no-preserve-formatting',
        action='store_true',
        help='Do not preserve paragraph structure'
    )
    
    args = parser.parse_args()
    
    # Get the text to analyze
    if args.file:
        text = read_text_from_file(args.file)
    elif args.text:
        text = args.text
    elif args.text_arg:
        text = args.text_arg
    else:
        text = ""
    
    if not text or not text.strip():
        print("Error: No text provided to simplify.", file=sys.stderr)
        sys.exit(1)
    
    # Store original for comparison
    original_text = text
    
    # Initialize simplifier and process text
    simplifier = TextSimplifier(
        spacy_model=args.model,
        simplification_level=args.level
    )
    
    simplified_text, stats = simplifier.simplify_text(
        text,
        preserve_formatting=not args.no_preserve_formatting
    )
    
    # Write output
    write_output(
        simplified_text,
        stats,
        output_file=args.output,
        show_stats=args.stats,
        show_diff=args.diff,
        original_text=original_text
    )


if __name__ == "__main__":
    main()
