from pathlib import Path
from app.utils import print_markdown

# pycurl docs patch
def patch_docs():
    """Show documentation for PATCH command."""
    file_path = Path(__file__).parent / "patch.md"
    print_markdown(file_path)
