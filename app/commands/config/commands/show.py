from typer import Option
from pprint import pprint

from app.utils import (
    CONFIG_PATH, 
    TextDisplay, 
    loadAndValidateConfig,
    extractConfigAttributes,
    ConfigError,
    InvalidConfig
)


def show(
    format: str = Option("human", "-f", "--format", help="Format to show the config file (json or human)")
):
    """Shows the current Configuration present in the file. If it is valid"""
    
    try:
        config_data = loadAndValidateConfig(config_path=CONFIG_PATH)

        token_file, token_type, default_token = extractConfigAttributes(config_data=config_data)

        if format == "human":

            Config = (
                "[yellow]PyCurl Config File[/yellow]\n"
                f"\t [cyan]Token File[/cyan] : {token_file}\n"
                f"\t [cyan]Token Type[/cyan] : {token_type}\n"
                f"\t [cyan]Default Token[/cyan] : {default_token}\n"
            )

            TextDisplay().style_text(Config, style="white")

        if format == "json":
            pprint(config_data)

    except InvalidConfig:
        ERROR = (
                "[red]Configuration is invalid[/red]\n"
                "\t - Use [cyan]pycurl config validate[/cyan] to check errors\n"
                "\t - Use [cyan]pycurl config generate[/cyan] to generate new config\n"
                "\t - Or simply run [cyan]pycurl init -o[/cyan] overwrite existing config"
            )
        TextDisplay().style_text(ERROR, style="white")
        raise SystemExit(1)

    except ConfigError as ce:
        TextDisplay().error_text(f"{ce}")
