from typer import Typer

from .commands import list_tokens, set_token, remove

# Typer object for subcommand
token = Typer(
    name="token",
    help="Token management utility"
)

# pycurl token
@token.callback(
     epilog="""
    EXAMPLES
    pycurl token list\n
    pycurl token set ...
    """
)
def token_callback():
    """
    Token management utility
    """
    pass

# pycurl token list ...
token.command(
    name="list",
    short_help="List tokens using alias or all tokens",
    epilog="""
    EXAMPLES
    pycurl token list\n
    pycurl token list --alias mytoken\n
    """
)(list_tokens)

# pycurl token set ...
token.command(
    name="set",
    short_help="Write new tokens to token file",
    epilog="""
    EXAMPLES
    pycurl token set --alias newtoken --token "ey..."\n
    """
)(set_token)

# pycurl token remove ...
token.command(
    name="remove",
    short_help="Remove any token alias or all token to remove from token file",
    epilog="""
    EXAMPLES
    pycurl token remove --alias oldtoken\n
    pycurl token remove --all\n
    """
)(remove)
