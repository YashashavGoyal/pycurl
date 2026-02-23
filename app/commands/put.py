import requests
import json
from typer import Argument, Option

from app.utils import TextDisplay, saveResponseToFile, saveRequestResponse, getSavedToken

# pycurl put
def put(
    url: str = Argument(..., help="The URL to send the PUT request to"),
    save_to_file: str = Option(None, "-o", "--output", help="File path to save the response content"),
    response_format: str = Option("json", "-f", "--format", help="Format to save the response (json or raw)"),
    save_request_to_file: str = Option(None, "-O", "--save-request", "--dump-request", help="File path to save the request details (json format)"),
    show_request: bool = Option(False, "-r", "--show-request", help="Whether to display the full request details"),
    show_content: bool = Option(False, "-s", "--show-content", help="Whether to display the response content"),
    json_data: str = Option(None, "-j", "--json", help="JSON data to include in the PUT request body (use '@filename' to read from file)"),
    data: str = Option(None, "-d", "--data", help="Data to include in the PUT request"),
    headers_list: list[str] = Option(None, "-H", "--header", help="Additional headers to include in the PUT request"),
    user_saved_requests: str | None = Option(None, "-U", "--use-token", help="Provide alias to use saved token from token file (type [cyan]default[/cyan] to use the default token)"),
    token_placement: str = Option("header", "-tp", "--token-placement", help="Where to attach the token: 'header' or 'cookie'"),
    token_cookie_name: str = Option("access_token", "-cn", "--cookie-name", help="Name of the cookie if token placement is 'cookie'")
):
    """
    Perform a PUT request to the specified URL with the given headers, body and return the response.
    """
    try:
        headers = {}

        # Parse headers from list
        if headers_list:
            for header in headers_list:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()

        # Handle authenticated requests
        request_cookies = {}
        if user_saved_requests:
            token, token_headers = getSavedToken(user_saved_requests)
            if token_placement.lower() == "header":
                headers.update(token_headers)
            elif token_placement.lower() == "cookie":
                request_cookies[token_cookie_name] = token
            else:
                 TextDisplay.warn_text(f"Unknown token placement '{token_placement}', defaulting to header.")
                 headers.update(token_headers)

        if not json_data and not data:
            TextDisplay.warn_text("Sending PUT request without a request body")

        if json_data and data:
            raise SystemExit(TextDisplay.error_text("Use either --json or --data, not both"))

        # Handle JSON payload
        elif json_data:
            headers.setdefault("Content-Type", "application/json")

            if json_data.strip().startswith("@"):
                file_path = json_data.strip()[1:]
                with open(file_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
            else:
                payload = json.loads(json_data)

            response = requests.put(url, json=payload, headers=headers, cookies=request_cookies)

        # Handle form data payload
        elif data:
            headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
            response = requests.put(url, data=data, headers=headers, cookies=request_cookies)

        # Handle empty body PUT
        else:
            response = requests.put(url, headers=headers, cookies=request_cookies)

        # Handle failed requests
        if response.status_code >= 400:
            try:
                response_json = response.json()
                TextDisplay.error_text(f"Request failed with status code: {response.status_code}")
                TextDisplay.print_json(response_json)
            except ValueError:
                TextDisplay.error_text(f"Request failed with status code: {response.status_code}")
                print(response.text)
            raise SystemExit(response.status_code) 

        # Success message
        TextDisplay.style_text(f"PUT request to {url} successful.", style="white")
        TextDisplay.success_text(f"Status Code: {response.status_code}")
 
        # Save response if requested
        if save_to_file:
            saveResponseToFile(response, save_to_file, response_format)

        # Display content if requested
        if show_content:
            TextDisplay.info_text("Response Content:", style="white")
            try:
                TextDisplay.print_json(response.json())
            except ValueError:
                print(response.text)

        # Save request/response details
        if save_request_to_file:
            saveRequestResponse(response, save_request_to_file)

        # Show request details
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
        raise SystemExit(TextDisplay.error_text(f"Error during PUT request: {e}"))
    
    except json.JSONDecodeError as jde:
        raise SystemExit(TextDisplay.error_text(f"Invalid JSON data: {jde}"))

    except Exception as ex:
        raise SystemExit(TextDisplay.error_text(f"An error occurred: {ex}"))