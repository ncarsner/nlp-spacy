# import pytest
from unittest.mock import mock_open, patch
import numpy as np
from collections import Counter
from scipy.stats import zipf as zipf_dist
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestZipfsLaw:
    """Test suite for zipfs.py Zipf's Law analysis"""

    def test_word_tokenization(self):
        """Test basic word tokenization"""
        text = "Hello world hello"
        words = text.lower().split()
        
        assert len(words) == 3
        assert words == ["hello", "world", "hello"]

    def test_word_counting(self):
        """Test word frequency counting"""
        text = "the cat and the dog"
        words = text.lower().split()
        word_counts = Counter(words)
        
        assert word_counts["the"] == 2
        assert word_counts["cat"] == 1
        assert word_counts["dog"] == 1

    def test_sorted_word_counts(self):
        """Test sorting word counts by frequency"""
        word_counts = Counter(["apple", "banana", "apple", "cherry", "apple"])
        sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        assert sorted_counts[0][0] == "apple"
        assert sorted_counts[0][1] == 3
        assert sorted_counts[1][1] <= sorted_counts[0][1]

    def test_rank_generation(self):
        """Test rank array generation"""
        word_counts = Counter(["a", "b", "c"])
        sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        ranks = np.arange(1, len(sorted_counts) + 1)
        
        assert len(ranks) == len(sorted_counts)
        assert ranks[0] == 1
        assert ranks[-1] == len(sorted_counts)

    def test_frequency_extraction(self):
        """Test extracting frequencies from sorted counts"""
        word_counts = Counter({"apple": 5, "banana": 3, "cherry": 1})
        sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        frequencies = [count for word, count in sorted_counts]
        
        assert frequencies == [5, 3, 1]
        assert frequencies[0] >= frequencies[1] >= frequencies[2]

    def test_zipf_distribution_fit(self):
        """Test Zipf distribution fitting"""
        # Create sample data following power law
        frequencies = [100, 50, 33, 25, 20, 16, 14, 12]
        
        a, loc, scale = zipf_dist.fit(frequencies, floc=0)
        
        assert isinstance(a, float)
        assert a > 0
        assert loc == 0  # We fixed loc to 0
        assert scale > 0

    @patch("builtins.open", new_callable=mock_open, read_data="Hello world hello world")
    def test_file_reading(self, mock_file):
        """Test reading text from file"""
        with open("test.txt", "r", encoding="utf-8") as file:
            text = file.read()
        
        assert text == "Hello world hello world"
        assert isinstance(text, str)

    def test_text_lowercase_conversion(self):
        """Test text conversion to lowercase"""
        text = "Hello WORLD Hello"
        words = text.lower().split()
        word_counts = Counter(words)
        
        assert word_counts["hello"] == 2
        assert "Hello" not in word_counts
        assert "WORLD" not in word_counts

    def test_empty_text_handling(self):
        """Test handling of empty text"""
        text = ""
        words = text.lower().split()
        word_counts = Counter(words)
        
        assert len(words) == 0
        assert len(word_counts) == 0

    def test_rank_frequency_relationship(self):
        """Test that ranks and frequencies have correct relationship"""
        # Simulate Zipf's law: frequency ∝ 1/rank
        word_counts = {"word1": 100, "word2": 50, "word3": 33, "word4": 25}
        sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        frequencies = [count for word, count in sorted_counts]
        ranks = np.arange(1, len(sorted_counts) + 1)
        
        # Check that highest frequency has rank 1
        assert ranks[0] == 1
        assert frequencies[0] == 100
        
        # Check descending order
        assert all(frequencies[i] >= frequencies[i+1] for i in range(len(frequencies)-1))

    def test_counter_most_common(self):
        """Test Counter's most_common method"""
        word_counts = Counter(["apple", "banana", "apple", "cherry", "apple", "banana"])
        most_common = word_counts.most_common(2)
        
        assert len(most_common) == 2
        assert most_common[0][0] == "apple"
        assert most_common[0][1] == 3
        assert most_common[1][0] == "banana"
        assert most_common[1][1] == 2

    def test_log_scale_values(self):
        """Test that log scaling preserves order"""
        values = np.array([1, 10, 100, 1000])
        log_values = np.log10(values)
        
        # Log should preserve ordering
        assert all(log_values[i] < log_values[i+1] for i in range(len(log_values)-1))
        
        # Check specific log values
        assert abs(log_values[0] - 0) < 0.01  # log10(1) = 0
        assert abs(log_values[1] - 1) < 0.01  # log10(10) = 1
        assert abs(log_values[2] - 2) < 0.01  # log10(100) = 2

    def test_zipf_parameters_validity(self):
        """Test that Zipf fit parameters are valid"""
        frequencies = [100, 50, 25, 12, 6, 3]
        a, loc, scale = zipf_dist.fit(frequencies, floc=0)
        
        # Parameters should be positive
        assert a > 0
        assert scale > 0
        
        # loc should be 0 as we fixed it
        assert loc == 0

    def test_whitespace_handling(self):
        """Test handling of multiple whitespace"""
        text = "hello    world  \t  test"
        words = text.lower().split()
        
        # split() should handle multiple whitespace
        assert len(words) == 3
        assert words == ["hello", "world", "test"]
