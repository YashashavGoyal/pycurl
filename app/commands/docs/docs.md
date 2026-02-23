# PyCurl Documentation

PyCurl is a lightweight, curl-like CLI tool written in Python using the `requests` library. It provides a user-friendly interface for making HTTP requests, managing authentication tokens, and configuring application behavior.

## Usage

You can view the full documentation by running:
```bash
pycurl docs
```

You can also view documentation for specific commands by appending the command name:
```bash
pycurl docs <command>
```

**Examples:**
```bash
pycurl docs get
pycurl docs auth login
pycurl docs config generate
```

## Table of Contents
- [Installation](#installation)
- [Global Commands](#global-commands)
- [Request Commands](#request-commands)
    - [get](#get)
    - [post](#post)
    - [put](#put)
    - [patch](#patch)
    - [delete](#delete)
- [Authentication and Tokens](#authentication-and-tokens)
    - [auth login](#auth-login)
    - [auth register](#auth-register)
    - [token list](#token-list)
    - [token set](#token-set)
    - [token remove](#token-remove)
- [Configuration](#configuration)
    - [init](#init)
    - [config show](#config-show)
    - [config set](#config-set)
    - [config get](#config-get)
    - [config validate](#config-validate)
    - [config generate](#config-generate)
- [Workflows](#workflows)

---

## Installation

Ensure you have Python installed. Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
python -m app.main init
```

---

## Global Commands

### version
Show the version of PyCurl.
```bash
pycurl version
```

### about
Show information about PyCurl.
```bash
pycurl about
```

### workflow
Show the general usage workflow.
```bash
pycurl workflow
```

---

## Request Commands

All request commands (`get`, `post`, `put`, `patch`, `delete`) share the following common options:

- `-o, --output PATH`: Save response content to a file.
- `-f, --format FORMAT`: Format to save the response (`json` or `raw`). Default is `json`.
- `-s, --show-content`: Display the response content in the terminal.
- `-O, --save-request PATH`: Save request details (JSON format) to a file.
- `-r, --show-request`: Display full request details in the terminal.
- `-H, --header KEY:VALUE`: Additional headers to include in the request. Can be used multiple times.
- `-U, --use-token ALIAS`: Use a saved token from the token file. Use `default` for the default token.
- `-tp, --token-placement PLACE`: Where to attach the token: `header` or `cookie`.
- `-cn, --cookie-name NAME`: Name of the cookie if token placement is `cookie`. Default is `access_token`.

### get
Perform a GET request.
```bash
pycurl get <URL> [OPTIONS]
```
**Example:**
```bash
pycurl get https://jsonplaceholder.typicode.com/posts/1 --show-content
```

### post
Perform a POST request. Supports JSON or form data.
- `-j, --json DATA`: JSON data. Use `@file.json` to read from a file.
- `-d, --data DATA`: Form data (URL-encoded).

**Example:**
```bash
pycurl post https://api.example.com/data --json '{"key": "value"}' --show-content
```

### put
Perform a PUT request. Similar options to `post`.
```bash
pycurl put <URL> --json '{"id": 1, "name": "updated"}'
```

### patch
Perform a PATCH request. Similar options to `post`.
```bash
pycurl patch <URL> --json '{"name": "partial-update"}'
```

### delete
Perform a DELETE request.
```bash
pycurl delete <URL> --use-token my-alias
```

---

## Authentication and Tokens

### auth login
Perform login and store the obtained token.
- `-j, --json DATA`: Login credentials (JSON). Use `@file.json` to read from a file.
- `-s, --show-content`: Display the response content.
- `-o, --save-to-file PATH`: File path to save the full login response.
- `-t, --token-field FIELD`: JSON field in response containing the token. Default is `token`.
- `-S, --store-token PATH`: Store the extracted token to a specific file.
- `--cookie-token KEY`: Key of the cookie to extract the token from (if returned in cookies).
- `-a, --save-alias ALIAS`: Save token with this alias in the PyCurl config for future use.

**Example:**
```bash
pycurl auth login https://api.example.com/login -j @creds.json -a my-app
```

### auth register
Perform registration and store the token. Supports the same options as `auth login`.
```bash
pycurl auth register https://api.example.com/register -j @user.json -a new-user
```

### token list
List saved tokens.
```bash
pycurl token list [--alias ALIAS]
```

### token set
Manually save a token to the token file.
```bash
pycurl token set --alias my-token --token "EY..."
```

### token remove
Remove a token or all tokens.
```bash
pycurl token remove --alias my-token
pycurl token remove --all
```

---

## Configuration

### init
Initialize the application with default config and token files.
- `-t, --token-file-path PATH`: Custom path for the token file.
- `-o, --overwrite`: Overwrite existing configuration.

### config show
Display the current configuration.
```bash
pycurl config show
```

### config set
Set a specific configuration key.
```bash
pycurl config set token_type "Bearer"
```

### config validate
Check for syntax errors in the configuration file.
```bash
pycurl config validate
```

### config generate
Comprehensive tool to manage or update the configuration. [Recommended]

**Options:**
- `-i, --interactive`: Enable interactive wizard mode to configure path, type, and alias.
- `-m, --modify`: Update or modify the existing configuration file.
- `-o, --overwrite`: Generate a new configuration and overwrite the existing file.
- `-r, --reset`: Reset the configuration file to defaults.
- `-s, --show`: Display the current configuration content.
- `-b, --backup`: Create a timestamped backup of the current config before modifying.
- `--dry-run`: Preview the final configuration and ask for confirmation before writing (works with default or `--modify`).

**Example:**
```bash
pycurl config generate --interactive --backup
```

---

## Workflows

### workflow
The `workflow` command provides guided documentation for common usage patterns in PyCurl. It is designed to help users get started quickly with typical tasks.

```bash
pycurl workflow
```
OR
```bash
pycurl docs workflow
```
