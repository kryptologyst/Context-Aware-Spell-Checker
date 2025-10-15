#!/usr/bin/env python3
"""
Demonstration script for Context-Aware Spell Checker
Shows all features and capabilities of the modernized spell checker
"""

import time
import json
from pathlib import Path
from spell_checker import ContextAwareSpellChecker
from config import ConfigManager, ConfigPresets

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧠 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demonstrate_basic_spell_checking():
    """Demonstrate basic spell checking functionality"""
    print_header("BASIC SPELL CHECKING DEMONSTRATION")
    
    # Initialize spell checker
    print("🚀 Initializing Context-Aware Spell Checker...")
    checker = ContextAwareSpellChecker()
    
    # Test cases with different types of errors
    test_cases = [
        {
            "text": "She went to the sea to meat her friend.",
            "description": "Homophone error (meat → meet)"
        },
        {
            "text": "Their going to the store to buy there groceries.",
            "description": "Multiple homophone errors (Their → They're, there → their)"
        },
        {
            "text": "I recieve the package yesterday and it was definately worth it.",
            "description": "Spelling errors (recieve → receive, definately → definitely)"
        },
        {
            "text": "The weather is to hot for me to go outside.",
            "description": "Homophone error (to → too)"
        },
        {
            "text": "Its a beautiful day and the sun is shining bright.",
            "description": "Homophone error (Its → It's)"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print_section(f"Test Case {i}: {test_case['description']}")
        
        print(f"📝 Original: {test_case['text']}")
        
        # Perform spell check
        result = checker.correct_text(test_case['text'])
        
        print(f"✅ Corrected: {result.corrected_text}")
        print(f"🎯 Confidence: {result.confidence_score:.2f}")
        
        if result.corrections_made:
            print("🔧 Corrections made:")
            for correction in result.corrections_made:
                print(f"   • {correction['original']} → {correction['corrected']} ({correction['type']})")
        
        # Get text statistics
        stats = checker.get_text_statistics(test_case['text'])
        print(f"📊 Stats: {stats['word_count']} words, {stats['sentence_count']} sentences")
        
        time.sleep(1)  # Pause for readability

def demonstrate_database_features():
    """Demonstrate database features"""
    print_header("DATABASE FEATURES DEMONSTRATION")
    
    checker = ContextAwareSpellChecker()
    db = checker.db
    
    print_section("Common Misspellings Database")
    misspellings = db.get_misspellings()
    print(f"📚 Total misspellings in database: {len(misspellings)}")
    
    print("🔍 Sample misspellings:")
    for incorrect, correct, freq in misspellings[:5]:
        print(f"   • {incorrect} → {correct} (frequency: {freq})")
    
    print_section("Homophone Groups Database")
    homophones = db.get_homophones()
    print(f"📚 Total homophone groups: {len(homophones)}")
    
    print("🔍 Sample homophone groups:")
    for group in homophones[:3]:
        print(f"   • {group['group']}: {', '.join(group['words'])}")
        print(f"     Rules: {group['rules']}")
        print(f"     Example: {group['examples']}")

def demonstrate_text_analysis():
    """Demonstrate text analysis features"""
    print_header("TEXT ANALYSIS DEMONSTRATION")
    
    checker = ContextAwareSpellChecker()
    
    sample_texts = [
        "This is a simple sentence.",
        "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet.",
        "In the realm of artificial intelligence and machine learning, sophisticated algorithms process vast amounts of data to extract meaningful patterns and insights that drive innovation across various industries.",
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print_section(f"Text Analysis {i}")
        print(f"📝 Text: {text}")
        
        stats = checker.get_text_statistics(text)
        
        print("📊 Statistics:")
        print(f"   • Words: {stats['word_count']}")
        print(f"   • Characters: {stats['character_count']}")
        print(f"   • Sentences: {stats['sentence_count']}")
        print(f"   • Flesch Reading Ease: {stats['flesch_reading_ease']:.1f}")
        print(f"   • Flesch-Kincaid Grade: {stats['flesch_kincaid_grade']:.1f}")
        print(f"   • Automated Readability Index: {stats['readability_score']:.1f}")

def demonstrate_configuration():
    """Demonstrate configuration management"""
    print_header("CONFIGURATION MANAGEMENT DEMONSTRATION")
    
    print_section("Default Configuration")
    config_manager = ConfigManager()
    
    print("⚙️ Current Configuration:")
    print(f"   • Model: {config_manager.get_model_config().name}")
    print(f"   • Device: {config_manager.get_model_config().device}")
    print(f"   • Confidence Threshold: {config_manager.get_model_config().confidence_threshold}")
    print(f"   • Database Path: {config_manager.get_database_config().path}")
    print(f"   • Context Window Size: {config_manager.get_spell_check_config().context_window_size}")
    
    print_section("Configuration Presets")
    
    # Development preset
    dev_config = ConfigPresets.development()
    print("🔧 Development Preset:")
    print(f"   • Model: {dev_config.model.name}")
    print(f"   • Device: {dev_config.model.device}")
    print(f"   • Debug Mode: {dev_config.api_debug}")
    
    # Production preset
    prod_config = ConfigPresets.production()
    print("🏭 Production Preset:")
    print(f"   • Model: {prod_config.model.name}")
    print(f"   • Device: {prod_config.model.device}")
    print(f"   • Debug Mode: {prod_config.api_debug}")
    
    # Testing preset
    test_config = ConfigPresets.testing()
    print("🧪 Testing Preset:")
    print(f"   • Model: {test_config.model.name}")
    print(f"   • Device: {test_config.model.device}")
    print(f"   • Debug Mode: {test_config.api_debug}")

def demonstrate_api_features():
    """Demonstrate API features"""
    print_header("API FEATURES DEMONSTRATION")
    
    print_section("Available Models")
    available_models = [
        "bert-base-uncased",
        "bert-base-cased",
        "distilbert-base-uncased",
        "roberta-base"
    ]
    
    print("🤖 Supported Models:")
    for model in available_models:
        print(f"   • {model}")
    
    print_section("API Endpoints")
    endpoints = [
        ("GET /", "Web interface"),
        ("POST /api/spell-check", "Spell check text"),
        ("GET /api/health", "Health check"),
        ("GET /api/models", "Available models")
    ]
    
    print("🌐 API Endpoints:")
    for endpoint, description in endpoints:
        print(f"   • {endpoint} - {description}")
    
    print_section("Example API Usage")
    example_request = {
        "text": "Their going to the store to buy there groceries.",
        "model_name": "bert-base-uncased"
    }
    
    print("📤 Example Request:")
    print(json.dumps(example_request, indent=2))
    
    example_response = {
        "original_text": "Their going to the store to buy there groceries.",
        "corrected_text": "They're going to the store to buy their groceries.",
        "confidence_score": 0.85,
        "corrections_made": [
            {"original": "Their", "corrected": "They're", "type": "homophone"},
            {"original": "there", "corrected": "their", "type": "homophone"}
        ],
        "text_statistics": {
            "word_count": 9,
            "character_count": 50,
            "sentence_count": 1,
            "flesch_reading_ease": 75.2
        }
    }
    
    print("📥 Example Response:")
    print(json.dumps(example_response, indent=2))

def demonstrate_web_interfaces():
    """Demonstrate web interface features"""
    print_header("WEB INTERFACE DEMONSTRATION")
    
    print_section("FastAPI Web App")
    print("🌐 FastAPI Features:")
    print("   • Modern, responsive web interface")
    print("   • Real-time spell checking")
    print("   • Interactive text input")
    print("   • Detailed results display")
    print("   • Confidence scoring")
    print("   • Text statistics")
    print("   • RESTful API endpoints")
    
    print("\n🚀 To start FastAPI app:")
    print("   python web_app.py")
    print("   Then visit: http://localhost:8000")
    
    print_section("Streamlit Dashboard")
    print("📊 Streamlit Features:")
    print("   • Interactive dashboard")
    print("   • Real-time text analysis")
    print("   • Visual statistics")
    print("   • Confidence gauges")
    print("   • Correction type analysis")
    print("   • Sidebar configuration")
    
    print("\n🚀 To start Streamlit app:")
    print("   streamlit run streamlit_app.py")
    print("   Then visit: http://localhost:8501")

def demonstrate_testing():
    """Demonstrate testing capabilities"""
    print_header("TESTING DEMONSTRATION")
    
    print_section("Test Suite Features")
    print("🧪 Test Categories:")
    print("   • Unit tests for all components")
    print("   • Integration tests")
    print("   • Performance tests")
    print("   • Mock database tests")
    print("   • Configuration validation tests")
    print("   • API endpoint tests")
    
    print("\n🔍 Test Coverage:")
    print("   • MockDatabase class")
    print("   • ContextAwareSpellChecker class")
    print("   • SpellCheckResult dataclass")
    print("   • Configuration management")
    print("   • End-to-end workflows")
    
    print("\n🚀 To run tests:")
    print("   python -m pytest test_spell_checker.py -v")
    print("   python -m pytest test_spell_checker.py::TestMockDatabase -v")
    print("   python -m pytest test_spell_checker.py::TestContextAwareSpellChecker -v")

def main():
    """Main demonstration function"""
    print("🎉 CONTEXT-AWARE SPELL CHECKER - COMPLETE DEMONSTRATION")
    print("This script demonstrates all features and capabilities of the modernized spell checker.")
    
    try:
        # Run all demonstrations
        demonstrate_basic_spell_checking()
        demonstrate_database_features()
        demonstrate_text_analysis()
        demonstrate_configuration()
        demonstrate_api_features()
        demonstrate_web_interfaces()
        demonstrate_testing()
        
        print_header("DEMONSTRATION COMPLETE")
        print("🎉 All features have been demonstrated successfully!")
        
        print("\n📋 Next Steps:")
        print("1. Run the basic spell checker: python spell_checker.py")
        print("2. Start the web app: python web_app.py")
        print("3. Start the Streamlit dashboard: streamlit run streamlit_app.py")
        print("4. Run tests: python -m pytest test_spell_checker.py -v")
        print("5. Set up the project: python setup.py")
        
        print("\n📚 For more information, see README.md")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        print("Please check your installation and dependencies.")

if __name__ == "__main__":
    main()
