from pathlib import Path
from typing import Dict

from app.utils import (
    loadAndValidateConfig, 
    extractConfigAttributes,
    InvalidConfig, 
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
def resolve_token(alias: str = "", config_path: Path = None) -> str:
    config = loadAndValidateConfig(config_path)
    token_file, _, default_token = extractConfigAttributes(config)

    tokens = parse_token_file(token_file)

    # If alias explicitly provided
    if alias:
        if alias not in tokens:
            raise InvalidConfig(f"Token alias '{alias}' not found")
        return tokens[alias]

    # Fallback to default token
    if default_token:
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
