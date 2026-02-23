from typer import  Argument
from pathlib import Path
import json

from app.utils import (
    CONFIG_PATH, 
    TextDisplay, 
    loadConfig, 
    configValidator,
    ConfigError,
)

# pycurl config set
def set_conf(
    key: str = Argument(..., help="Enter key you want to update as [bold]Referenced from auth[/bold] using [cyan].[/cyan]"),
    value: str = Argument("", help="Enter the value you want to update for given key")
):
    """Recommended when you want to update any single key in config file as per your requirement"""

    try:
        if not key:
            raise ValueError("Properly Enter Key or go to --help")
        
        config_data = loadConfig(CONFIG_PATH)
        parts = key.split(".")

        # if key.endswith("token_file"):
        if parts == ["auth", "token_file"]:
            try: 
                value = Path(value).expanduser().resolve()
                if not value.exists():
                    value.parent.mkdir(parents=True, exist_ok=True)

                    TextDisplay.error_text(f"token file not found at {value}")
                    TextDisplay.style_text("Creating token file...", style="gray50")
                    
                    DEFAULT_TOKEN_TEMPLATE = """# alias:token\n# example\n# localhost:eyJhbGciOi...\n"""
                    value.write_text(
                        DEFAULT_TOKEN_TEMPLATE,
                        encoding="utf-8"
                    )
                    TextDisplay.style_text("token file created", style="gray50")
                value = str(value)

            except Exception as e:
                raise e

        # Traverse and set value
        target = config_data
        for p in parts[:-1]:
            target = target.setdefault(p, {})

        target[parts[-1]] = value

        # Validate before saving
        valid, errors = configValidator(config_data)
        if not valid:
            for e in errors:
                TextDisplay.error_text(str(e))
            raise SystemExit(1)

        # Save to file
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)

        TextDisplay.success_text("Configuration updated successfully.")

    except ConfigError as ce:
        TextDisplay.error_text(str(ce))
    
    except ValueError as ve:
        TextDisplay.error_text(f"Error: {ve}")
 