from typer import Typer, Context
from pathlib import Path

from app.utils import TextDisplay, print_markdown
from .commands import (
    get_docs,
    post_docs,
    put_docs,
    patch_docs,
    delete_docs,
    init_docs,
    auth_docs,
    config_docs,
    token_docs,
    workflow_docs
)

# Typer object for documentation
docs = Typer(
    name="docs",
    help="""
    Show documentation for pycurl commands, documentation mimic actual command stucture\n
    like 
    for pycurl get -> pycurl docs get
    for pycurl post -> pycurl docs post
    for pycurl config show -> pycurl docs config show
    for pycurl config init -> pycurl docs config init
    """,
)

def show_docs():
    """Displays the markdown documentation."""
    docs_path = Path(__file__).parent / "docs.md"
    try:
        print_markdown(docs_path)
    except FileNotFoundError as fnfe:
        TextDisplay.error_text(f"Error: {fnfe}")


# callback for docs
@docs.callback(
    epilog="""
    EXAMPLES\n
    pycurl docs\n
    pycurl docs show\n
    pycurl docs get\n
    pycurl docs config show\n
    """,
invoke_without_command=True
)
def docs_callback(ctx: Context):
    """
    Show documentation for pycurl commands.
    """
    if ctx.invoked_subcommand is None:
        show_docs()


# Register subcommands

# pycurl docs auth
docs.add_typer(
    auth_docs, 
    name="auth"
)

# pycurl docs config
docs.add_typer(
    config_docs, 
    name="config"
)

# pycurl docs token
docs.add_typer(
    token_docs, 
    name="token"
)

# pycurl docs workflow
docs.add_typer(
    workflow_docs, 
    name="workflow"
)

# Commands

# pycurl docs show
docs.command(
    name="show",
    short_help="Show the full documentation."
)(show_docs)

# pycurl docs get
docs.command(
    name="get",
    short_help="Show GET documentation."
)(get_docs)

# pycurl docs post
docs.command(
    name="post",
    short_help="Show POST documentation."
)(post_docs)

# pycurl docs put
docs.command(
    name="put",
    short_help="Show PUT documentation."
)(put_docs)

# pycurl docs patch
docs.command(
    name="patch",
    short_help="Show PATCH documentation."
)(patch_docs)

# pycurl docs delete
docs.command(
    name="delete",
    short_help="Show DELETE documentation."
)(delete_docs)

# pycurl docs init
docs.command(
    name="init",
    short_help="Show INIT documentation."
)(init_docs)
