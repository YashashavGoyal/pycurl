from typer import Typer, Argument, Option

from app.utils import TextDisplay, authManager

# Typer app for authentication
auth = Typer(
    name="auth",
    help="Manage authentication requests and tokens",
    no_args_is_help=True
)

@auth.callback(
    epilog="""
    EXAMPLES\n
    pycurl auth login ...\n
    pycurl auth register ...\n
    """
)
def auth_callback():
    """
    Manage authentication requests and tokens
    """
    pass

# pycurl auth login ...
@auth.command(
    name="login",
    short_help="Perform login and store authentication token",
    epilog="""
    EXAMPLES\n
    pycurl auth login https://api.example.com/login -j '{"u": "user", "p": "pass"}' --save-alias mytoken\n
    pycurl auth login https://api.example.com/login -j @login.json -t "access_token"\n
    """
)
def login(
    url: str = Argument(..., help="The URL to send the login request to"),
    json_data: str = Option(..., "-j", "--json", help="JSON data for the login request (@file for file input)"),
    show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
    save_to_file: str | None = Option(None, "-o", "--save-to-file", help="File path to save the login response"),
    token_field: str = Option("token", "-t", "--token-field", help="Field name in the response JSON that contains the token"),
    store_token_to_file: str | None = Option(None, "-S", "--store-token", help="Store the token to a specified file"),
    cookie_token: str | None = Option(None, "--cookie-token", help="Key of the cookie to extract the token from"),
    save_alias: str | None = Option(None, "-a", "--save-alias", help="Save the token to the default config with this alias")
):
    """
    Perform a login request to obtain and store an authentication token.
    """
    try:
        authManager(
            url=url,
            json_data=json_data,
            show_content=show_content,
            success_msg="Login successful!",
            save_to_file=save_to_file,
            token_field=token_field,
            store_token_to_file=store_token_to_file,
            cookie_token=cookie_token,
            save_alias=save_alias
        )

    except Exception as e:
        raise SystemExit(TextDisplay.error_text(f"Login failed: {e}"))


# pycurl auth register ...
@auth.command(
    name="register",
    short_help="Perform registration and store authentication token",
    epilog="""
    EXAMPLES\n
    pycurl auth register https://api.example.com/register -j @user.json --save-alias newuser\n
    """
)
def register(
    url: str = Argument(..., help="The URL to send the registration request to"),
    json_data: str = Option(..., "-j", "--json", help="JSON data for the registration request (@file for file input)"),
    show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
    save_to_file: str | None = Option(None, "-o", "--save-to-file", help="File path to save the registration response"),
    token_field: str = Option("token", "-t", "--token-field", help="Field name in the response JSON that contains the token"),
    store_token_to_file: str | None = Option(None, "-S", "--store-token", help="Store the token to a specified file"),
    cookie_token: str | None = Option(None, "--cookie-token", help="Key of the cookie to extract the token from"),
    save_alias: str | None = Option(None, "-a", "--save-alias", help="Save the token to the default config with this alias")
):
    """
    Perform a registration request to obtain and store an authentication token.
    """
    try:
        authManager(
            url=url,
            json_data=json_data,
            show_content=show_content,
            success_msg="Registration successful!",
            save_to_file=save_to_file,
            token_field=token_field,
            store_token_to_file=store_token_to_file,
            cookie_token=cookie_token,
            save_alias=save_alias
        )

    except Exception as e:
        raise SystemExit(TextDisplay.error_text(f"Registration failed: {e}"))