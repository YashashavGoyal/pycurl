from typer import Argument, Option

from app.utils import (
    CONFIG_PATH, 
    tokenPathResolver, 
    loadAndValidateConfig, 
    TextDisplay, 
    ConfigError, 
    alias_validator
)

# pycurl token set
def set_token(
    token: str = Argument(..., help="Token string to save"),
    alias: str = Option(..., "-a", "--alias", help="Alias for this token")
):
    """Add a new token or update an existing one in the token file."""
    try:
        config = loadAndValidateConfig(config_path=CONFIG_PATH)
        token_file_path = tokenPathResolver(config_data=config)

        # Handle token file existence
        if not token_file_path.exists():
            TextDisplay.warn_text(f"Token file not found at {token_file_path}\n[yellow]Creating File...[/yellow]")
            token_file_path.parent.mkdir(parents=True, exist_ok=True)
            token_file_path.touch()

        # Validate alias format
        if alias and not alias_validator(alias):
            raise ValueError("Invalid alias format")

        # Read existing file
        with open(token_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        found = False
        new_token_line = f"{alias}:{token}\n"

        for line in lines:
            stripped = line.strip()
            
            # Preserve comments and empty lines
            if not stripped or stripped.startswith("#"):
                new_lines.append(line)
                continue
            
            if ":" not in stripped:
                new_lines.append(line)
                continue
                
            current_alias, _ = stripped.split(":", 1)
            
            if current_alias.strip() == alias:
                new_lines.append(new_token_line)
                found = True
            else:
                new_lines.append(line)

        # Append if new alias
        if not found:
            # Ensure we start on a new line if the file doesn't end with one
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines[-1] += "\n"
            new_lines.append(new_token_line)

        # Write updates
        with open(token_file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        if found:
            TextDisplay.info_text(f"Token '{alias}' updated successfully at {token_file_path}")
        else:
            TextDisplay.info_text(f"Token '{alias}' set successfully at {token_file_path}")

    except ConfigError as ce:
        TextDisplay.error_text(str(ce))
    except ValueError as ve:
        TextDisplay.error_text(str(ve))
    except Exception as e:
        TextDisplay.error_text(f"Error: {e}")