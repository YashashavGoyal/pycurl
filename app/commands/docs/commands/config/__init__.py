from typer import Typer, Context
from pathlib import Path
from app.utils import print_markdown

# Typer object for config documentation
config_docs = Typer(
    name="config",
    help="Documentation for config commands",
    no_args_is_help=True
)


# callback for pycurl docs config
@config_docs.callback(
    invoke_without_command=True
)
def config_docs_callback(ctx: Context):
    """Configuration documentation."""
    if ctx.invoked_subcommand is None:
        # Show all config related docs if no subcommand i.e. all commands inside config
        docs_to_show = ["show.md", "validate.md", "get.md", "set.md", "generate.md"]
        for doc in docs_to_show:
            file_path = Path(__file__).parent / doc
            print_markdown(file_path)


# commands

# pycurl docs config show
@config_docs.command(
    name="show",
    help="Show config show documentation."
)
def show_docs():
    """Show config show documentation."""
    file_path = Path(__file__).parent / "show.md"
    print_markdown(file_path)

# pycurl docs config validate
@config_docs.command(
    name="validate",
    help="Show config validate documentation."
)
def validate_docs():
    """Show config validate documentation."""
    file_path = Path(__file__).parent / "validate.md"
    print_markdown(file_path)

# pycurl docs config get
@config_docs.command(
    name="get",
    help="Show config get documentation."
)
def get_docs():
    """Show config get documentation."""
    file_path = Path(__file__).parent / "get.md"
    print_markdown(file_path)

# pycurl docs config set
@config_docs.command(
    name="set",
    help="Show config set documentation."
)
def set_docs():
    """Show config set documentation."""
    file_path = Path(__file__).parent / "set.md"
    print_markdown(file_path)

# pycurl docs config generate
@config_docs.command(
    name="generate",
    help="Show config generate documentation."
)
def generate_docs():
    """Show config generate documentation."""
    file_path = Path(__file__).parent / "generate.md"
    print_markdown(file_path)
