from typer import Argument

from app.utils import (
    CONFIG_PATH,
    parse_token_file,
    extractConfigAttributes,
    loadAndValidateConfig,
    TextDisplay,
    TableDisplay,
    InvalidConfig,
    ConfigError
)

# pycurl token list
def list_tokens(
    alias: str = Argument(None, help="Token alias name")
):
    """List specific tokens by alias or all available tokens."""
    try:
        config = loadAndValidateConfig(CONFIG_PATH)
        token_file, _, default = extractConfigAttributes(config)
        tokens = parse_token_file(token_file)
        
        # Handle default alias resolution
        if alias == "default":
            if not default:
                raise ConfigError("Default alias is not set. use [blue]pycurl config generate --modify[/blue] to set")
            if default not in tokens:
                raise InvalidConfig(f"Default alias '{default}' not found")
            return tokens[default]

        if alias:
            if alias not in tokens:
                raise InvalidConfig(f"Token alias '{alias}' not found")
            token = tokens[alias]
            TextDisplay.style_text(f"[bold]{alias}[/bold] : {token}", style="white")
            return
        
        table = TableDisplay( title="Tokens",columns=["Alias", "Token"], style="white")
        for alias, token in tokens.items():
            table.add_row([alias, token])
        table.show()


    except InvalidConfig as ic:
        TextDisplay.error_text(str(ic))

    except ConfigError as ce:
        TextDisplay.error_text(str(ce))
