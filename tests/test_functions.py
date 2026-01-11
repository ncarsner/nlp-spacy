from utils.functions import remove_punctuation


class TestFunctions:
    """Test suite for functions.py utilities"""

    def test_remove_punctuation_basic(self):
        """Test basic punctuation removal"""
        text = "Hello, world!"
        result = remove_punctuation(text)
        assert result == "Hello world"

    def test_remove_punctuation_all_types(self):
        """Test removal of all punctuation types"""
        text = "Hello! How are you? I'm fine, thanks. #winning @home"
        result = remove_punctuation(text)
        assert "!" not in result
        assert "?" not in result
        assert "," not in result
        assert "." not in result
        assert "'" not in result
        assert "#" not in result
        assert "@" not in result

    def test_remove_punctuation_empty_string(self):
        """Test with empty string"""
        result = remove_punctuation("")
        assert result == ""

    def test_remove_punctuation_no_punctuation(self):
        """Test with text that has no punctuation"""
        text = "Hello world"
        result = remove_punctuation(text)
        assert result == text

    def test_remove_punctuation_only_punctuation(self):
        """Test with only punctuation"""
        text = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/"
        result = remove_punctuation(text)
        assert result == ""

    def test_remove_punctuation_preserves_numbers(self):
        """Test that numbers are preserved"""
        text = "Price: $100.50"
        result = remove_punctuation(text)
        assert "100" in result
        assert "50" in result

    def test_remove_punctuation_preserves_whitespace(self):
        """Test that whitespace is preserved"""
        text = "Hello,   world!  How are you?"
        result = remove_punctuation(text)
        assert "   " in result  # Multiple spaces preserved
        assert "  " in result
