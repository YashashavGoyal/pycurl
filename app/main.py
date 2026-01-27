from typer import Typer
from app.commands import get
from app.utils.ui import PanelDisplay, TextDisplay

# Typer app instance
app = Typer(
    name="pycurl", 
    help="A lightweight curl-like CLI tool written in Python using requests",
    no_args_is_help=True
    )

# pycurl get ...
app.command(
    name="get",
    short_help="Perform a GET request"
)(get)


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