import json
import requests
from typer import Argument, Option

from app.utils import TextDisplay, saveResponseToFile, saveRequestResponse

def post(
    url: str = Argument(..., help="The URL to send the POST request to"),
    save_to_file: str = Option(None, "-o", "--output", help="File path to save the response content"),
    response_format: str = Option("json", "-f", "--format", help="Format to save the response (json or raw)"),
    save_request_to_file: str = Option(None, "-O", "--save-request", "--dump-request", help="File path to save the request details (json format)"),
    show_request: bool = Option(False, "-r", "--show-request", help="Whether to display the full request details"),
    show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
    json_data: str = Option(None, "-j", "--json", help="JSON data to include in the POST request body (use '@filename' to read from file)"),
    data: str = Option(None, "-d", "--data", help="Data to include in the POST request"),
    headers_list: list[str] = Option(None, "-H", "--header", help="Additional headers to include in the POST request"),
):
    """Perform a POST request to the specified URL with the given headers, body and return the response."""
    try:
        headers = {}

        if headers_list:
            for header in headers_list:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()

        if json_data and data:
            raise SystemExit(TextDisplay.error_text("Use either --json or --data, not both"))

        elif json_data:
            headers.setdefault("Content-Type", "application/json")

            if json_data.strip().startswith("@"):
                file_path = json_data.strip()[1:]
                with open(file_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
            else:
                payload = json.loads(json_data)

            response = requests.post(url, json=payload, headers=headers)

        elif data:
            headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
            response = requests.post(url, data=data, headers=headers)

        else:
            response = requests.post(url, headers=headers)

        response.raise_for_status() 
        TextDisplay.style_text(f"POST request to {url} successful.", style="white")
        TextDisplay.success_text(f"Status Code: {response.status_code}")
 
        if save_to_file:
            saveResponseToFile(response, save_to_file, response_format)

        if show_content:
            TextDisplay.info_text("Response Content:", style="white")
            try:
                TextDisplay.print_json(response.json())
            except ValueError:
                print(response.text)

        if save_request_to_file:
            saveRequestResponse(response, save_request_to_file)

        if show_request:
            TextDisplay.info_text("Request Details:")
            TextDisplay.print_json({
                "method": response.request.method,
                "url": response.request.url,
                "headers": dict(response.request.headers),
                "body": (
                    response.request.body.decode("utf-8")
                    if isinstance(response.request.body, bytes)
                    else response.request.body
                )
            })
            # TextDisplay.print_json(response.request.__dict__)

    except requests.exceptions.RequestException as e:
        raise SystemExit(TextDisplay.error_text(f"Error during POST request: {e}"))
    
    except json.JSONDecodeError as jde:
        raise SystemExit(TextDisplay.error_text(f"Invalid JSON data: {jde}"))

    except Exception as ex:
        raise SystemExit(TextDisplay.error_text(f"An error occurred: {ex}"))