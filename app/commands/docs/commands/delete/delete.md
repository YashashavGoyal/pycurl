### delete
Perform a DELETE request.

**Basic Example:**
```bash
pycurl delete https://api.example.com/users/1
```

**With Headers:**
```bash
pycurl delete https://api.example.com/posts/1 --header "Authorization: Bearer <token>"
```

**With JSON Body:**
```bash
pycurl delete https://api.example.com/resources/1 --json '{"reason": "obsolete"}'
```

**With JSON Body from File:**
```bash
pycurl delete https://api.example.com/resources/1 --json @payload.json
```

**Save Response to File:**
```bash
pycurl delete https://api.example.com/posts/1 -o response.json
```

**Show Request Details:**
```bash
pycurl delete https://api.example.com/posts/1 -r
```

**Using Saved Token:**
```bash
pycurl delete https://api.example.com/protected/1 --use-token my-alias
```
