### put
Perform a PUT request.

**Basic Example:**
```bash
pycurl put https://api.example.com/users/1 --json '{"id": 1, "name": "updated"}'
```

**With Headers:**
```bash
pycurl put https://api.example.com/posts/1 --header "Authorization: Bearer <token>" --json '{"title": "Updated Post"}'
```

**With JSON Body from File:**
```bash
pycurl put https://api.example.com/resources/1 --json @payload.json
```

**Save Response to File:**
```bash
pycurl put https://api.example.com/posts/1 --json '{"status": "published"}' -o response.json
```

**Using Saved Token:**
```bash
pycurl put https://api.example.com/protected/1 --use-token my-alias --json '{"active": true}'
```
