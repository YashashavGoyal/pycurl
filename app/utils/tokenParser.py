from pathlib import Path
from typing import Dict

from .configParser import (
    CONFIG_PATH,
    loadAndValidateConfig, 
    extractConfigAttributes, 
    InvalidConfig
)


# Parse token alias file into {alias: token}
def parse_token_file(token_file: Path) -> Dict[str, str]:

    if not token_file.exists():
        raise InvalidConfig(f"Token file not found at {token_file}")

    tokens: Dict[str, str] = {}

    with open(token_file, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()

            # Ignore comments & empty lines
            if not line or line.startswith("#"):
                continue
            
            if ":" not in line:
                raise InvalidConfig(
                    f"Invalid token format at line {lineno}: {line}"
                )

            alias, token = line.split(":", 1)

            alias = alias.strip()
            token = token.strip()

            if not alias or not token:
                raise InvalidConfig(
                    f"Empty alias or token at line {lineno}"
                )

            if alias in tokens:
                raise InvalidConfig(
                    f"Duplicate alias '{alias}' at line {lineno}"
                )

            tokens[alias] = token
    
    return tokens

# Resolve token alias into actual token
def resolve_token(alias: str = "", config_path: Path = CONFIG_PATH) -> str:
    config = loadAndValidateConfig(config_path)
    token_file, _, default_token = extractConfigAttributes(config)

    tokens = parse_token_file(token_file)

    # If alias explicitly provided
    if alias and alias != "default":
        if alias not in tokens:
            raise InvalidConfig(f"Token alias '{alias}' not found")
        return tokens[alias]

    # Fallback to default token
    if default_token and alias == "default":
        if default_token not in tokens:
            raise InvalidConfig(
                f"Default token alias '{default_token}' not found"
            )
        return tokens[default_token]

    raise InvalidConfig(
        "No token alias provided and no default_token set in config"
    )

# Check if alias is correct or not
def alias_validator(alias: str) -> bool:
    if ":" in alias.strip():
        return False
    return True

def getSavedToken(alias: str, config_path: Path = CONFIG_PATH) -> tuple[str, dict]:
    config = loadAndValidateConfig(config_path)
    token_file, token_type, default_token = extractConfigAttributes(config)
    tokens = parse_token_file(token_file)
    
    headers = {}

    if alias == "default":
        if default_token not in tokens:
            raise InvalidConfig(f"Default token alias '{default_token}' not found in token file")
        headers["Authorization"] = f"{token_type} {tokens[default_token]}"
        return tokens[default_token], headers

    if alias not in tokens:
        raise InvalidConfig(f"Token alias '{alias}' not found")

    headers["Authorization"] = f"{token_type} {tokens[alias]}"
    return tokens[alias], headers


# Store the authentication token to a specified file
def storeTokenToFile(token: str, file_path: str):
    """Store the authentication token to a specified file."""
    if not token:
        raise ValueError("No token provided to store in file.")

    if not file_path:
        raise ValueError("No file path provided to store the token.")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(token)
    except Exception as e:
        raise RuntimeError(f"Error storing token to file: {e}")


# Save the token to the default configuration file with the given alias
def saveTokenToDefaultConfig(token: str, alias: str):
    """Save the token to the default configuration file with the given alias."""
    if not alias_validator(alias):
        raise ValueError(f"Invalid alias '{alias}'. Aliases cannot contain ':'.")

    try:
        # Load config to find the token file path
        config = loadAndValidateConfig(CONFIG_PATH) # using default global path
        token_file, _, _ = extractConfigAttributes(config)

        # Ensure directory exists
        token_file.parent.mkdir(parents=True, exist_ok=True)
        
        lines = []
        if token_file.exists():
            with open(token_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        
        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("#") or not line.strip():
                new_lines.append(line)
                continue
                
            if ":" in line:
                current_alias, _ = line.split(":", 1)
                if current_alias.strip() == alias:
                    new_lines.append(f"{alias}: {token}\n")
                    updated = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        if not updated:
            new_lines.append(f"{alias}: {token}\n")

        with open(token_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    except Exception as e:
        raise RuntimeError(f"Error saving token to default config: {e}")