### post
Perform a POST request. Supports JSON or form data.

**Specific Options:**
- `-j, --json DATA`: JSON data. Use `@file.json` to read from a file.
- `-d, --data DATA`: Form data (URL-encoded).
- `-H, --header KEY:VALUE`: Additional headers.
- `-O, --save-request PATH`: Save request details to a file.
- `-r, --show-request`: Display full request details.

**Common Options:**
- `-o, --output PATH`: Save response content to a file.
- `-f, --format FORMAT`: Format to save the response (`json` or `raw`). Default is `json`.
- `-s, --show-content`: Display the response content in the terminal.
- `-U, --use-token ALIAS`: Use a saved token from the token file. Use `default` for the default token.
- `-tp, --token-placement PLACE`: Where to attach the token: `header` or `cookie`.
- `-cn, --cookie-name NAME`: Name of the cookie if token placement is `cookie`. Default is `access_token`.

**Example:**
```bash
pycurl post https://api.example.com/data --json '{"key": "value"}' --show-content
```
