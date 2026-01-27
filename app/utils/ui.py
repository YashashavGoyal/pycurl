from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

# Text display utilities
class TextDisplay:
    INFO = "blue"
    WARNING = "yellow"
    ERROR = "red"
    SUCCESS = "green"

    def style_text(self, text: str, style: str):
        console.print(f"[{style}]{text}[/{style}]")
    
    def success_text(self, text: str, style: str = ""):
        if style:
            style_n = style + " " + self.SUCCESS
        else:
            style_n = self.SUCCESS
        self.style_text(text, style_n)

    def warn_text(self, text: str, style: str = ""):
        if style:
            style_n = style + " " + self.WARNING
        else:
            style_n = self.WARNING
        self.style_text(text, style_n)
    
    def error_text(self, text: str, style: str = ""):
        if style:
            style_n = style + " " + self.ERROR
        else:
            style_n = self.ERROR
        self.style_text(text, style_n)
    
    def info_text(self, text: str, style: str = ""):
        if style:
            style_n = style + " " + self.INFO
        else:
            style_n = self.INFO
        self.style_text(text, style_n) 
    
    def print_panel(self, title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
        panel = Panel(content, title=title, title_align="left", border_style=border_style, style="white", subtitle=subtitle, subtitle_align=subtitle_align)
        console.print(panel)

# Panel display utilities
class PanelDisplay:
    ERROR = "bold red"
    SUCCESS = "bold green"
    INFO = "bold blue"
    WARNING = "bold yellow"    

    def print_panel(self, title: str, content: str, border_style: str = "blue", subtitle: str = None, subtitle_align: str = "right"):
        panel = Panel(content, title=title, title_align="left", border_style=border_style, style="white", subtitle=subtitle, subtitle_align=subtitle_align)
        console.print(panel)

    def print_error(self, title: str, content: str):
        self.print_panel(title, content, border_style=self.ERROR)

    def print_success(self, title: str, content: str):
        self.print_panel(title, content, border_style=self.SUCCESS)
    
    def print_info(self, title: str, content: str):
        self.print_panel(title, content, border_style=self.INFO)
    
    def print_warning(self, title: str, content: str):
        self.print_panel(title, content, border_style=self.WARNING)

    def print_multi_style_panel(
            self, 
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

# Table display utilities
class TableDisplay:
    def __init__(self, title: str, columns: list, style: str = "cyan"):
        self.table = Table(title=title)
        for col in columns:
            self.table.add_column(col, style=style, no_wrap=True)

    def add_row(self, row: list, style: str = "cyan"):
        self.table.add_row(*row, style=style)

    def show(self):
        console.print(self.table)
