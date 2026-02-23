### auth login
Perform login and store the obtained token.

**Options:**
- `-j, --json DATA`: Login credentials.
- `-t, --token-field FIELD`: JSON field in response containing the token. Default is `token`.
- `-a, --save-alias ALIAS`: Save token with this alias for future use.

**Example:**
```bash
pycurl auth login https://api.example.com/login -j @creds.json -a my-app
```
