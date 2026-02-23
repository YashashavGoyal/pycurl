from pathlib import Path
from app.utils import print_markdown

# pycurl docs post
def post_docs():
    """Show documentation for POST command."""
    file_path = Path(__file__).parent / "post.md"
    print_markdown(file_path)
