from typer import Typer, Context
from pathlib import Path
from app.utils import print_markdown

# Typer object for auth documentation
auth_docs = Typer(
    name="auth",
    help="Documentation for auth commands"
)

# callback for pycurl docs auth
@auth_docs.callback(
    invoke_without_command=True
)
def auth_docs_callback(ctx: Context):
    """Authentication and Tokens documentation."""
    if ctx.invoked_subcommand is None:
        # Show both login and register docs if no subcommand i.e. all commands inside auth
        file_path = Path(__file__).parent / "login.md"
        print_markdown(file_path)
        file_path = Path(__file__).parent / "register.md"
        print_markdown(file_path)  
    

# commands

# pycurl docs auth login
@auth_docs.command(
    name="login",
    help="Show login documentation."
)
def login():
    """Show login documentation."""
    file_path = Path(__file__).parent / "login.md"
    print_markdown(file_path)


# pycurl docs auth register
@auth_docs.command(
    name="register",
    help="Show register documentation."
)
def register():
    """Show register documentation."""
    file_path = Path(__file__).parent / "register.md"
    print_markdown(file_path)  
