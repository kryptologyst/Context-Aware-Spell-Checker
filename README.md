# Context-Aware Spell Checker

An intelligent spell checker that uses BERT and context analysis to provide accurate corrections for spelling errors, homophones, and context-sensitive mistakes.

## Features

- **Context-Aware Corrections**: Uses BERT models to understand context and suggest appropriate corrections
- **Homophone Detection**: Identifies and corrects commonly confused words (there/their/they're, to/too/two, etc.)
- **Multiple Interfaces**: Web UI (FastAPI), Streamlit dashboard, and Python API
- **Mock Database**: SQLite database with common misspellings and context examples
- **Text Statistics**: Comprehensive readability and text analysis
- **Configurable**: Flexible configuration system with presets
- **Modern Tech Stack**: Built with latest NLP libraries and best practices

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kryptologyst/Context-Aware-Spell-Checker.git
cd Context-Aware-Spell-Checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

### Basic Usage

```python
from spell_checker import ContextAwareSpellChecker

# Initialize the spell checker
checker = ContextAwareSpellChecker()

# Check text
text = "She went to the sea to meat her friend."
result = checker.correct_text(text)

print(f"Original: {result.original_text}")
print(f"Corrected: {result.corrected_text}")
print(f"Confidence: {result.confidence_score:.2f}")
```

## Web Interfaces

### FastAPI Web App

Start the FastAPI web application:

```bash
python web_app.py
```

Then open your browser to `http://localhost:8000` for a modern web interface.

### Streamlit Dashboard

Start the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

Access the dashboard at `http://localhost:8501` for an interactive analytics interface.

## Features Overview

### Spell Checking Capabilities

- **Spelling Errors**: Detects and corrects misspelled words using BERT
- **Homophones**: Identifies contextually incorrect homophones
- **Grammar Suggestions**: Basic grammar error detection
- **Confidence Scoring**: Provides confidence scores for all corrections

### Text Analysis

- **Readability Metrics**: Flesch Reading Ease, Flesch-Kincaid Grade
- **Text Statistics**: Word count, sentence count, character count
- **Context Analysis**: Analyzes surrounding words for better corrections

### Database Features

- **Common Misspellings**: Pre-populated database with frequent errors
- **Homophone Groups**: Organized groups of commonly confused words
- **Context Examples**: Sample sentences for each correction type
- **Extensible**: Easy to add new misspellings and patterns

## 🔧 Configuration

The application supports flexible configuration through YAML files:

```yaml
model:
  name: "bert-base-uncased"
  device: "auto"
  confidence_threshold: 0.7

database:
  path: "spell_checker.db"
  auto_create: true

spell_check:
  check_spelling: true
  check_homophones: true
  context_window_size: 3
  max_suggestions: 5

ui:
  theme: "light"
  show_confidence: true
  auto_correct: false
```

### Configuration Presets

- **Development**: Optimized for development with faster models
- **Production**: Optimized for production with higher accuracy
- **Testing**: Minimal configuration for testing

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest test_spell_checker.py -v

# Run specific test categories
python -m pytest test_spell_checker.py::TestMockDatabase -v
python -m pytest test_spell_checker.py::TestContextAwareSpellChecker -v
```

## 📁 Project Structure

```
context-aware-spell-checker/
├── spell_checker.py          # Main spell checker implementation
├── web_app.py               # FastAPI web application
├── streamlit_app.py         # Streamlit dashboard
├── config.py                # Configuration management
├── test_spell_checker.py    # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── 0197.py                 # Original implementation
└── spell_checker.db         # SQLite database (auto-created)
```

## API Endpoints

### FastAPI Endpoints

- `GET /` - Web interface
- `POST /api/spell-check` - Spell check text
- `GET /api/health` - Health check
- `GET /api/models` - Available models

### Example API Usage

```python
import requests

# Check spelling via API
response = requests.post('http://localhost:8000/api/spell-check', 
                        json={'text': 'Their going to the store.'})
result = response.json()

print(result['corrected_text'])
print(result['confidence_score'])
```

## Use Cases

- **Content Writing**: Blog posts, articles, documentation
- **Educational**: Learning tools, writing assistance
- **Professional**: Business communications, reports
- **Accessibility**: Assistive technology for writing
- **Research**: Text analysis and correction tools

## Technical Details

### Models Supported

- **BERT Base Uncased**: Default model for context understanding
- **BERT Base Cased**: Case-sensitive variant
- **DistilBERT**: Faster, lighter alternative
- **RoBERTa**: Alternative transformer model

### Dependencies

- **transformers**: Hugging Face transformers library
- **spacy**: Natural language processing
- **torch**: PyTorch for deep learning
- **fastapi**: Modern web framework
- **streamlit**: Interactive dashboard framework
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning utilities

## Performance

- **GPU Support**: Automatic GPU detection and usage
- **Batch Processing**: Efficient processing of multiple texts
- **Caching**: Model and database caching for faster responses
- **Async Support**: Non-blocking API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for the transformers library
- spaCy for NLP capabilities
- The BERT team for the pre-trained models
- The open-source community for various dependencies

## Support

For questions, issues, or contributions:

- Open an issue on GitHub
- Check the documentation
- Review the test cases for usage examples


# Context-Aware-Spell-Checker
