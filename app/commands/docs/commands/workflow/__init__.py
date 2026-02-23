from typer import Typer
from pathlib import Path
from app.utils import print_markdown

# Typer object for workflow documentation
workflow_docs = Typer(
    name="workflow",
    help="Documentation for PyCurl workflows",
    epilog="""
    EXAMPLES\n
    pycurl workflow
    pycurl docs workflow
    """
)

# callback for pycurl docs workflow
@workflow_docs.callback(
    invoke_without_command=True
)
def workflow_docs_callback():
    """Show the general usage workflow."""
    file_path = Path(__file__).parent / "usage.md"
    print_markdown(file_path)
