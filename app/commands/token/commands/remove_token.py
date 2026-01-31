from typer import Argument, Option

from app.utils import CONFIG_PATH, extractConfigAttributes, loadAndValidateConfig, TextDisplay, PromptTaker, ConfigError, ConfigNotFound

def remove(
    alias: str | None = Argument(None, help="Token alias name to delete (ignored when --all is used)"),
    all: bool = Option(False, "-a", "--all", help="Delete all tokens from the file")
):
    try:

        if not alias and not all:
            raise ValueError("Give [yellow]alias name[/yellow] to delete token or \nuse [yellow]--all[/yellow] to delete all token")
        

        config = loadAndValidateConfig(CONFIG_PATH)
        token_file_path,_,default = extractConfigAttributes(config_data=config)
        if not token_file_path.exists():
            raise ConfigNotFound(f"Token file not found at {token_file_path}\n use [yellow] pycurl token set[/yellow]")
        
        if all:
            confirm = PromptTaker.confirm(
                "Are you sure you want to delete ALL tokens?",
                default=False
            )
            if not confirm:
                TextDisplay.info_text("Operation cancelled")
                return

        with open(token_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        found = False

        for line in lines:
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                new_lines.append(line)
                continue

            if ":" not in stripped:
                new_lines.append(line)
                continue

            name, _ = stripped.split(":", 1)

            if all:
                continue

            if alias == "default":
                alias = default

            if name == alias:
                found = True
                continue

            new_lines.append(line)

        if not all and not found:
            raise ValueError(f"Token alias '{alias}' not found")

        with open(token_file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        if all:
            TextDisplay.success_text("All tokens deleted successfully")
        else:
            TextDisplay.success_text(f"Token '{alias}' deleted successfully")

            if alias == default:
                TextDisplay.warn_text(
                    "Deleted token was default. Consider setting a new default token."
                )


    except ConfigError as ce:
        TextDisplay.error_text(str(ce))

    except ValueError as ve:
        TextDisplay.error_text(str(ve))

    except Exception as e:
        TextDisplay.error_text(str(e))