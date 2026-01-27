import json
import requests

from app.utils import TextDisplay

def saveRequestResponse(response: requests.Response, filename: str="request.response.json"):
    """Save the request and response details to a file in JSON format."""

    try:
        data = {
            "request": {
                "method": response.request.method,
                "url": response.request.url,
                "headers": dict(response.request.headers),
                "body": (
                    response.request.body.decode("utf-8")
                    if isinstance(response.request.body, bytes)
                    else response.request.body
                ),
            },
            "response": {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.text,
            },
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        TextDisplay().success_text(f"Request and response saved to {filename}")

    except Exception as e:
        raise SystemExit(TextDisplay().error_text(f"Error saving request and response to file: {e}"))
