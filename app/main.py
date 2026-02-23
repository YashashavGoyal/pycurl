from typer import Typer

from app.commands import init, config, get, post, put, patch, delete, auth, token, docs
from app.commands.docs.commands import workflow_docs
from app.utils import PanelDisplay, TextDisplay

# Typer app instance
app = Typer(
    name="pycurl", 
    help="A lightweight curl-like CLI tool written in Python using requests",
    no_args_is_help=True
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
    TextDisplay.style_text("PyCurl version: 1.1.0", style="white")

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
      subtitle="Version 1.1.0"
    )



if __name__ == "__main__":
    app()
