# PyCurl

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Typer](https://img.shields.io/badge/typer-000000?style=for-the-badge&logo=typer&logoColor=white)
![Requests](https://img.shields.io/badge/requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/rich-000000?style=for-the-badge&logo=python&logoColor=white)

![License](https://img.shields.io/github/license/YashashavGoyal/pycurl?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/YashashavGoyal/pycurl?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/YashashavGoyal/pycurl?style=for-the-badge)

PyCurl is a lightweight, modern CLI tool written in Python that brings the power of `curl` with the ergonomics of Python's `requests` library. It provides a user-friendly command-line interface for making HTTP requests, managing authentication, and handling configurations.

## How It Works

PyCurl mimics the simplicity of `curl` but adds structured output and state management.

```mermaid
flowchart LR
    User([👤 User])
    CLI[("💻 PyCurl CLI")]
    Config["⚙️ Config/Auth"]
    Network("🌐 Internet")
    
    subgraph Core ["🔄 Core Logic"]
        direction TB
        Parser["📝 Typer Parser"]
        Requester["🚀 Requests Engine"]
        Formatter["✨ Rich Formatter"]
    end

    User ==>|Command| CLI
    CLI --> Parser
    Parser <--> Config
    Parser --> Requester
    Requester <==>|HTTP/HTTPS| Network
    Requester --> Formatter
    Formatter -->|Pretty Output| User

    classDef plain fill:#1a1a1a,stroke:#fff,color:#fff;
    classDef highlight fill:#22226e,stroke:#f2f0f0,stroke-width:2px,color:#fff;
    class User plain;
    class CLI,Config highlight;
```

## Features

- **Intuitive HTTP Methods**: robust support for `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- **Rich Output**: Beautifully formatted JSON responses and error messages using `rich`.
- **Token Management**:
  - Securely save and manage authentication tokens.
  - Support for custom aliases for tokens.
  - Insert tokens automatically into headers or cookies.
- **Configuration System**:
  - Persist settings across sessions.
  - Easy `init` and `config` commands.
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux.

## 🚀 DevOps & Deployment

We use **GitHub Actions** for our CI/CD pipeline to ensure code quality and automated testing.

### 🔄 CI/CD Pipeline

Our pipeline validates every commit:
1.  **Testing**: Runs unit and integration tests. (will be comming soon)
2.  **Build**: Verifies that the package builds correctly.

## Installation

### Prerequisites
- Python 3.10+

### Install via pip (Development)

```bash
git clone https://github.com/YashashavGoyal/pycurl.git
cd pycurl
pip install .
```

## Usage

### Initialization
Initialize `pycurl` with a default configuration:
```bash
pycurl init
```

### Making Requests

**GET Request**
```bash
pycurl get https://jsonplaceholder.typicode.com/posts/1
```

**POST Request**
```bash
pycurl post https://api.example.com/users -d '{"name": "John", "job": "Dev"}'
```

**Authentication**
Save a token for future use:
```bash
pycurl token save --alias myapi --value eyJhbGciOi...
```
Use the token in a request:
```bash
pycurl get https://api.example.com/protected --token-alias myapi
```

## 📂 Modular Code Structure

```bash
├── app/
│   ├── (commands)/          # Individual CLI Commands
│   │   ├── get.py
│   │   ├── post.py
│   │   ├── auth/            # Auth Management
│   │   └── ...
│   ├── main.py              # Entry Point (Typer App)
│   └── utils/               # Helpers (Display, Parsers)
├── pyproject.toml           # Project Dependencies & Metadata
└── tests/                   # Unit Tests
```

---

**Author**: Yashashav Goyal

<a href="https://github.com/YashashavGoyal">
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</a>
<a href="https://linkedin.com/in/yashashavgoyal">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
<a href="https://twitter.com/YashashavGoyal">
  <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter" />
</a>

**License**: MIT
