from pathlib import Path
from app.utils import print_markdown

# pycurl docs init
def init_docs():
    """Show documentation for INIT command."""
    file_path = Path(__file__).parent / "init.md"
    print_markdown(file_path)
