import requests
from typer import Argument, Option
from pprint import pprint

from app.utils import TextDisplay, saveResponseToFile

# pycurl get command logic
def get(
        url: str = Argument(..., help="The URL to send the GET request to"),
        show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
        save_to_file: str = Option(None, "-o", "--output", help="File path to save the response content"),
        response_format: str = Option("json", "-f", "--format", help="Format to save the response (json or raw)")
    ):
    """Perform a GET request to the specified URL and return the response."""
    try:
        response = requests.get(url)
        response.raise_for_status() 
        TextDisplay().style_text(f"GET request to {url} successful.", style="white")
        TextDisplay().success_text(f"Status Code: {response.status_code}")
        
        if show_content:
            TextDisplay().info_text("Response Content:", style="white")
            pprint(response.json())
        if save_to_file:
            saveResponseToFile(response, save_to_file, response_format)

    except requests.exceptions.RequestException as e:
        raise SystemExit(TextDisplay().error_text(f"Error during GET request: {e}"))
    
