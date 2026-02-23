from app.utils import (
    CONFIG_PATH, 
    TextDisplay, 
    loadConfig, 
    configValidator, 
    ConfigError,
)

# pycurl config validate
def validate():
    """Validates the Configuration on the basis of syntax and values."""
    
    try:
        config_data = loadConfig(config_path=CONFIG_PATH)

        isValid, errors = configValidator(config_data=config_data)
        if not isValid:
            for err in errors:
                TextDisplay.error_text(f"- {err}")

            guidance = (
                "\n[yellow]How to resolve errors[/yellow]\n"
                "\t - Use [cyan]pycurl config generate[/cyan] to generate new config\n"
                "\t - Or simply run [cyan]pycurl init -o[/cyan] overwrite existing config\n" 
                "\n[green]Recommended[/green]: Update config using:\n"
                "\t - pycurl config [blue]set[/blue] or\n"
                "\t - pycurl config [blue]generate[/blue]\n"
            )
            TextDisplay.style_text(guidance, style="white")
            raise SystemExit(1)
        
        else:
            TextDisplay.success_text("Your Configuration File is alright")

    except ConfigError as ce:
        TextDisplay.error_text(f"Error: {ce}")
