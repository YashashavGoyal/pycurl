### get
Perform a GET request.
```bash
pycurl get <URL> [OPTIONS]
```

**Common Options:**
- `-o, --output PATH`: Save response content to a file.
- `-f, --format FORMAT`: Format to save the response (`json` or `raw`). Default is `json`.
- `-s, --show-content`: Display the response content in the terminal.
- `-U, --use-token ALIAS`: Use a saved token from the token file. Use `default` for the default token.
- `-tp, --token-placement PLACE`: Where to attach the token: `header` or `cookie`.
- `-cn, --cookie-name NAME`: Name of the cookie if token placement is `cookie`. Default is `access_token`.

**Example:**
```bash
pycurl get https://jsonplaceholder.typicode.com/posts/1 --show-content
```
