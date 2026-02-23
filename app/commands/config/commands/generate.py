from typer import Option
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import shutil
import json

from app.utils import (
    CONFIG_PATH, 
    DEFAULT_TOKEN_PATH,
    getDefaultConfig,
    configValidator,
    loadAndValidateConfig,
    extractConfigAttributes,
    TextDisplay,
    PanelDisplay,
    PromptTaker,
    ConfigError, 
    ConfigNotFound, 
    InvalidConfig
)

# Configuration modes
class ConfigMode(Enum):
    CREATE = "create"
    OVERWRITE = "overwrite"
    MODIFY = "modify"
    RESET = "reset"

# Configuration options container
@dataclass
class ConfigOptions:
    overwrite: bool
    modify: bool
    reset: bool
    interactive: bool
    dry_run: bool
    backup: bool
    show: bool

# Logic for resolving the configuration mode
def resolve_config_mode(
    options: ConfigOptions,
    config_exists: bool
) -> ConfigMode:
    
    """Decide which mode/action should be performed or if any conflicting options are passed"""

    # Error Case
    if options.reset and options.modify:
        raise ConfigError("Cannot use --reset with --modify")
    
    if options.reset and options.overwrite:
        raise ConfigError("Cannot use --reset with --overwrite")

    if options.modify and options.overwrite:
        raise ConfigError("Cannot use --modify with --overwrite")

    if options.modify and not config_exists:
        raise ConfigNotFound("Cannot modify config: config file does not exist")
    
    # Deciding Mode - based on priority
    if options.reset:
        return ConfigMode.RESET
    
    if options.modify:
        return ConfigMode.MODIFY
    
    if config_exists:
        if options.overwrite:
            return ConfigMode.OVERWRITE
        else:
            raise ConfigError("Config already exists. Use --overwrite or --modify")
        
    return ConfigMode.CREATE

# Local helper for path validation
def verify_path(path: str) -> bool:
    """Validates that a path's parent directory exists."""
    token_path = Path(path).expanduser().resolve()
    return token_path.parent.exists()

# Logic for backing up configuration
def backup_config_file(config_file_path: Path) -> Path:
    """Backup the Config file in default PyCurl Directory in backup folder with timestamps"""
    if not config_file_path.exists():
        raise ConfigNotFound("Config file not found for backup")

    backup_dir = config_file_path.parent / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = backup_dir / f"config_{timestamp}.json"

    shutil.copy2(config_file_path, backup_file)

    return backup_file

# Logic for writing configuration to disk
def write_config(config_path: Path, config: dict):
    """Writes the configuration dictionary to a file."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

# Interactive configuration wizard
def get_config_from_user(existing_config: dict = None) -> dict:
    """Prompts the user for configuration details."""
    TextDisplay.style_text("\n--- PyCurl Config Wizard ---", style="yellow")
    
    d_path = DEFAULT_TOKEN_PATH
    d_type = "Bearer"
    d_alias = None

    if existing_config:
        try:
            path, t_type, alias = extractConfigAttributes(existing_config)
            d_path, d_type, d_alias = str(path), t_type, alias
        except Exception:
            # If extraction fails (corrupt file), we just stay with fallback defaults
            pass

    token_file_path = PromptTaker.input_text(
        "Token file path", 
        default=d_path, 
        validator=verify_path,
        error_msg="Invalid Path: Parent directory must exist."
    )

    token_type = PromptTaker.input_text("Token type", default=d_type)
    token_alias = PromptTaker.input_text("Default token alias", default=d_alias)

    config = getDefaultConfig(
        token_file=Path(token_file_path).expanduser().resolve(), 
        token_type=token_type, 
        default_token=token_alias
    )

    is_valid, errors = configValidator(config)
    if not is_valid:
        for e in errors:
            TextDisplay.error_text(str(e))
        raise InvalidConfig("The details provided failed validation rules.")
    
    return config

# pycurl config generate
def generate(
    reset: bool = Option(False, "-r", "--reset", help="Reset Config file to default configuration"),
    modify: bool = Option(False, "-m", "--modify", help="Update or modify existing config File"),
    overwrite: bool = Option(False, "-o", "--overwrite", help="Generate new config and overwrite existing file"),
    interactive: bool = Option(False, "-i", "--interactive", help="Generate Config file using user input"),
    show_config: bool = Option(False, "-s", "--show", help="Shows config file"),
    backup_config: bool = Option(False, "-b", "--backup", help="Backup Original Config_file before modifying"),
    dry_run: bool = Option(False, "--dry-run", help="Shows you the final config file before writing and asks for confirmation, can only be used with no-flag and --modify")
):
    """
    Config Modifier or Manager, Recommended method to change Config File,
    without any flag [bold]Default Behaviour[/bold] is [yellow]creating new Config[/yellow] If not exist
    """

    options = ConfigOptions(
        reset=reset,
        modify=modify,
        overwrite=overwrite,
        interactive=interactive,
        backup=backup_config,
        show=show_config,
        dry_run=dry_run
    )

    try:
        default_config_path = CONFIG_PATH

        action_flags = [reset, modify, overwrite, dry_run, backup_config, interactive]
        if show_config and any(action_flags):
            raise ConfigError("The --show flag cannot be used with modification flags.") 

        # Display-only mode
        if show_config:
            if not CONFIG_PATH.exists():
                raise ConfigNotFound("No config file found.")
            config_data = loadAndValidateConfig(default_config_path)
            PanelDisplay.print_json(
                title="PyCurl Config",
                content="\n[#FFA500]Current Config:[/#FFA500]",
                json=config_data
            )
            return
        
        # Determine execution path
        is_exists = default_config_path.exists()
        mode = resolve_config_mode(
                    options=options,
                    config_exists=is_exists
                )

        if dry_run and mode not in (ConfigMode.MODIFY, ConfigMode.CREATE):
            raise ConfigError("--dry-run only works with default generation or --modify")

        new_config_data = None

        # Mode execution
        if mode == ConfigMode.CREATE:
            new_config_data = get_config_from_user() if interactive else getDefaultConfig()

        elif mode == ConfigMode.MODIFY:
            current = loadAndValidateConfig(CONFIG_PATH)
            new_config_data = get_config_from_user(existing_config=current)

        elif mode in [ConfigMode.RESET, ConfigMode.OVERWRITE]:
            new_config_data = get_config_from_user() if interactive else getDefaultConfig()        
            
        # Perform backup
        if backup_config and is_exists:
            b_path = backup_config_file(CONFIG_PATH)
            TextDisplay.success_text(f"Backup created at: {b_path}")

        # Dry run confirmation
        if dry_run:
            PanelDisplay.print_json(title=f"DRY RUN: {mode.name}", json=new_config_data)
            if not PromptTaker.confirm("Proceed with writing to disk?", default=True):
                TextDisplay.style_text("\nOperation cancelled.", style="red")
                return

        # Commit changes
        write_config(CONFIG_PATH, new_config_data)
        TextDisplay.success_text(f"\nSuccessfully executed {mode.name} mode.")

    except Exception as e:
        TextDisplay.error_text(f"{e}")