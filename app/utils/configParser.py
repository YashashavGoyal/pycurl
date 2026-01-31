from pathlib import Path
import json

# Default Config Path
CONFIG_PATH = Path.home() / ".pycurl" / "config.json"

# Default Config Template
DEFAULT_TOKEN_PATH = Path.home()/".pycurl/tokens"
def getDefaultConfig(token_file:Path = DEFAULT_TOKEN_PATH, token_type:str = "Bearer", default_token:str|None = None) -> dict:
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
    pass

class ConfigNotFound(ConfigError):
    pass

class InvalidConfig(ConfigError):
    pass


# Load and return the configuration data
def loadConfig(config_path: Path) -> dict:
    if not config_path.exists():
        raise ConfigNotFound(f"Config not found at {config_path}")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError as e:
        raise InvalidConfig(f"Invalid JSON in {config_path}") from e

# Validates the syntax and fields of config file
def configValidator(config_data: dict) -> tuple[bool, list[ConfigError]]:
    errors = []
    auth = config_data.get("auth")

    # checking auth
    if not isinstance(auth, dict):
        return False, [InvalidConfig("Missing or invalid 'auth' section")]

    # Check for unexpected top-level keys
    allowed_top_keys = {"auth"}
    actual_keys = set(config_data.keys())
    extra_keys = actual_keys - allowed_top_keys
    if extra_keys:
        errors.append(InvalidConfig(f"Unknown sections: {', '.join(extra_keys)}"))

    # Validate token_file
    token_file = auth.get("token_file")
    if not isinstance(token_file, str) or not token_file.strip():
        errors.append(InvalidConfig("'auth.token_file' must be a non-empty string"))
    
    # Validate token_type
    token_type = auth.get("token_type")
    if not isinstance(token_type, str):
        errors.append(InvalidConfig("'auth.token_type' must be a string (can be empty)"))

    # Validate default_token
    default_token = auth.get("default_token")
    if default_token is not None:
        if not isinstance(default_token, str):
            errors.append(InvalidConfig("'auth.default_token' must be a string or null"))
        elif ":" in default_token:
            errors.append(InvalidConfig("'auth.default_token' cannot contain ':'"))

    # Check for unexpected keys inside auth
    allowed_auth_keys = {"token_file", "token_type", "default_token"}
    extra_auth = set(auth.keys()) - allowed_auth_keys
    if extra_auth:
        errors.append(InvalidConfig(f"Unknown keys in 'auth': {', '.join(extra_auth)}"))

    return len(errors) == 0, errors

# For Future Use
# load + Validate
def loadAndValidateConfig(config_path) -> dict:
    config_data = loadConfig(config_path)
    isValid, errors = configValidator(config_data=config_data)
    
    if not isValid:
        raise InvalidConfig("Validation failed")

    return config_data

# Implement token path resolution logic here
def tokenPathResolver(config_data: dict) -> Path:
    raw_path = config_data["auth"]["token_file"]
    return Path(raw_path).expanduser().resolve()

# Implement token type resolution logic here
def tokenTypeResolver(config_data: dict) -> str:
    return config_data.get("auth", {}).get("token_type", "")

# Implement default token resolution logic here
def defaultTokenResolver(config_data: dict) -> str | None:
    return config_data["auth"].get("default_token")

# Implement attribute extraction logic here
def extractConfigAttributes(config_data: dict) -> tuple[Path, str, str | None]:
    return (
        tokenPathResolver(config_data),
        tokenTypeResolver(config_data),
        defaultTokenResolver(config_data)
    )
