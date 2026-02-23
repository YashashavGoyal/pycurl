from typer import Argument

from app.utils import (
    CONFIG_PATH, 
    TextDisplay, 
    loadAndValidateConfig,
    InvalidConfig
)

# pycurl config get
def get(
    key: str = Argument(..., help="Enter key you want to see as [bold]Referenced from auth[/bold] using [cyan].[/cyan]")
):
    """Fetches key you request to see as [bold]Referenced from auth[/bold] using using [cyan].[/cyan]"""

    try:
        config_data = loadAndValidateConfig(config_path=CONFIG_PATH)
        
        parts = key.split(".")
        value = config_data
        for p in parts:
            value = value[p]

        TextDisplay.style_text(f"[blue]{key}[/blue] = {value}", style="white")

    except InvalidConfig:
        error_msg = (
            "[red]Configuration is invalid[/red]\n"
            "\t - Use [cyan]pycurl config validate[/cyan] to check errors\n"
            "\t - Use [cyan]pycurl config generate[/cyan] to generate new config\n"
            "\t - Or simply run [cyan]pycurl init -o[/cyan] overwrite existing config"
        )
        TextDisplay.style_text(error_msg, style="white")
        raise SystemExit(1)

    except Exception as e:
        TextDisplay.error_text(f"Error: {e}")
