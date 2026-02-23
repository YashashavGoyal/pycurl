from pathlib import Path
from app.utils import print_markdown

# pycurl docs put
def put_docs():
    """Show documentation for PUT command."""
    file_path = Path(__file__).parent / "put.md"
    print_markdown(file_path)
