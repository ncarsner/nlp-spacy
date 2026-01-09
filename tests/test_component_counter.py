import pytest
import spacy
from collections import Counter
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.component_counter import phrases


class TestComponentCounter:
    """Test suite for component_counter.py"""

    @pytest.fixture(scope="class")
    def nlp(self):
        """Load spaCy model once for all tests"""
        return spacy.load("en_core_web_sm")

    def test_phrases_exist(self):
        """Test that phrases list is not empty"""
        assert len(phrases) > 0

    def test_phrases_are_strings(self):
        """Test that all phrases are strings"""
        assert all(isinstance(phrase, str) for phrase in phrases)

    def test_spacy_processing(self, nlp):
        """Test that spaCy can process all phrases"""
        for phrase in phrases:
            doc = nlp(phrase)
            assert len(doc) > 0

    def test_token_filtering(self, nlp):
        """Test that punctuation filtering works"""
        test_phrase = "Hello, world!"
        doc = nlp(test_phrase)
        tokens_no_punct = [token for token in doc if token.pos_ != "PUNCT"]
        
        # Should have 2 tokens (Hello, world) after filtering
        assert len(tokens_no_punct) == 2
        assert all(token.pos_ != "PUNCT" for token in tokens_no_punct)

    def test_pos_counting(self, nlp):
        """Test POS tag counting works correctly"""
        test_phrase = "The cat sat on the mat."
        doc = nlp(test_phrase)
        tokens_no_punct = [token for token in doc if token.pos_ != "PUNCT"]
        pos_counts = Counter(token.pos_ for token in tokens_no_punct)
        
        assert len(pos_counts) > 0
        assert sum(pos_counts.values()) == len(tokens_no_punct)

    def test_lemma_counting(self, nlp):
        """Test lemma counting works correctly"""
        test_phrase = "The cats are running quickly."
        doc = nlp(test_phrase)
        tokens_no_punct = [token for token in doc if token.pos_ != "PUNCT"]
        lemma_counts = Counter(token.lemma_ for token in tokens_no_punct)
        
        assert len(lemma_counts) > 0
        assert sum(lemma_counts.values()) == len(tokens_no_punct)

    def test_token_attributes(self, nlp):
        """Test that expected token attributes are available"""
        test_phrase = "John lives in New York."
        doc = nlp(test_phrase)
        
        for token in doc:
            assert hasattr(token, 'text')
            assert hasattr(token, 'pos_')
            assert hasattr(token, 'lemma_')
            assert hasattr(token, 'dep_')
            assert hasattr(token, 'head')
            assert hasattr(token, 'ent_type_')

    def test_entity_recognition(self, nlp):
        """Test named entity recognition"""
        test_phrase = "Apple Inc. is located in California."
        doc = nlp(test_phrase)
        entities = [token for token in doc if token.ent_type_]
        
        # Should find at least one entity (Apple or California)
        assert len(entities) > 0

    def test_dependency_parsing(self, nlp):
        """Test dependency parsing works"""
        test_phrase = "I love Python."
        doc = nlp(test_phrase)
        
        # Find the ROOT token
        root_tokens = [token for token in doc if token.dep_ == "ROOT"]
        assert len(root_tokens) == 1
        assert root_tokens[0].text.lower() == "love"

    def test_most_common_extraction(self, nlp):
        """Test that most_common works on Counter objects"""
        test_phrase = "The dog and the cat and the bird."
        doc = nlp(test_phrase)
        tokens_no_punct = [token for token in doc if token.pos_ != "PUNCT"]
        pos_counts = Counter(token.pos_ for token in tokens_no_punct)
        
        most_common = pos_counts.most_common(1)
        assert len(most_common) > 0
        assert isinstance(most_common[0], tuple)
        assert len(most_common[0]) == 2
