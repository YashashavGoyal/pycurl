from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.json import JSON
from rich.markdown import Markdown

from pathlib import Path

from typing import Callable, List
import re

# Central Console instance
console = Console()
error_console = Console(stderr=True)

class GlobalMode:
    QUIET = False
    VERBOSE = False
    JSON = False
    NO_COLOR = False

def set_modes(quiet: bool = False, verbose: bool = False, json: bool = False, no_color: bool = False):
    GlobalMode.QUIET = quiet
    GlobalMode.VERBOSE = verbose
    GlobalMode.JSON = json
    GlobalMode.NO_COLOR = no_color
    
    # Configure consoles
    if no_color:
        console.no_color = True
        error_console.no_color = True
    
    if quiet:
        # In quiet mode, we might want to suppress most things, 
        # but COS says "minimize output (errors only)"
        pass

# Display logic for plain and styled text
class TextDisplay:
    DEBUG = "bright_black"
    INFO = "blue"
    WARNING = "yellow"
    ERROR = "red"
    SUCCESS = "green"

    @staticmethod
    def style_text(text: str, style: str, is_debug: bool = False):
        if GlobalMode.QUIET and not is_debug: # If quiet, only allow errors
             return
        if is_debug and not GlobalMode.VERBOSE:
            return
            
        con = error_console if GlobalMode.JSON else console
        con.print(text, style=style)
    
    @staticmethod
    def success_text(text: str, style: str = ""):
        if GlobalMode.QUIET: return
        style_n = f"{style} {TextDisplay.SUCCESS}".strip()
        TextDisplay.style_text(f"✔ {text}", style_n)

    @staticmethod
    def warn_text(text: str, style: str = ""):
        if GlobalMode.QUIET: return
        style_n = f"{style} {TextDisplay.WARNING}".strip()
        TextDisplay.style_text(f"⚠ {text}", style_n)
    
    @staticmethod
    def error_text(text: str, style: str = ""):
        # Errors always show unless redirected
        style_n = f"{style} {TextDisplay.ERROR}".strip()
        con = error_console if GlobalMode.JSON else console
        con.print(f"✖ {text}", style=style_n)
    
    @staticmethod
    def info_text(text: str, style: str = ""):
        if GlobalMode.QUIET: return
        style_n = f"{style} {TextDisplay.INFO}".strip()
        TextDisplay.style_text(f"ℹ {text}", style_n) 

    @staticmethod
    def debug_text(text: str, style: str = ""):
        if not GlobalMode.VERBOSE: return
        style_n = f"{style} {TextDisplay.DEBUG}".strip()
        TextDisplay.style_text(text, style_n, is_debug=True)
    
    @staticmethod
    def print_json(json_data: dict, style: str = "White", is_result: bool = False):
        json_obj = JSON.from_data(json_data, indent=4)
        if is_result and GlobalMode.JSON:
            # Pure JSON to stdout
            console.print(json_obj)
        elif not GlobalMode.JSON:
            console.print(json_obj, style=style)

    @staticmethod
    def print_panel(title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
        if GlobalMode.QUIET: return
        if GlobalMode.JSON:
            return
        panel = Panel(content, title=title, title_align="left", border_style=border_style, style="white", subtitle=subtitle, subtitle_align=subtitle_align)
        console.print(panel)

    @staticmethod
    def psa_error(problem: str, source: str = None, action: str = None):
        """Standardized P-S-A error format: Problem-Source-Action"""
        msg = f"[ERROR] {problem}"
        if source:
            msg += f"\nSource: {source}"
        if action:
            msg += f"\nSuggestion: {action}"
        
        style = f"bold {TextDisplay.ERROR}"
        con = error_console if GlobalMode.JSON else console
        con.print(Panel(msg, title="✖ Error", border_style=TextDisplay.ERROR))

# Panel display utilities
class PanelDisplay:
    ERROR = "bold red"
    SUCCESS = "bold green"
    INFO = "bold blue"
    WARNING = "bold yellow"    

    @staticmethod
    def print_panel( title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
        if GlobalMode.QUIET or GlobalMode.JSON: return
        panel = Panel(content, title=title, title_align="left", border_style=border_style, style="white", subtitle=subtitle, subtitle_align=subtitle_align)
        console.print(panel)

    @staticmethod
    def print_error( title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.ERROR)

    @staticmethod
    def print_success( title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.SUCCESS)
    
    @staticmethod
    def print_info( title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.INFO)
    
    @staticmethod
    def print_warning( title: str, content: str):
        PanelDisplay.print_panel(title, content, border_style=PanelDisplay.WARNING)

    @staticmethod
    def print_json( title: str, json: dict, content: str = "", title_align: str = "left", border_style:str = "gray50"):
        if GlobalMode.QUIET or GlobalMode.JSON: return
        body = Group(
            content,
            JSON.from_data(json, indent=4)
        )
        panel = Panel(
            body,
            title=title,
            title_align=title_align,
            border_style=border_style,
        )
        console.print(panel)

    @staticmethod
    def print_multi_style_panel(
            title: str, 
            content_parts: list, 
            border_style: str = "blue bold",
            title_align: str = "left",
        ):
        if GlobalMode.QUIET or GlobalMode.JSON: return
        combined_content = Text()
        for part, style in content_parts:
            combined_content.append(str(part), style=style)

        panel = Panel(
            combined_content,
            title=title,
            title_align=title_align,
            border_style=border_style,
        )
        console.print(panel)

# Table display utility
class TableDisplay:
    def __init__(self, title: str, columns: list, style: str = "cyan"):
        self.table = Table(title=title)
        for col in columns:
            self.table.add_column(col, style=style, no_wrap=True)

    def add_row(self, row: list, style: str = "cyan"):
        self.table.add_row(*row, style=style)

    def show(self):
        if GlobalMode.QUIET or GlobalMode.JSON: return
        console.print(self.table)

# Logic for user input and prompts
class PromptTaker:

    @staticmethod
    def input_text(
        prompt:str,
        default:str|None = None,
        error_msg:str = "Invalid Input",
        validator:Callable[[str], bool] | None = None,
        max_retries:int = 3
    ) -> str:  
        if GlobalMode.QUIET or GlobalMode.JSON:
             return default if default else ""

        for _ in range(max_retries):
            ans = Prompt.ask(prompt, default=default)

            if validator and not validator(ans):
                TextDisplay.error_text(f"{error_msg}")
                continue
            
            return ans
        
        raise RuntimeError("Maximum Retries Exceeded")

    @staticmethod
    def choices(
        prompt: str,
        choices: List[str],
        default: str | None = None,
    ) -> str:
        if GlobalMode.QUIET or GlobalMode.JSON:
             return default if default else choices[0]

        ans = Prompt.ask(
            prompt=prompt,
            default=default,
            choices=choices
        )
        
        return ans
    
    @staticmethod
    def confirm(
        prompt:str,
        default:bool = False
    ) -> bool:
        if GlobalMode.QUIET or GlobalMode.JSON:
             return default

        ans = Confirm.ask(
                prompt=prompt,
                default=default
            )
        
        return ans


    @staticmethod
    def password(
        prompt:str,
        validator: Callable[[str], bool] | None = None,
        error_msg:str = "Password is not strong",
        max_retries: int = 3
    ):
        if GlobalMode.QUIET or GlobalMode.JSON:
             raise RuntimeError("Non-interactive mode detected. Password input skipped.")

        for _ in range(max_retries):
            passwd = Prompt.ask(
                prompt=prompt,
                password=True
            )
            if validator and not validator(passwd):
                TextDisplay.error_text(f"{error_msg}")
                continue

            return passwd

        raise RuntimeError("Maximum Retries Exceeded")

    @staticmethod # Use a _PromptTaker__strong_password
    def strong_password(
        pwd: str
    ) -> bool:
        return (
            len(pwd) >= 8 and
            bool(re.search(r"[A-Z]", pwd)) and
            bool(re.search(r"[a-z]", pwd)) and
            bool(re.search(r"\d", pwd)) and
            bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd))
        )

# Documentation rendering logic
def print_markdown(path: str, pager: bool = False):
    # if GlobalMode.JSON: return
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Documentation not found at {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    if pager:
        with console.pager(styles=True):
            console.print(Markdown(md_content), width=console.size.width)
    else:
        console.print(Markdown(md_content))
