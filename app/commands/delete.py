import requests
import json
from typer import Argument, Option
from pprint import pprint

from app.utils import TextDisplay, saveRequestResponse, saveResponseToFile

def delete(
    url: str = Argument(..., help="The URL to send the DELETE request to"),
    save_to_file: str = Option(None, "-o", "--output", help="File path to save the response content"),
    response_format: str = Option("json", "-f", "--format", help="Format to save the response (json or raw)"),
    save_request_to_file: str = Option(None, "-O", "--save-request", "--dump-request", help="File path to save the request details (json format)"),
    show_request: bool = Option(False, "-r", "--show-request", help="Whether to display the full request details"),
    show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
    json_data: str = Option(None, "-j", "--json", help="JSON data to include in the DELETE request body (use '@filename' to read from file)"),
    data: str = Option(None, "-d", "--data", help="Data to include in the DELETE request"),
    headers_list: list[str] = Option(None, "-H", "--header", help="Additional headers to include in the DELETE request"),

):
    """Perform a DELETE request to the specified URL with optional headers and query parameters."""

    try:
        headers = {}

        if headers_list:
            for header in headers_list:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()

        if json_data or data:
            TextDisplay().warn_text("DELETE request with body detected (allowed but not widely supported)")

        if json_data and data:
            raise SystemExit(TextDisplay().error_text("Use either --json or --data, not both"))

        elif json_data:
            headers.setdefault("Content-Type", "application/json")

            if json_data.strip().startswith("@"):
                file_path = json_data.strip()[1:]
                with open(file_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
            else:
                payload = json.loads(json_data)

            response = requests.delete(url, json=payload, headers=headers)

        elif data:
            headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
            response = requests.delete(url, data=data, headers=headers)
        else:
            response = requests.delete(url, headers=headers)

        response.raise_for_status() 
        TextDisplay().style_text(f"DELETE request to {url} successful.", style="white")
        TextDisplay().success_text(f"Status Code: {response.status_code}")
 
        if save_to_file:
            saveResponseToFile(response, save_to_file, response_format)

        if show_content:
            TextDisplay().info_text("Response Content:", style="white")
            try:
                pprint(response.json())
            except ValueError:
                print(response.text)

        if save_request_to_file:
            saveRequestResponse(response, save_request_to_file)

        if show_request:
            TextDisplay().info_text("Request Details:")
            pprint({
                "method": response.request.method,
                "url": response.request.url,
                "headers": dict(response.request.headers),
                "body": (
                    response.request.body.decode("utf-8")
                    if isinstance(response.request.body, bytes)
                    else response.request.body
                )
            })
            # pprint(response.request.__dict__)

    except requests.exceptions.RequestException as e:
        raise SystemExit(TextDisplay().error_text(f"Error during DELETE request: {e}"))
    
    except json.JSONDecodeError as jde:
        raise SystemExit(TextDisplay().error_text(f"Invalid JSON data: {jde}"))

    except Exception as ex:
        raise SystemExit(TextDisplay().error_text(f"An error occurred: {ex}"))