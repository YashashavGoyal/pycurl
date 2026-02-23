### patch
Perform a PATCH request.

**Basic Example:**
```bash
pycurl patch https://api.example.com/users/1 --json '{"name": "partial-update"}'
```

**With Headers:**
```bash
pycurl patch https://api.example.com/posts/1 --header "Authorization: Bearer <token>" --json '{"title": "Updated"}'
```

**With JSON Body from File:**
```bash
pycurl patch https://api.example.com/resources/1 --json @update.json
```

**Save Response to File:**
```bash
pycurl patch https://api.example.com/posts/1 --json '{"category": "tech"}' -o response.json
```

**Using Saved Token:**
```bash
pycurl patch https://api.example.com/protected/1 --use-token my-alias --json '{"status": "archived"}'
```
