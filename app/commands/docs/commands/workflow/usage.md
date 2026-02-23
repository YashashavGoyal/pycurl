# PyCurl Usage Workflow

Follow these steps to get started with PyCurl after installation.

### 1. Initialize PyCurl
The first thing you should do is initialize the application. This creates the necessary configuration and token files.
```bash
pycurl init
```

### 2. Configure PyCurl (Optional)
You can customize the default behavior, such as the default token type or token file location.
```bash
pycurl config generate --interactive
```

### 3. Log In
To make authenticated requests, log in to your API and save the token with an alias.
```bash
pycurl auth login <URL> -j '{"username": "user", "password": "password"}' -a my-app
```

### 4. Use PyCurl
Now you can make authenticated requests using the saved alias.
```bash
pycurl get <URL> -U my-app --show-content
```

### 5. Manage Tokens
List or remove tokens as needed.
```bash
pycurl token list
pycurl token remove --alias my-app
```
