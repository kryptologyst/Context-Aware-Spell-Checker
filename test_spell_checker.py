"""
Comprehensive Test Suite for Context-Aware Spell Checker
"""

import pytest
import unittest
from unittest.mock import Mock, patch
import tempfile
import os
from pathlib import Path

from spell_checker import ContextAwareSpellChecker, MockDatabase, SpellCheckResult

class TestMockDatabase(unittest.TestCase):
    """Test cases for MockDatabase class"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = MockDatabase(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test database initialization"""
        self.assertTrue(os.path.exists(self.temp_db.name))
    
    def test_misspellings_data(self):
        """Test misspellings data population"""
        misspellings = self.db.get_misspellings()
        self.assertGreater(len(misspellings), 0)
        
        # Check specific misspelling
        incorrect_words = [item[0] for item in misspellings]
        self.assertIn("recieve", incorrect_words)
    
    def test_homophones_data(self):
        """Test homophones data population"""
        homophones = self.db.get_homophones()
        self.assertGreater(len(homophones), 0)
        
        # Check specific homophone group
        groups = [item['group'] for item in homophones]
        self.assertIn("there/their/they're", groups)

class TestContextAwareSpellChecker(unittest.TestCase):
    """Test cases for ContextAwareSpellChecker class"""
    
    @patch('spell_checker.spacy.load')
    @patch('spell_checker.AutoTokenizer.from_pretrained')
    @patch('spell_checker.AutoModelForMaskedLM.from_pretrained')
    @patch('spell_checker.pipeline')
    def setUp(self, mock_pipeline, mock_model, mock_tokenizer, mock_spacy):
        """Set up spell checker with mocked dependencies"""
        # Mock the dependencies
        mock_spacy.return_value = Mock()
        mock_tokenizer.return_value = Mock()
        mock_model.return_value = Mock()
        mock_pipeline.return_value = Mock()
        
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        # Initialize spell checker
        self.spell_checker = ContextAwareSpellChecker()
        self.spell_checker.db = MockDatabase(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.temp_db.name)
    
    def test_initialization(self):
        """Test spell checker initialization"""
        self.assertIsNotNone(self.spell_checker)
        self.assertIsNotNone(self.spell_checker.db)
    
    def test_detect_errors_spelling(self):
        """Test spelling error detection"""
        text = "This is a testt sentence."
        errors = self.spell_checker.detect_errors(text)
        
        # Should detect spelling error
        self.assertGreater(len(errors), 0)
        self.assertEqual(errors[0]['type'], 'spelling')
    
    def test_detect_errors_homophone(self):
        """Test homophone error detection"""
        text = "Their going to the store."
        errors = self.spell_checker.detect_errors(text)
        
        # Should detect homophone error
        homophone_errors = [e for e in errors if e['type'] == 'homophone']
        self.assertGreater(len(homophone_errors), 0)
    
    def test_get_context_window(self):
        """Test context window extraction"""
        doc = Mock()
        doc.tokens = [Mock(text=word) for word in "This is a test sentence".split()]
        
        context = self.spell_checker._get_context_window(doc, "test")
        self.assertIn("test", context)
    
    def test_calculate_confidence(self):
        """Test confidence calculation"""
        corrections = [
            {'type': 'spelling'},
            {'type': 'homophone'}
        ]
        
        confidence = self.spell_checker._calculate_confidence(corrections)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_get_text_statistics(self):
        """Test text statistics generation"""
        text = "This is a test sentence. It has multiple sentences!"
        stats = self.spell_checker.get_text_statistics(text)
        
        self.assertIn('word_count', stats)
        self.assertIn('character_count', stats)
        self.assertIn('sentence_count', stats)
        self.assertGreater(stats['word_count'], 0)

class TestSpellCheckResult(unittest.TestCase):
    """Test cases for SpellCheckResult dataclass"""
    
    def test_spell_check_result_creation(self):
        """Test SpellCheckResult creation"""
        result = SpellCheckResult(
            original_text="test text",
            corrected_text="test text",
            suggestions=[],
            confidence_score=0.9,
            error_type="none",
            corrections_made=[]
        )
        
        self.assertEqual(result.original_text, "test text")
        self.assertEqual(result.confidence_score, 0.9)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    @patch('spell_checker.spacy.load')
    @patch('spell_checker.AutoTokenizer.from_pretrained')
    @patch('spell_checker.AutoModelForMaskedLM.from_pretrained')
    @patch('spell_checker.pipeline')
    def test_end_to_end_correction(self, mock_pipeline, mock_model, mock_tokenizer, mock_spacy):
        """Test end-to-end spell correction"""
        # Mock the pipeline to return a prediction
        mock_pipeline.return_value = [
            {'token_str': 'meet', 'score': 0.9},
            {'token_str': 'meat', 'score': 0.1}
        ]
        
        # Mock other dependencies
        mock_spacy.return_value = Mock()
        mock_tokenizer.return_value = Mock()
        mock_model.return_value = Mock()
        
        # Create temporary database
        temp_db = tempfile.NamedTemporaryFile(delete=False)
        temp_db.close()
        
        # Initialize spell checker
        spell_checker = ContextAwareSpellChecker()
        spell_checker.db = MockDatabase(temp_db.name)
        
        # Test correction
        text = "She went to meat her friend."
        result = spell_checker.correct_text(text)
        
        self.assertIsInstance(result, SpellCheckResult)
        self.assertEqual(result.original_text, text)
        
        # Clean up
        os.unlink(temp_db.name)

# Pytest fixtures and tests
@pytest.fixture
def temp_database():
    """Create a temporary database for testing"""
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()
    db = MockDatabase(temp_db.name)
    yield db
    os.unlink(temp_db.name)

@pytest.fixture
def mock_spell_checker():
    """Create a mock spell checker"""
    with patch('spell_checker.spacy.load'), \
         patch('spell_checker.AutoTokenizer.from_pretrained'), \
         patch('spell_checker.AutoModelForMaskedLM.from_pretrained'), \
         patch('spell_checker.pipeline'):
        
        temp_db = tempfile.NamedTemporaryFile(delete=False)
        temp_db.close()
        
        checker = ContextAwareSpellChecker()
        checker.db = MockDatabase(temp_db.name)
        
        yield checker
        
        os.unlink(temp_db.name)

def test_database_misspellings(temp_database):
    """Test database misspellings functionality"""
    misspellings = temp_database.get_misspellings()
    assert len(misspellings) > 0
    assert any("recieve" in item for item in misspellings)

def test_database_homophones(temp_database):
    """Test database homophones functionality"""
    homophones = temp_database.get_homophones()
    assert len(homophones) > 0
    assert any("there/their/they're" in item['group'] for item in homophones)

def test_spell_checker_text_statistics(mock_spell_checker):
    """Test text statistics generation"""
    text = "This is a test sentence."
    stats = mock_spell_checker.get_text_statistics(text)
    
    assert stats['word_count'] == 5
    assert stats['character_count'] == len(text)
    assert stats['sentence_count'] == 1

def test_spell_checker_confidence_calculation(mock_spell_checker):
    """Test confidence calculation"""
    corrections = [
        {'type': 'spelling'},
        {'type': 'homophone'},
        {'type': 'grammar'}
    ]
    
    confidence = mock_spell_checker._calculate_confidence(corrections)
    assert 0.0 <= confidence <= 1.0
    assert confidence == pytest.approx(0.8, rel=1e-1)

# Performance tests
class TestPerformance(unittest.TestCase):
    """Performance tests"""
    
    def test_large_text_processing(self):
        """Test processing of large text"""
        large_text = "This is a test sentence. " * 1000
        
        with patch('spell_checker.spacy.load'), \
             patch('spell_checker.AutoTokenizer.from_pretrained'), \
             patch('spell_checker.AutoModelForMaskedLM.from_pretrained'), \
             patch('spell_checker.pipeline'):
            
            temp_db = tempfile.NamedTemporaryFile(delete=False)
            temp_db.close()
            
            checker = ContextAwareSpellChecker()
            checker.db = MockDatabase(temp_db.name)
            
            # Should not raise an exception
            stats = checker.get_text_statistics(large_text)
            self.assertGreater(stats['word_count'], 1000)
            
            os.unlink(temp_db.name)

# Test configuration
if __name__ == "__main__":
    # Run unittest tests
    unittest.main(verbosity=2)
    
    # Run pytest tests
    pytest.main([__file__, "-v"])
