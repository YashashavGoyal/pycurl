from pathlib import Path
import json

from .ui import TextDisplay

# Default Config Path
CONFIG_PATH = Path.home() / ".pycurl" / "config.json"

# Default Token Path
DEFAULT_TOKEN_PATH = Path.home() / ".pycurl" / "tokens"

# Fetch default config template
def getDefaultConfig(token_file:Path = DEFAULT_TOKEN_PATH, token_type:str = "Bearer", default_token:str|None = None) -> dict:
    """Returns the default configuration template."""
    DEFAULT_CONFIG_TEMPLATE = {
        "auth": {
            "token_file": str(token_file),
            "token_type": token_type,
            "default_token": default_token
        }
    }
    return DEFAULT_CONFIG_TEMPLATE

# Error classes for Config Exception
class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass

class ConfigNotFound(ConfigError):
    """Exception raised when the configuration file is not found."""
    pass

class InvalidConfig(ConfigError):
    """Exception raised when the configuration file is invalid."""
    pass


# Configuration loading logic
def loadConfig(config_path: Path) -> dict:
    """Loads and returns the configuration data."""
    TextDisplay.debug_text(f"Attempting to load config from: {config_path}")
    if not config_path.exists():
        TextDisplay.debug_text(f"Config file not found: {config_path}")
        raise ConfigNotFound(f"Config not found at {config_path}")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            TextDisplay.debug_text(f"Successfully loaded config from: {config_path}")
            return data

    except json.JSONDecodeError as e:
        TextDisplay.debug_text(f"Failed to parse JSON in {config_path}: {e}")
        raise InvalidConfig(f"Invalid JSON in {config_path}") from e

# Validates the syntax and fields of config file
def configValidator(config_data: dict) -> tuple[bool, list[ConfigError]]:
    """Validates the syntax and fields of the configuration data."""

    TextDisplay.debug_text("Validating configuration data...")
    errors = []
    auth = config_data.get("auth")

    # checking auth section
    if not isinstance(auth, dict):
        TextDisplay.debug_text("Validation failed: Missing or invalid 'auth' section")
        return False, [InvalidConfig("Missing or invalid 'auth' section")]

    # Check for unexpected top-level keys
    allowed_top_keys = {"auth"}
    actual_keys = set(config_data.keys())
    extra_keys = actual_keys - allowed_top_keys
    if extra_keys:
        msg = f"Unknown sections: {', '.join(extra_keys)}"
        TextDisplay.debug_text(f"Validation warning: {msg}")
        errors.append(InvalidConfig(msg))

    # Validate token_file field
    token_file = auth.get("token_file")
    if not isinstance(token_file, str) or not token_file.strip():
        errors.append(InvalidConfig("'auth.token_file' must be a non-empty string"))
    
    # Validate token_type field
    token_type = auth.get("token_type")
    if not isinstance(token_type, str):
        errors.append(InvalidConfig("'auth.token_type' must be a string (can be empty)"))

    # Validate default_token field
    default_token = auth.get("default_token")
    if default_token is not None:
        if not isinstance(default_token, str):
            errors.append(InvalidConfig("'auth.default_token' must be a string or null"))
        elif ":" in default_token:
            errors.append(InvalidConfig("'auth.default_token' cannot contain ':'"))

    # Check for unexpected keys inside auth section
    allowed_auth_keys = {"token_file", "token_type", "default_token"}
    extra_auth = set(auth.keys()) - allowed_auth_keys
    if extra_auth:
        msg = f"Unknown keys in 'auth': {', '.join(extra_auth)}"
        TextDisplay.debug_text(f"Validation warning: {msg}")
        errors.append(InvalidConfig(msg))

    if not errors:
        TextDisplay.debug_text("Configuration validation successful")
    else:
        TextDisplay.debug_text(f"Configuration validation found {len(errors)} issues")

    return len(errors) == 0, errors

# For Future Use
# load + Validate
def loadAndValidateConfig(config_path) -> dict:
    """Loads and validates the configuration data."""
    config_data = loadConfig(config_path)
    isValid, errors = configValidator(config_data=config_data)
    
    if not isValid:
        raise InvalidConfig("Validation failed")

    return config_data

# Implement token path resolution logic here
def tokenPathResolver(config_data: dict) -> Path:
    """Resolves the absolute path to the token file."""
    raw_path = config_data["auth"]["token_file"]
    return Path(raw_path).expanduser().resolve()

# Implement token type resolution logic here
def tokenTypeResolver(config_data: dict) -> str:
    """Returns the token type from configuration."""
    return config_data.get("auth", {}).get("token_type", "")

# Implement default token resolution logic here
def defaultTokenResolver(config_data: dict) -> str | None:
    """Returns the default token from configuration."""
    return config_data["auth"].get("default_token")

# Implement attribute extraction logic here
def extractConfigAttributes(config_data: dict) -> tuple[Path, str, str | None]:
    """Extracts all core configuration attributes."""
    return (
        tokenPathResolver(config_data),
        tokenTypeResolver(config_data),
        defaultTokenResolver(config_data)
    )
