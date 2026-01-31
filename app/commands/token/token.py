from typer import Typer

from .commands import list_tokens, set_token, remove

# Typer object for subcommand
token = Typer(
    name="token",
    help="Token management utility"
)

# token list ...
token.command(
    name="list",
    short_help="List tokens using alias or all tokens"
)(list_tokens)

# token set ...
token.command(
    name="set",
    short_help="Write new tokens to token file"
)(set_token)

# token remove ...
token.command(
    name="remove",
    short_help="Remove any token alias or all token to remove from token file"
)(remove)
