# import pytest
from unittest.mock import Mock, patch, mock_open
# from collections import Counter
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.pdf_reader import get_common_words_from_pdf


class TestPDFReader:
    """Test suite for pdf_reader.py"""

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_get_common_words_basic(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test basic functionality of get_common_words_from_pdf"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "Hello world hello"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=2)
        
        # Verify
        assert len(result) > 0
        assert all(isinstance(item, tuple) for item in result)
        assert all(len(item) == 2 for item in result)

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_stopwords_removal(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that stopwords are properly removed"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "the cat and the dog"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = ["the", "and"]
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=10)
        words = [word for word, count in result]
        
        # Verify stopwords are not in result
        assert "the" not in words
        assert "and" not in words

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_custom_stop_words(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that custom stop words are excluded"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "cat dog bird cat dog bird"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test with custom stop words
        result = get_common_words_from_pdf("test.pdf", num_words=10, 
                                          custom_stop_words=["cat"])
        words = [word for word, count in result]
        
        # Verify custom stopword is excluded
        assert "cat" not in words

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_word_counting(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that word counting is accurate"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "apple apple apple banana banana"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=2)
        
        # Verify counts
        result_dict = dict(result)
        assert result_dict.get("apple", 0) == 3
        assert result_dict.get("banana", 0) == 2

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_case_insensitivity(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that word counting is case-insensitive"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "Hello HELLO hello"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=5)
        result_dict = dict(result)
        
        # All variations should be counted as one word
        assert result_dict.get("hello", 0) == 3

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_punctuation_removal(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that punctuation is removed"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "Hello, world! How are you?"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=10)
        words = [word for word, count in result]
        
        # Words should not contain punctuation
        assert all(',' not in word for word in words)
        assert all('!' not in word for word in words)
        assert all('?' not in word for word in words)

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_num_words_parameter(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that num_words parameter limits results"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "one two three four five six seven"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=3)
        
        # Should return at most 3 words
        assert len(result) <= 3

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_multiple_pages(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test processing multiple PDF pages"""
        # Setup mock
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "apple banana"
        
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "apple cherry"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page1, mock_page2]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=10)
        result_dict = dict(result)
        
        # Apple appears on both pages
        assert result_dict.get("apple", 0) == 2

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_single_char_removal(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that single character words are removed"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "a b c hello world i j k"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=10)
        words = [word for word, count in result]
        
        # Single characters should be filtered out
        assert all(len(word) > 1 for word in words)

    @patch('utils.pdf_reader.stopwords')
    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    @patch('pypdf.PdfReader')
    def test_digit_removal(self, mock_pdf_reader, mock_file, mock_stopwords):
        """Test that pure digit words are removed"""
        # Setup mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "hello 123 world 456 test"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        mock_stopwords.words.return_value = []
        
        # Test
        result = get_common_words_from_pdf("test.pdf", num_words=10)
        words = [word for word, count in result]
        
        # Pure digits should be filtered out
        assert "123" not in words
        assert "456" not in words
