"""
Context-Aware Spell Checker
A modern implementation using multiple NLP techniques for comprehensive spell checking.
"""

import json
import sqlite3
import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path

import torch
import spacy
import nltk
from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
import wordfreq
import enchant

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

@dataclass
class SpellCheckResult:
    """Result of spell checking operation"""
    original_text: str
    corrected_text: str
    suggestions: List[Dict[str, Any]]
    confidence_score: float
    error_type: str
    corrections_made: List[Dict[str, str]]

class MockDatabase:
    """Mock database for storing common misspellings and context examples"""
    
    def __init__(self, db_path: str = "spell_checker.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_sample_data()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Common misspellings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS misspellings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incorrect_word TEXT NOT NULL,
                correct_word TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                context_examples TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Homophones table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS homophones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_group TEXT NOT NULL,
                words TEXT NOT NULL,
                context_rules TEXT,
                examples TEXT
            )
        ''')
        
        # Context patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS context_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL,
                word TEXT NOT NULL,
                confidence REAL,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def populate_sample_data(self):
        """Populate database with sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sample misspellings
        misspellings = [
            ("recieve", "receive", 5, "I will recieve the package tomorrow."),
            ("seperate", "separate", 3, "Please seperate the items."),
            ("definately", "definitely", 4, "I will definately be there."),
            ("occured", "occurred", 2, "The event occured yesterday."),
            ("accomodate", "accommodate", 3, "We can accomodate your request."),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO misspellings (incorrect_word, correct_word, frequency, context_examples)
            VALUES (?, ?, ?, ?)
        ''', misspellings)
        
        # Sample homophones
        homophones = [
            ("there/their/they're", "there,their,they're", "location,possession,contraction", "There is a book. Their book is red. They're coming."),
            ("to/too/two", "to,too,two", "preposition,adverb,number", "Go to the store. It's too hot. Two people came."),
            ("your/you're", "your,you're", "possession,contraction", "Your car is nice. You're welcome."),
            ("its/it's", "its,it's", "possession,contraction", "The dog wagged its tail. It's raining."),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO homophones (word_group, words, context_rules, examples)
            VALUES (?, ?, ?, ?)
        ''', homophones)
        
        conn.commit()
        conn.close()
    
    def get_misspellings(self) -> List[Tuple[str, str, int]]:
        """Get all misspellings from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT incorrect_word, correct_word, frequency FROM misspellings')
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_homophones(self) -> List[Dict[str, str]]:
        """Get all homophone groups from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT word_group, words, context_rules, examples FROM homophones')
        results = []
        for row in cursor.fetchall():
            results.append({
                'group': row[0],
                'words': row[1].split(','),
                'rules': row[2],
                'examples': row[3]
            })
        conn.close()
        return results

class ContextAwareSpellChecker:
    """Modern context-aware spell checker using multiple techniques"""
    
    def __init__(self, model_name: str = "bert-base-uncased"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize components
        self.db = MockDatabase()
        self.nlp = spacy.load("en_core_web_sm")
        self.enchant_dict = enchant.Dict("en_US")
        
        # Initialize BERT model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(model_name)
        self.fill_mask_pipeline = pipeline(
            "fill-mask",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1
        )
        
        # Load word lists
        self.english_words = set(nltk.corpus.words.words())
        
        # Initialize TF-IDF for context similarity
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        print(f"✅ Context-Aware Spell Checker initialized with {model_name}")
        print(f"🔧 Device: {self.device}")
    
    def detect_errors(self, text: str) -> List[Dict[str, Any]]:
        """Detect various types of errors in text"""
        errors = []
        doc = self.nlp(text)
        
        for token in doc:
            if token.is_alpha:
                # Check spelling
                if not self.enchant_dict.check(token.text.lower()):
                    errors.append({
                        'word': token.text,
                        'position': token.idx,
                        'type': 'spelling',
                        'suggestions': self.enchant_dict.suggest(token.text.lower())
                    })
                
                # Check homophones
                homophone_error = self._check_homophones(token.text, doc)
                if homophone_error:
                    errors.append(homophone_error)
        
        return errors
    
    def _check_homophones(self, word: str, doc) -> Optional[Dict[str, Any]]:
        """Check for homophone errors"""
        homophone_groups = self.db.get_homophones()
        
        for group in homophone_groups:
            if word.lower() in group['words']:
                # Analyze context to determine correct usage
                context = self._get_context_window(doc, word)
                correct_word = self._analyze_homophone_context(word, context, group)
                
                if correct_word and correct_word.lower() != word.lower():
                    return {
                        'word': word,
                        'position': next(token.idx for token in doc if token.text == word),
                        'type': 'homophone',
                        'suggestions': [correct_word],
                        'confidence': 0.8
                    }
        
        return None
    
    def _get_context_window(self, doc, target_word: str, window_size: int = 3) -> str:
        """Get context window around target word"""
        words = [token.text for token in doc]
        try:
            idx = words.index(target_word)
            start = max(0, idx - window_size)
            end = min(len(words), idx + window_size + 1)
            return ' '.join(words[start:end])
        except ValueError:
            return ""
    
    def _analyze_homophone_context(self, word: str, context: str, group: Dict) -> Optional[str]:
        """Analyze context to determine correct homophone"""
        # Simple rule-based approach (can be enhanced with ML)
        context_lower = context.lower()
        
        if word.lower() == "there":
            if any(pos in context_lower for pos in ["is", "are", "was", "were"]):
                return "there"
        elif word.lower() == "their":
            if any(noun in context_lower for noun in ["book", "car", "house", "name"]):
                return "their"
        elif word.lower() == "they're":
            if any(verb in context_lower for verb in ["coming", "going", "here", "there"]):
                return "they're"
        
        return None
    
    def correct_text(self, text: str) -> SpellCheckResult:
        """Main correction function"""
        errors = self.detect_errors(text)
        corrected_text = text
        corrections_made = []
        
        for error in errors:
            if error['type'] == 'spelling':
                # Use BERT for context-aware spelling correction
                suggestion = self._bert_correct_spelling(text, error['word'], error['position'])
                if suggestion:
                    corrected_text = corrected_text.replace(error['word'], suggestion)
                    corrections_made.append({
                        'original': error['word'],
                        'corrected': suggestion,
                        'type': 'spelling'
                    })
            
            elif error['type'] == 'homophone':
                suggestion = error['suggestions'][0]
                corrected_text = corrected_text.replace(error['word'], suggestion)
                corrections_made.append({
                    'original': error['word'],
                    'corrected': suggestion,
                    'type': 'homophone'
                })
        
        # Calculate confidence score
        confidence = self._calculate_confidence(corrections_made)
        
        return SpellCheckResult(
            original_text=text,
            corrected_text=corrected_text,
            suggestions=errors,
            confidence_score=confidence,
            error_type="mixed",
            corrections_made=corrections_made
        )
    
    def _bert_correct_spelling(self, text: str, word: str, position: int) -> Optional[str]:
        """Use BERT to correct spelling errors"""
        try:
            # Create masked sentence
            masked_text = text[:position] + "[MASK]" + text[position + len(word):]
            
            # Get predictions
            predictions = self.fill_mask_pipeline(masked_text, top_k=5)
            
            # Filter predictions to exclude the original incorrect word
            valid_predictions = [p for p in predictions if p['token_str'].lower() != word.lower()]
            
            if valid_predictions:
                return valid_predictions[0]['token_str']
            
        except Exception as e:
            print(f"Error in BERT correction: {e}")
        
        return None
    
    def _calculate_confidence(self, corrections: List[Dict]) -> float:
        """Calculate confidence score for corrections"""
        if not corrections:
            return 1.0
        
        # Simple confidence calculation based on correction types
        confidence_scores = []
        for correction in corrections:
            if correction['type'] == 'spelling':
                confidence_scores.append(0.9)
            elif correction['type'] == 'homophone':
                confidence_scores.append(0.8)
            else:
                confidence_scores.append(0.7)
        
        return sum(confidence_scores) / len(confidence_scores)
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """Get comprehensive text statistics"""
        return {
            'word_count': len(text.split()),
            'character_count': len(text),
            'sentence_count': textstat.sentence_count(text),
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'readability_score': textstat.automated_readability_index(text)
        }

def main():
    """Main function to demonstrate the spell checker"""
    print("🚀 Initializing Context-Aware Spell Checker...")
    
    # Initialize spell checker
    checker = ContextAwareSpellChecker()
    
    # Test cases
    test_cases = [
        "She went to the sea to meat her friend.",
        "Their going to the store to buy there groceries.",
        "I recieve the package yesterday and it was definately worth it.",
        "The weather is to hot for me to go outside.",
        "Its a beautiful day and the sun is shining bright."
    ]
    
    print("\n" + "="*60)
    print("🧪 TESTING CONTEXT-AWARE SPELL CHECKER")
    print("="*60)
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Original: {test_text}")
        
        result = checker.correct_text(test_text)
        
        print(f"Corrected: {result.corrected_text}")
        print(f"Confidence: {result.confidence_score:.2f}")
        
        if result.corrections_made:
            print("Corrections made:")
            for correction in result.corrections_made:
                print(f"  • {correction['original']} → {correction['corrected']} ({correction['type']})")
        
        # Get text statistics
        stats = checker.get_text_statistics(test_text)
        print(f"Text Statistics: {stats['word_count']} words, {stats['sentence_count']} sentences")
        print("-" * 40)

if __name__ == "__main__":
    main()
