import requests
import json
from typer import Argument, Option
from pprint import pprint
from app.utils.ui import TextDisplay

# pycurl get command logic
def get(
        url: str = Argument(..., help="The URL to send the GET request to"),
        show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
        save_to_file: str = Option(None, "-o", "--output", help="File path to save the response content"),
        response_format: str = Option("raw", "-f", "--format", help="Format to save the response (json or raw)")
    ):
    """Perform a GET request to the specified URL and return the response."""
    try:
        response = requests.get(url)
        response.raise_for_status() 
        TextDisplay().style_text(f"GET request to {url} successful.", style="white")
        TextDisplay().success_text(f"Status Code: {response.status_code}")
        
        if show_content:
            TextDisplay().info_text("Response Content:", style="white")
            pprint(response.text)
        if save_to_file:
            save_response_to_file(response, save_to_file, response_format)

    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error during GET request: {e}")
    


# Helper function to save response to file
def save_response_to_file(response: requests.Response, file_path: str, format: str = "json"):
    """Save the response content to a file."""

    try:
        if format not in ["json", "raw"]:
            raise ValueError("Unsupported format. Use 'json' or 'raw'.")

        with open(file_path, "w", encoding="utf-8") as f:
            if format == "json":

                if 'application/json' not in response.headers.get('Content-Type', ''):
                    raise ValueError("Response content is not in JSON format.")

                json.dump(response.json(), f, indent=4)
            else:
                f.write(response.text)

        TextDisplay().success_text(f"Response saved to {file_path}", style="white")
    
    except ValueError as ve:
        raise SystemExit(TextDisplay().error_text(str(ve)))
    
    except Exception as e:
        raise SystemExit(TextDisplay().error_text(f"Error saving response to file: {e}"))