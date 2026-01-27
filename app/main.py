from typer import Typer


app = Typer(
    name="pycurl", 
    help="A lightweight curl-like CLI tool written in Python using requests")

@app.command(
    name="version",
    short_help="Show the version of PyCurl"
)
def version():
    """Show the version of PyCurl"""
    print(f"PyCurl version: 0.1.0")

if __name__ == "__main__":
    app()