"""
Configuration Management for Context-Aware Spell Checker
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import yaml

@dataclass
class ModelConfig:
    """Configuration for ML models"""
    name: str = "bert-base-uncased"
    device: str = "auto"  # auto, cpu, cuda
    max_length: int = 512
    batch_size: int = 1
    confidence_threshold: float = 0.7

@dataclass
class DatabaseConfig:
    """Configuration for database"""
    path: str = "spell_checker.db"
    auto_create: bool = True
    populate_sample_data: bool = True

@dataclass
class SpellCheckConfig:
    """Configuration for spell checking behavior"""
    check_spelling: bool = True
    check_homophones: bool = True
    check_grammar: bool = False
    context_window_size: int = 3
    max_suggestions: int = 5
    min_confidence: float = 0.5

@dataclass
class UIConfig:
    """Configuration for user interface"""
    theme: str = "light"  # light, dark
    language: str = "en"
    show_confidence: bool = True
    show_statistics: bool = True
    auto_correct: bool = False

@dataclass
class AppConfig:
    """Main application configuration"""
    model: ModelConfig
    database: DatabaseConfig
    spell_check: SpellCheckConfig
    ui: UIConfig
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None

class ConfigManager:
    """Configuration manager for the spell checker application"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.yaml"
        self.config = self._load_config()
    
    def _load_config(self) -> AppConfig:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_path):
            return self._load_from_file()
        else:
            return self._create_default_config()
    
    def _load_from_file(self) -> AppConfig:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.endswith('.json'):
                    data = json.load(f)
                else:
                    data = yaml.safe_load(f)
            
            return self._dict_to_config(data)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> AppConfig:
        """Create default configuration"""
        return AppConfig(
            model=ModelConfig(),
            database=DatabaseConfig(),
            spell_check=SpellCheckConfig(),
            ui=UIConfig()
        )
    
    def _dict_to_config(self, data: Dict[str, Any]) -> AppConfig:
        """Convert dictionary to AppConfig"""
        return AppConfig(
            model=ModelConfig(**data.get('model', {})),
            database=DatabaseConfig(**data.get('database', {})),
            spell_check=SpellCheckConfig(**data.get('spell_check', {})),
            ui=UIConfig(**data.get('ui', {})),
            api_host=data.get('api_host', '0.0.0.0'),
            api_port=data.get('api_port', 8000),
            api_debug=data.get('api_debug', False),
            log_level=data.get('log_level', 'INFO'),
            log_file=data.get('log_file')
        )
    
    def save_config(self, path: Optional[str] = None):
        """Save current configuration to file"""
        save_path = path or self.config_path
        
        config_dict = {
            'model': asdict(self.config.model),
            'database': asdict(self.config.database),
            'spell_check': asdict(self.config.spell_check),
            'ui': asdict(self.config.ui),
            'api_host': self.config.api_host,
            'api_port': self.config.api_port,
            'api_debug': self.config.api_debug,
            'log_level': self.config.log_level,
            'log_file': self.config.log_file
        }
        
        with open(save_path, 'w') as f:
            if save_path.endswith('.json'):
                json.dump(config_dict, f, indent=2)
            else:
                yaml.dump(config_dict, f, default_flow_style=False)
    
    def get_model_config(self) -> ModelConfig:
        """Get model configuration"""
        return self.config.model
    
    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration"""
        return self.config.database
    
    def get_spell_check_config(self) -> SpellCheckConfig:
        """Get spell check configuration"""
        return self.config.spell_check
    
    def get_ui_config(self) -> UIConfig:
        """Get UI configuration"""
        return self.config.ui
    
    def update_model_config(self, **kwargs):
        """Update model configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config.model, key):
                setattr(self.config.model, key, value)
    
    def update_spell_check_config(self, **kwargs):
        """Update spell check configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config.spell_check, key):
                setattr(self.config.spell_check, key, value)
    
    def update_ui_config(self, **kwargs):
        """Update UI configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config.ui, key):
                setattr(self.config.ui, key, value)

# Environment variable configuration
class EnvironmentConfig:
    """Configuration from environment variables"""
    
    @staticmethod
    def get_model_name() -> str:
        """Get model name from environment"""
        return os.getenv('SPELL_CHECKER_MODEL', 'bert-base-uncased')
    
    @staticmethod
    def get_device() -> str:
        """Get device from environment"""
        return os.getenv('SPELL_CHECKER_DEVICE', 'auto')
    
    @staticmethod
    def get_api_host() -> str:
        """Get API host from environment"""
        return os.getenv('SPELL_CHECKER_HOST', '0.0.0.0')
    
    @staticmethod
    def get_api_port() -> int:
        """Get API port from environment"""
        return int(os.getenv('SPELL_CHECKER_PORT', '8000'))
    
    @staticmethod
    def get_debug() -> bool:
        """Get debug mode from environment"""
        return os.getenv('SPELL_CHECKER_DEBUG', 'false').lower() == 'true'
    
    @staticmethod
    def get_log_level() -> str:
        """Get log level from environment"""
        return os.getenv('SPELL_CHECKER_LOG_LEVEL', 'INFO')

# Configuration presets
class ConfigPresets:
    """Predefined configuration presets"""
    
    @staticmethod
    def development() -> AppConfig:
        """Development configuration"""
        return AppConfig(
            model=ModelConfig(
                name="distilbert-base-uncased",
                device="cpu",
                confidence_threshold=0.6
            ),
            database=DatabaseConfig(
                path="dev_spell_checker.db"
            ),
            spell_check=SpellCheckConfig(
                context_window_size=2,
                max_suggestions=3
            ),
            ui=UIConfig(
                theme="light",
                auto_correct=False
            ),
            api_debug=True,
            log_level="DEBUG"
        )
    
    @staticmethod
    def production() -> AppConfig:
        """Production configuration"""
        return AppConfig(
            model=ModelConfig(
                name="bert-base-uncased",
                device="auto",
                confidence_threshold=0.8
            ),
            database=DatabaseConfig(
                path="prod_spell_checker.db"
            ),
            spell_check=SpellCheckConfig(
                context_window_size=3,
                max_suggestions=5,
                min_confidence=0.7
            ),
            ui=UIConfig(
                theme="light",
                auto_correct=True
            ),
            api_debug=False,
            log_level="INFO"
        )
    
    @staticmethod
    def testing() -> AppConfig:
        """Testing configuration"""
        return AppConfig(
            model=ModelConfig(
                name="bert-base-uncased",
                device="cpu",
                confidence_threshold=0.5
            ),
            database=DatabaseConfig(
                path="test_spell_checker.db"
            ),
            spell_check=SpellCheckConfig(
                context_window_size=1,
                max_suggestions=2
            ),
            ui=UIConfig(
                theme="light"
            ),
            api_debug=True,
            log_level="DEBUG"
        )

# Configuration validation
class ConfigValidator:
    """Validate configuration values"""
    
    @staticmethod
    def validate_model_config(config: ModelConfig) -> bool:
        """Validate model configuration"""
        valid_models = [
            "bert-base-uncased",
            "bert-base-cased",
            "distilbert-base-uncased",
            "roberta-base"
        ]
        
        if config.name not in valid_models:
            raise ValueError(f"Invalid model name: {config.name}")
        
        if config.device not in ["auto", "cpu", "cuda"]:
            raise ValueError(f"Invalid device: {config.device}")
        
        if not 0.0 <= config.confidence_threshold <= 1.0:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
        
        return True
    
    @staticmethod
    def validate_spell_check_config(config: SpellCheckConfig) -> bool:
        """Validate spell check configuration"""
        if config.context_window_size < 1:
            raise ValueError("Context window size must be at least 1")
        
        if config.max_suggestions < 1:
            raise ValueError("Max suggestions must be at least 1")
        
        if not 0.0 <= config.min_confidence <= 1.0:
            raise ValueError("Min confidence must be between 0.0 and 1.0")
        
        return True
    
    @staticmethod
    def validate_ui_config(config: UIConfig) -> bool:
        """Validate UI configuration"""
        if config.theme not in ["light", "dark"]:
            raise ValueError("Theme must be 'light' or 'dark'")
        
        if config.language not in ["en", "es", "fr", "de"]:
            raise ValueError("Unsupported language")
        
        return True

def main():
    """Demonstrate configuration usage"""
    print("🔧 Configuration Management Demo")
    
    # Create config manager
    config_manager = ConfigManager()
    
    # Display current configuration
    print("\n📋 Current Configuration:")
    print(f"Model: {config_manager.get_model_config().name}")
    print(f"Device: {config_manager.get_model_config().device}")
    print(f"Database: {config_manager.get_database_config().path}")
    print(f"API Port: {config_manager.config.api_port}")
    
    # Update configuration
    print("\n🔄 Updating Configuration...")
    config_manager.update_model_config(device="cpu")
    config_manager.update_spell_check_config(context_window_size=5)
    
    # Save configuration
    config_manager.save_config("custom_config.yaml")
    print("✅ Configuration saved to custom_config.yaml")
    
    # Test presets
    print("\n🎯 Testing Presets:")
    dev_config = ConfigPresets.development()
    print(f"Development Model: {dev_config.model.name}")
    
    prod_config = ConfigPresets.production()
    print(f"Production Model: {prod_config.model.name}")
    
    # Test validation
    print("\n✅ Testing Validation:")
    try:
        ConfigValidator.validate_model_config(dev_config.model)
        print("Model config validation passed")
    except ValueError as e:
        print(f"Model config validation failed: {e}")

if __name__ == "__main__":
    main()
