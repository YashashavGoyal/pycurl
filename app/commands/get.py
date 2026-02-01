import requests
from typer import Argument, Option

from app.utils import TextDisplay, saveResponseToFile, getSavedToken, CONFIG_PATH

# pycurl get command logic
def get(
        url: str = Argument(..., help="The URL to send the GET request to"),
        show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
        save_to_file: str = Option(None, "-o", "--output", help="File path to save the response content"),
        response_format: str = Option("json", "-f", "--format", help="Format to save the response (json or raw)"),
        user_saved_requests: str | None = Option(None, "-U", "--use-token", help="Provide alias to use saved token from token file (type [cyan]default[/cyan] to use the default token)"),
        token_placement: str = Option("header", "-tp", "--token-placement", help="Where to attach the token: 'header' or 'cookie'"),
        token_cookie_name: str = Option("access_token", "-cn", "--cookie-name", help="Name of the cookie if token placement is 'cookie'")
):
    """Perform a GET request to the specified URL and return the response."""
    try:

        if user_saved_requests:
            token, token_headers = getSavedToken(user_saved_requests, config_path=CONFIG_PATH)
            if token_placement.lower() == "header":
                response = requests.get(url, headers=token_headers)
            elif token_placement.lower() == "cookie":
                response = requests.get(url, cookies={token_cookie_name: token})
            else:
                 TextDisplay.warn_text(f"Unknown token placement '{token_placement}', defaulting to header.")
                 response = requests.get(url, headers=token_headers)
        else:
            response = requests.get(url)

        if response.status_code >= 400:
            try:
                response_json = response.json()
                TextDisplay.error_text(f"Request failed with status code: {response.status_code}")
                TextDisplay.print_json(response_json)
            except ValueError:
                TextDisplay.error_text(f"Request failed with status code: {response.status_code}")
                print(response.text)
            raise SystemExit(response.status_code) 
        TextDisplay.style_text(f"GET request to {url} successful.", style="white")
        TextDisplay.success_text(f"Status Code: {response.status_code}")
        
        if show_content:
            TextDisplay.info_text("Response Content:", style="white")
            try:
                TextDisplay.print_json(response.json())
            except ValueError:
                print(response.text)
        if save_to_file:
            saveResponseToFile(response, save_to_file, response_format)

    except requests.exceptions.RequestException as e:
        raise SystemExit(TextDisplay.error_text(f"Error during GET request: {e}"))
    
