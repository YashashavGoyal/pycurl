from typer import Typer, Context

from .commands import show, validate, get, set_conf, generate

# Typer app for configuration
config = Typer(
    name="config",
    short_help="Configuration Management Tool for pycurl",
    invoke_without_command=True
)

# alias pycurl config to pycurl config show
@config.callback(
    epilog="""
    EXAMPLES\n
    pycurl config show\n
    pycurl config generate\n
    """
)
def config_callback(ctx: Context):
    """
    Default behavior for `pycurl config`
    """
    if ctx.invoked_subcommand is None:
        show(format="human")


# pycurl config show ...
config.command(
    name="show",
    short_help="Shows or Print the config file",
    epilog="""
    EXAMPLES\n
    pycurl config show\n
    """
)(show)

# pycurl config validate ...
config.command(
    name="validate",
    short_help="validates the syntax of the config file and shows error",
    epilog="""
    EXAMPLES\n
    pycurl config validate\n
    """
)(validate)


# pycurl config get ...
config.command(
    name="get",
    short_help="Fetches asked key from config file",
    epilog="""
    EXAMPLES\n
    pycurl config get auth.token_type\n
    """
)(get)

# pycurl config set ...
config.command(
    name="set",
    help="Used to set any key in config file explictly for user customisation",
    epilog="""
    EXAMPLES\n
    pycurl config set auth.token_type "Bearer"\n
    pycurl config set auth.token_type "Bearer" --file ./tokens/token.json\n
    """
)(set_conf)

# pycurl config generate ...
config.command(
    name="generate",
    short_help="Generate or update the config file for user customisation. [green]Most Recommended[/green]",
    epilog="""
    EXAMPLES\n
    pycurl config generate --interactive\n
    pycurl config generate --reset\n
    """
)(generate)