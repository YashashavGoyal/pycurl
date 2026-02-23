from pathlib import Path
from app.utils import print_markdown

# pycurl docs get
def get_docs():
    """Show documentation for GET command."""
    file_path = Path(__file__).parent / "get.md"
    print_markdown(file_path)
