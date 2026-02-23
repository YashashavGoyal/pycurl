from pathlib import Path
from app.utils import print_markdown

# pycurl docs delete
def delete_docs():
    """Show documentation for DELETE command."""
    file_path = Path(__file__).parent / "delete.md"
    print_markdown(file_path)
