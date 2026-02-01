import requests
import json
from typer import Argument, Option

from app.utils import TextDisplay, saveRequestResponse, saveResponseToFile, getSavedToken

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
    user_saved_requests: str | None = Option(None, "-U", "--use-token", help="Provide alias to use saved token from token file (type [cyan]default[/cyan] to use the default token)"),
    token_placement: str = Option("header", "-tp", "--token-placement", help="Where to attach the token: 'header' or 'cookie'"),
    token_cookie_name: str = Option("access_token", "-cn", "--cookie-name", help="Name of the cookie if token placement is 'cookie'")
):
    """Perform a DELETE request to the specified URL with optional headers and query parameters."""

    try:
        headers = {}

        if headers_list:
            for header in headers_list:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()

        if user_saved_requests:
            token, token_headers = getSavedToken(user_saved_requests)
            if token_placement.lower() == "header":
                headers.update(token_headers)
            elif token_placement.lower() != "cookie":
                 TextDisplay.warn_text(f"Unknown token placement '{token_placement}', defaulting to header.")
                 headers.update(token_headers)

        request_cookies = {}
        if user_saved_requests and token_placement.lower() == "cookie":
             token, _ = getSavedToken(user_saved_requests)
             request_cookies[token_cookie_name] = token

        if json_data or data:
            TextDisplay.warn_text("DELETE request with body detected (allowed but not widely supported)")

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

            response = requests.delete(url, json=payload, headers=headers, cookies=request_cookies)

        elif data:
            headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
            response = requests.delete(url, data=data, headers=headers, cookies=request_cookies)
        else:
            response = requests.delete(url, headers=headers, cookies=request_cookies)

        if response.status_code >= 400:
            try:
                response_json = response.json()
                TextDisplay.error_text(f"Request failed with status code: {response.status_code}")
                TextDisplay.print_json(response_json)
            except ValueError:
                TextDisplay.error_text(f"Request failed with status code: {response.status_code}")
                print(response.text)
            raise SystemExit(response.status_code) 
        TextDisplay.style_text(f"DELETE request to {url} successful.", style="white")
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
        raise SystemExit(TextDisplay.error_text(f"Error during DELETE request: {e}"))
    
    except json.JSONDecodeError as jde:
        raise SystemExit(TextDisplay.error_text(f"Invalid JSON data: {jde}"))

    except Exception as ex:
        raise SystemExit(TextDisplay.error_text(f"An error occurred: {ex}"))