import requests
import json

from app.utils import TextDisplay, saveResponseToFile


# Authentication Logic for auth login / register
def authManager(
    *,
    url: str,
    json_data: str,
    show_content: bool = False,
    success_msg: str,
    save_to_file: str | None = None,
    token_field: str = "token",
    store_token_to_file: str | None = None
) -> tuple[requests.Response, str | None]:
    
    """Authenticate a user by sending a POST request to the specified URL with JSON data."""

    try:
        headers = {"Content-Type": "application/json"}

        if json_data.strip().startswith("@"):
            file_path = json_data.strip()[1:]
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        else:
            payload = json.loads(json_data)

        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()
        TextDisplay.style_text(success_msg, style="white")
        TextDisplay.success_text(f"Status Code: {response.status_code}")

        if save_to_file:
            saveResponseToFile(response, save_to_file, "json")

        if show_content:
            TextDisplay.info_text("Response Content:", style="white")
            try:
                TextDisplay.print_json(response.json())
            except ValueError:
                print(response.text)

        token: str | None = None
        if store_token_to_file:
            token = getAuthTokenFromResponse(response, token_field)
            storeTokenToFile(token, store_token_to_file)

        return response, token

    except requests.exceptions.RequestException as e:
        raise SystemExit(TextDisplay.error_text(f"Error during authentication request: {e}"))

    except json.JSONDecodeError as jde:
        raise SystemExit(TextDisplay.error_text(f"Invalid JSON data: {jde}"))

    except Exception as ex:
        raise SystemExit(TextDisplay.error_text(f"An error occurred: {ex}"))
    
def getAuthTokenFromResponse(
    response: requests.Response,
    token_field: str = "token"
) -> str:
    """Extract the authentication token from the response JSON."""
    try:
        response_json = response.json()
        token = response_json.get(token_field)

        if not token:
            raise ValueError(f"Token field '{token_field}' not found in the response.")

        return token

    except json.JSONDecodeError:
        raise SystemExit(TextDisplay.error_text("Response is not valid JSON."))

    except Exception as e:
        raise SystemExit(TextDisplay.error_text(f"Error extracting token: {e}"))

def storeTokenToFile(token: str, file_path: str):
    """Store the authentication token to a specified file."""
    if not token:
        TextDisplay.error_text("No token provided to store in file.")
        TextDisplay.info_text("Ensure TOKEN_FIELD is correct and the response contains the token.")
        raise SystemExit(1)

    if not file_path:
        raise ValueError(
            TextDisplay.error_text("No file path provided to store the token.")
            )

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(token)
        TextDisplay.style_text(f"Token stored to file '{file_path}'.", style="white")

    except Exception as e:
        raise SystemExit(TextDisplay.error_text(f"Error storing token to file: {e}"))