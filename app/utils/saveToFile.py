import json
import requests

from app.utils import TextDisplay

# Helper function to save response to file
def saveResponseToFile(response: requests.Response, file_path: str, format: str = "json"):
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

        TextDisplay.success_text(f"Response saved to {file_path}", style="white")
    
    except ValueError as ve:
        raise SystemExit(TextDisplay.error_text(str(ve)))
    
    except Exception as e:
        raise SystemExit(TextDisplay.error_text(f"Error saving response to file: {e}"))