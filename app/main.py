from typer import Typer

from app.commands import init, get, post, put, patch, delete, auth
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

# pycurl init ...
app.command(
    name="init",
    short_help="Initialize the application with a configuration file"
)(init)

# pycurl get ...
app.command(
    name="get",
    short_help="Perform a GET request"
)(get)

# pycurl post ...
app.command(
    name="post",
    short_help="Perform a POST request"
)(post)

# pycurl put ...
app.command(
    name="put",
    short_help="Perform a PUT request"
)(put)

# pycurl patch ...
app.command(
    name="patch",
    short_help="Perform a PATCH request"
)(patch)

# pycurl delete ...
app.command(
    name="delete",
    short_help="Perform a DELETE request"
)(delete)


# pycurl version
@app.command(
    name="version",
    short_help="Show the version of PyCurl"
)
def version():
    """Show the version of PyCurl"""
    TextDisplay().style_text("PyCurl version: 0.1.0",style="white")

# pycurl about
@app.command(
    name="about",
    short_help="Show information about PyCurl"
)
def about():
    """Show information about PyCurl"""
    PanelDisplay().print_panel("About PyCurl", "PyCurl is a lightweight curl-like CLI tool written in Python using requests.", border_style="cyan", subtitle="Version 0.1.0")



if __name__ == "__main__":
    app()