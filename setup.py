#!/usr/bin/env python3
"""
Setup script for Context-Aware Spell Checker
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("⚠️  Warning: spaCy model download failed. You may need to install it manually.")
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data", "config"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def create_config_files():
    """Create default configuration files"""
    config_content = """# Context-Aware Spell Checker Configuration

model:
  name: "bert-base-uncased"
  device: "auto"
  confidence_threshold: 0.7
  max_length: 512
  batch_size: 1

database:
  path: "spell_checker.db"
  auto_create: true
  populate_sample_data: true

spell_check:
  check_spelling: true
  check_homophones: true
  check_grammar: false
  context_window_size: 3
  max_suggestions: 5
  min_confidence: 0.5

ui:
  theme: "light"
  language: "en"
  show_confidence: true
  show_statistics: true
  auto_correct: false

# API settings
api_host: "0.0.0.0"
api_port: 8000
api_debug: false

# Logging
log_level: "INFO"
log_file: "logs/spell_checker.log"
"""
    
    try:
        with open("config.yaml", "w") as f:
            f.write(config_content)
        print("✅ Created default configuration file: config.yaml")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.db
*.sqlite
*.sqlite3
logs/
data/
config/local_*.yaml
config/local_*.json

# Models (if downloaded locally)
models/
checkpoints/

# Temporary files
*.tmp
*.temp
"""
    
    try:
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .gitignore: {e}")
        return False

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import torch
        import transformers
        import spacy
        import fastapi
        import streamlit
        print("✅ All core dependencies imported successfully")
        
        # Test spell checker
        from spell_checker import ContextAwareSpellChecker
        print("✅ Spell checker module imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Context-Aware Spell Checker")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Create configuration files
    if not create_config_files():
        print("❌ Configuration file creation failed")
        sys.exit(1)
    
    # Create .gitignore
    if not create_gitignore():
        print("❌ .gitignore creation failed")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the basic spell checker: python spell_checker.py")
    print("2. Start the web app: python web_app.py")
    print("3. Start the Streamlit dashboard: streamlit run streamlit_app.py")
    print("4. Run tests: python -m pytest test_spell_checker.py -v")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
