import os
from typing import Optional
from typer import Typer, Option, Context, Exit

from app.commands import init, config, get, post, put, patch, delete, auth, token, docs
from app.commands.docs.commands import workflow_docs
from app.utils import PanelDisplay, TextDisplay, set_modes

# Typer app instance
app = Typer(
    name="pycurl", 
    help="A lightweight curl-like CLI tool written in Python using requests",
    no_args_is_help=True
)

app_version = "1.2.0"

def version_callback(value: bool):
    if value:
        TextDisplay.style_text(f"✔ PyCurl version: {app_version}", style="white")
        raise Exit()

@app.callback()
def global_callback(
    ctx: Context,
    verbose: bool = Option(False, "--verbose", help="Show detailed DEBUG logs"),
    quiet: bool = Option(
        False, "--quiet", "-q", 
        help="Minimize output (errors only)",
        envvar="CLIMON_QUIET"
    ),
    json_mode: bool = Option(
        False, "--json", "-j", 
        help="Output result in pure JSON format",
        envvar="CLIMON_JSON"
    ),
    no_color: bool = Option(
        False, "--no-color", 
        help="Disable colored output",
        envvar="CLIMON_NO_COLOR"
    ),
    version: Optional[bool] = Option(
        None, "--version", "-v", 
        callback=version_callback,
        is_eager=True,
        help="Show CLI version"
    )
):
    """
    Global options for pycurl.
    """
    # Determine effective mode settings, considering both flags and environment variables
    cur_quiet = quiet or os.environ.get("CLIMON_QUIET") == "1"
    cur_json = json_mode or os.environ.get("CLIMON_JSON") == "1"
    cur_no_color = no_color or os.environ.get("CLIMON_NO_COLOR") == "1"

    # Log which global modes are being enabled based on flags and env vars
    if cur_no_color:
        TextDisplay.debug_text("Global Mode: NO_COLOR enabled")
    if verbose:
        TextDisplay.debug_text("Global Mode: VERBOSE enabled")
    if cur_quiet:
        TextDisplay.debug_text("Global Mode: QUIET enabled")
    if cur_json:
        TextDisplay.debug_text("Global Mode: JSON enabled")

    # Applying mode settings
    set_modes(
        quiet=cur_quiet,
        verbose=verbose,
        json=cur_json,
        no_color=cur_no_color
    )

# Registering subcommands

# pycurl auth ...
app.add_typer(auth)

# pycurl config ...
app.add_typer(config)

# pycurl token ...
app.add_typer(token)

# pycurl docs ...
app.add_typer(docs)

# pycurl workflow ...
app.add_typer(workflow_docs)


# Commands

# pycurl init ...
app.command(
    name="init",
    short_help="Initialize the application with a configuration file",
    epilog="""
    EXAMPLES\n
    pycurl init\n
    pycurl init --token-file ./tokens
    """
)(init)

# pycurl get ...
app.command(
    name="get",
    short_help="Perform a GET request",
    epilog="""
    EXAMPLES\n
    pycurl get https://jsonplaceholder.typicode.com/posts/1\n
    pycurl get https://api.example.com/data --output data.json --header "Authorization: Basic ..."\n
    pycurl get https://api.example.com/protected --use-token mytoken -r
    """
)(get)

# pycurl post ...
app.command(
    name="post",
    short_help="Perform a POST request",
    epilog="""
    EXAMPLES\n
    pycurl post https://api.example.com/users --json '{"name": "Alice"}'\n
    pycurl post https://api.example.com/login --json @credentials.json\n
    pycurl post https://api.example.com/submit --data "key=value"
    """
)(post)

# pycurl put ...
app.command(
    name="put",
    short_help="Perform a PUT request",
    epilog="""
    EXAMPLES\n
    pycurl put https://api.example.com/users/1 --json '{"name": "Bob"}'\n
    pycurl put https://api.example.com/posts/1 --header "Content-Type: application/json" --json '{"title": "Updated"}'\n
    pycurl put https://api.example.com/resources/1 --json @payload.json\n
    pycurl put https://api.example.com/protected/1 --use-token my-alias --json '{"active": true}'
    """
)(put)

# pycurl patch ...
app.command(
    name="patch",
    short_help="Perform a PATCH request",
    epilog="""
    EXAMPLES\n
    pycurl patch https://api.example.com/users/1 --json '{"name": "partial-update"}'\n
    pycurl patch https://api.example.com/posts/1 --header "Authorization: Bearer ..." --json '{"title": "Updated"}'\n
    pycurl patch https://api.example.com/resources/1 --json @update.json\n
    pycurl patch https://api.example.com/protected/1 --use-token my-alias --json '{"status": "archived"}'
    """
)(patch)

# pycurl delete ...
app.command(
    name="delete",
    short_help="Perform a DELETE request",
    epilog="""
    EXAMPLES\n
    pycurl delete https://api.example.com/users/1\n
    pycurl delete https://api.example.com/posts/1 --header "Authorization: Bearer ..."\n
    pycurl delete https://api.example.com/resources/1 --json '{"reason": "cleanup"}'\n
    pycurl delete https://api.example.com/protected/1 --use-token my-alias
    """
)(delete)


# General Commands

# pycurl version
@app.command(
    name="version",
    short_help="Show the version of PyCurl",
    epilog="""
    EXAMPLES\n
    pycurl version\n
    """
)
def version():
    """Show the version of PyCurl"""
    TextDisplay.style_text(f"PyCurl version: {app_version}", style="white")

# pycurl about
@app.command(
    name="about",
    short_help="Show information about PyCurl",
    epilog="""
    EXAMPLES\n
    pycurl about\n
    """
)
def about():
    """Show information about PyCurl"""
    PanelDisplay.print_panel(
      "About PyCurl", 
      "PyCurl is a lightweight curl-like CLI tool written in Python using requests.", 
      border_style="cyan", 
      subtitle=f"Version {app_version}"
    )



if __name__ == "__main__":
    app()
