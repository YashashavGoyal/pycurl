from typer import Typer, Context
from pathlib import Path
from app.utils import print_markdown

# Typer object for token documentation
token_docs = Typer(
    name="token",
    help="Documentation for token commands"
)


# callback for pycurl docs token
@token_docs.callback(
    invoke_without_command=True
)
def token_docs_callback(ctx: Context):
    """Token management documentation."""
    if ctx.invoked_subcommand is None:
        # Show all token related docs if no subcommand i.e. all commands inside token
        docs_to_show = ["list.md", "set.md", "remove.md"]
        for doc in docs_to_show:
            file_path = Path(__file__).parent / doc
            print_markdown(file_path)


# commands

# pycurl docs token list
@token_docs.command(
    name="list",
    help="Show token list documentation."
)
def list_docs():
    """Show token list documentation."""
    file_path = Path(__file__).parent / "list.md"
    print_markdown(file_path)

# pycurl docs token set
@token_docs.command(
    name="set",
    help="Show token set documentation."
)
def set_docs():
    """Show token set documentation."""
    file_path = Path(__file__).parent / "set.md"
    print_markdown(file_path)

# pycurl docs token remove
@token_docs.command(
    name="remove",
    help="Show token remove documentation."
)
def remove_docs():
    """Show token remove documentation."""
    file_path = Path(__file__).parent / "remove.md"
    print_markdown(file_path)

