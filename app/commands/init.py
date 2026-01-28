import json
from pathlib import Path
from typer import Option

from app.utils import TextDisplay
from app.utils import CONFIG_PATH, getDefaultConfig



def init(
    token_file_path: str | None = Option(None, "-t", "--token-file-path", help="Path to save the token file"),
    overwrite: bool = Option(False, "-o", "--overwrite", help="Overwrite existing configuration file if it exists")
):
    """Initialize the application with a configuration file."""
    
    created_config = False
    created_token = False

    config_file = CONFIG_PATH
    token_file = Path(token_file_path).expanduser().resolve() if token_file_path else Path.home() / ".pycurl/tokens"


    DEFAULT_CONFIG_TEMPLATE = getDefaultConfig(token_file)

    DEFAULT_TOKEN_TEMPLATE = """# alias:token\n# example\n# localhost:eyJhbGciOi...\n"""


    try:

        if token_file == config_file:
            raise SystemExit(TextDisplay().error_text("Token file and config file cannot be the same"))

        if overwrite:
            TextDisplay().warn_text("Overwrite enabled: existing files may be replaced.")

        if not config_file.exists() or overwrite:
            if config_file.parent.exists():
                TextDisplay().info_text(f"Config directory exists: {config_file.parent}")
            else:
                config_file.parent.mkdir(parents=True, exist_ok=True)
                TextDisplay().success_text(f"Created directory: {config_file.parent}")
            with open(config_file, "w", encoding="utf-8") as cf:
                json.dump(DEFAULT_CONFIG_TEMPLATE, cf, indent=4)
            created_config = True
            TextDisplay().success_text(f"Created configuration file at: {config_file}")
        else:
            TextDisplay().info_text(f"Config directory exists: {config_file.parent}")
            TextDisplay().info_text(f"Configuration file already exists at: {config_file}")

        if not token_file.exists() or overwrite:
            token_file.parent.mkdir(parents=True, exist_ok=True)
            token_file.write_text(
                DEFAULT_TOKEN_TEMPLATE,
                encoding="utf-8"
            )
            created_token = True
            TextDisplay().success_text("Created tokens file")
        else:
            TextDisplay().info_text("tokens file already exists")     

        NEXT_STEPS = (
            "\nYou can now use pycurl commands.\n"
            "Next steps:\n"
            "\t- Run [blue]`pycurl auth login ...`[/blue]\n"
            "\t- Use [blue]`-U <alias>`[/blue] to attach a token"
        )


        if created_config or created_token:
            TextDisplay().style_text(
                f"pycurl initialized at {config_file.parent}",
                style="white"
            )
            TextDisplay().style_text(
                NEXT_STEPS,
                style="white"
            )
        else:
            TextDisplay().style_text(
                "pycurl already initialized",
                style="white"
            )
            TextDisplay().style_text(
                NEXT_STEPS,
                style="white"
            )
   

    except Exception as e:
        raise SystemExit(TextDisplay().error_text(f"Failed to initialize configuration file: {e}"))