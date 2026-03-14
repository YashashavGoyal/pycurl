import requests
import json

from .ui import TextDisplay, PSAException
from .saveToFile import saveResponseToFile
from .configParser import loadAndValidateConfig, extractConfigAttributes
from .tokenParser import (
    alias_validator,
    storeTokenToFile,
    saveTokenToDefaultConfig
)

# Authentication logic for auth login / register commands
def authManager(
    *,
    url: str,
    json_data: str,
    show_content: bool = False,
    success_msg: str,
    save_to_file: str | None = None,
    token_field: str = "token",
    store_token_to_file: str | None = None,
    cookie_token: str | None = None,
    save_alias: str | None = None
) -> tuple[requests.Response, str | None]:
    """
    Authenticate a user by sending a POST request to the specified URL with JSON data.
    """
    try:
        headers = {"Content-Type": "application/json"}

        # Handle payload input (direct JSON or file)
        if json_data.strip().startswith("@"):
            file_path = json_data.strip()[1:]
            TextDisplay.debug_text(f"Reading auth payload from file: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        else:
            TextDisplay.debug_text("Parsing inline JSON auth payload")
            payload = json.loads(json_data)

        # Send authentication request
        TextDisplay.debug_text(f"Sending POST request to: {url}")
        TextDisplay.debug_text(f"Headers: {headers}")
        response = requests.post(url, json=payload, headers=headers)
        TextDisplay.debug_text(f"Response received in {response.elapsed.total_seconds():.3f}s")

        try:
            response_json = response.json()
        except ValueError:
            TextDisplay.debug_text("Response body is not valid JSON")
            response_json = {"message": response.text}

        # Handle request failure
        if response.status_code >= 400:
            TextDisplay.debug_text(f"Authentication failed with status {response.status_code}")
            raise PSAException(
                problem=response_json.get("message", "Authentication failed"),
                source=f"POST {url}",
                action="Check your credentials and the URL. The service might be offline or requiring different credentials.",
                exit_code=response.status_code
            )

        # Success messages
        TextDisplay.style_text(success_msg, style="white")
        TextDisplay.success_text(f"Status Code: {response.status_code}")

        # Save response if requested
        if save_to_file:
            saveResponseToFile(response, save_to_file, "json")

        # Display content if requested
        if show_content:
            TextDisplay.info_text("Response Content:", style="white")
            try:
                TextDisplay.print_json(response.json())
            except ValueError:
                print(response.text)

        # Handle token storage logic
        token: str | None = None
        if store_token_to_file or save_alias:
            if cookie_token:
                TextDisplay.debug_text(f"Extracting token from cookie: '{cookie_token}'")
                token = response.cookies.get(cookie_token)
                if not token:
                    TextDisplay.warn_text(f"Token cookie '{cookie_token}' not found in response.")
            else:
                TextDisplay.debug_text(f"Extracting token from JSON field: '{token_field}'")
                token = getAuthTokenFromResponse(response, token_field)
            
            if store_token_to_file:
                storeTokenToFile(token, store_token_to_file)
                TextDisplay.style_text(f"Token stored to file '{store_token_to_file}'.", style="white")
            
            if save_alias and token:
                saveTokenToDefaultConfig(token, save_alias)
                TextDisplay.success_text(f"Token saved to default config with alias '{save_alias}'")

        return response, token

    except requests.exceptions.RequestException as e:
        raise PSAException(
            problem=f"Error during authentication request: {e}",
            source="Requests Library",
            action="Verify your network connection and the URL format."
        )

    except json.JSONDecodeError as jde:
        raise PSAException(
            problem=f"Invalid JSON data: {jde}",
            source="JSON Decoder",
            action="Check the format of your --json payload."
        )

    except Exception as ex:
        if isinstance(ex, PSAException):
            raise ex
        raise PSAException(
            problem=f"An error occurred: {ex}",
            source="Authentication Logic",
            action="Please report this issue if it persists."
        )

# Token extraction logic
def getAuthTokenFromResponse(
    response: requests.Response,
    token_field: str = "token"
) -> str:
    """Extract the authentication token from the response JSON."""
    try:
        response_json = response.json()
        token = response_json.get(token_field)

        if not token:
            raise PSAException(
                problem=f"Token field '{token_field}' not found in the response.",
                source="Token Extraction",
                action="Specify the correct token field using --token-field."
            )

        return token

    except json.JSONDecodeError:
        raise PSAException(
            problem="Response is not valid JSON.",
            source="JSON Decoder",
            action="The auth endpoint must return a JSON response containing the token."
        )
