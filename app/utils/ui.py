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

# Display logic for plain and styled text
class TextDisplay:
    INFO = "blue"
    WARNING = "yellow"
    ERROR = "red"
    SUCCESS = "green"

    @staticmethod
    def style_text(text: str, style: str):
        console.print(text, style=style)
    
    @staticmethod
    def success_text( text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.SUCCESS}".strip()
        TextDisplay.style_text(text, style_n)

    @staticmethod
    def warn_text( text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.WARNING}".strip()
        TextDisplay.style_text(text, style_n)
    
    @staticmethod
    def error_text( text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.ERROR}".strip()
        TextDisplay.style_text(text, style_n)
    
    @staticmethod
    def info_text( text: str, style: str = ""):
        style_n = f"{style} {TextDisplay.INFO}".strip()
        TextDisplay.style_text(text, style_n) 
    
    @staticmethod
    def print_json( json:dict, style: str = "White"):
        json_obj = JSON.from_data(json, indent=4)
        console.print(json_obj, style=style)

    @staticmethod
    def print_panel( title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
        panel = Panel(content, title=title, title_align="left", border_style=border_style, style="white", subtitle=subtitle, subtitle_align=subtitle_align)
        console.print(panel)

# Panel display utilities
class PanelDisplay:
    ERROR = "bold red"
    SUCCESS = "bold green"
    INFO = "bold blue"
    WARNING = "bold yellow"    

    @staticmethod
    def print_panel( title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
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