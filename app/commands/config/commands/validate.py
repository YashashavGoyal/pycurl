from app.utils import (
    CONFIG_PATH, 
    TextDisplay, 
    loadConfig, 
    configValidator, 
    ConfigError,
)


def validate():
    """Validates the Configuration on the basis of syntax and values."""
    
    try:
        config_data = loadConfig(config_path=CONFIG_PATH)

        isValid, errors = configValidator(config_data=config_data)
        if not isValid:
            for err in errors:
                TextDisplay().error_text(f"- {err}")

            ERROR = (
            "\n[yellow]How to reslove errors[/yellow]\n"
            "\t - Use [cyan]pycurl config generate[/cyan] to generate new config\n"
            "\t - Or simply run [cyan]pycurl init -o[/cyan] overwrite existing config\n" 
            "\n[green]Recommended[/green]: Update config using:\n"
            "\t - pycurl config [blue]set[/blue] or\n"
            "\t - pycurl config [blue]generate[/blue]\n"
            )
            TextDisplay().style_text(ERROR, style="white")

            raise SystemExit(1)
        
        else:
            TextDisplay().success_text("Your Configuration File is alright")

    except ConfigError as ce:
        TextDisplay().error_text(f"{ce}")

