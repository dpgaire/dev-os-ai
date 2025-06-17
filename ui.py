from rich.console import Console, Group
from rich.panel import Panel
from rich.columns import Columns
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme
from typing import Optional
from config import config

# Custom theme for terminal
terminal_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red",
    "success": "bold green",
    "prompt": "bold yellow",
    "code": "grey30",
    "output": "bright_white"
})

console = Console(theme=terminal_theme)

def create_command_panel(title: str, commands: list, color: str = "cyan"):
    """Helper function to create consistent command panels."""
    content = "\n".join(f"[prompt]{cmd}[/prompt]" for cmd in commands)
    return Panel.fit(content, title=f"[bold {color}]{title}[/]", border_style=color)

def display_welcome():
    """Display welcome message with system info and extended command help in horizontal layout."""
    # System info panel
    system_info = f"""
    [bold green]DevOS AI[/bold green] - Your AI Development Assistant
    
    [bold]System Ready[/bold]
    Model: [prompt]{config.model}[/prompt]
    Config: [info]~/.config/devos-ai/config.yaml[/info]
    """
    
    # Create columns of command panels
    command_panels = [
        create_command_panel("Core Commands", [
            "Type prompt + Enter for assistance",
            "!config - Change settings",
            "!exit - Quit the application"
        ], "green"),
        
        create_command_panel("Code Generation", [
            "!bash - Generate Bash scripts",
            "!python - Generate Python code",
            "!js - Generate JavaScript code"
        ], "yellow"),
        
        create_command_panel("File Operations", [
            "!find <pattern> - Find files",
            "!read <file> - Display contents",
            "!edit <file> - Edit file",
            "@file.txt - Analyze file"
        ], "blue"),
        
        create_command_panel("System Control", [
            "!open <app> - Launch apps",
            "!apps - List running apps",
            "!kill <app> - Terminate apps"
        ], "magenta"),
        
        create_command_panel("Git Integration", [
            "!git status - Repository status",
            "!git branch - Current branch",
            "!git diff - Show changes"
        ], "cyan"),
        
        create_command_panel("Web Resources", [
            "!search <query> - Web search",
            "!fetch <url> - Get webpage"
        ], "red")
    ]
    
    # Examples panel
    examples = """
    [bold]Examples:[/bold]
    - "!find *.py src/" - Find Python files
    - "!open Visual Studio Code" - Launch VSCode
    - "!git status" - Check Git status
    - "!search Python async patterns" - Web search
    - "@config.py" - Analyze a file
    """
    
    # Layout the panels
    console.print(Panel.fit(system_info, border_style="green", padding=(1, 2)))
    console.print("\n[bold]Available Commands:[/bold]")
    console.print(Columns(command_panels, equal=True, expand=True))
    console.print(Panel.fit(examples, border_style="yellow", padding=(1, 2)))

def display_response(response: str, language: Optional[str] = None):
    """Display AI response with appropriate formatting."""
    if not response:
        return
        
    if language:
        parts = response.split("```")
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Code block
                code_lines = part.split('\n')
                if len(code_lines) > 1 and code_lines[0].strip() == language:
                    code = '\n'.join(code_lines[1:])
                else:
                    code = part
                
                console.print(Syntax(
                    code, language, theme=config.theme,
                    line_numbers=True,
                    word_wrap=True
                ))
            else:
                console.print(Markdown(part))
    else:
        console.print(Markdown(response))

def display_error(message: str):
    """Display error message in a styled panel."""
    console.print(Panel.fit(
        f"[error]{message}",
        title="[bold]Error[/bold]",
        border_style="red",
        padding=(0, 1)
    ))

def display_success(message: str):
    """Display success message in a styled panel."""
    console.print(Panel.fit(
        f"[success]{message}",
        title="[bold]Success[/bold]",
        border_style="green",
        padding=(0, 1)
    ))

def show_progress(message: str):
    """Display a progress spinner for operations."""
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    )
    task_id = progress.add_task(description=message, total=None)
    progress.start()
    return progress

def hide_progress(progress):
    """Stop the progress spinner."""
    progress.stop()

def display_file_content(content: str, file_path: str):
    """Display file content with syntax highlighting."""
    console.print(f"\n[bold]Contents of [green]{file_path}[/green]:[/bold]")
    extension = file_path.split('.')[-1].lower()
    language = {
        'py': 'python',
        'js': 'javascript',
        'sh': 'bash',
        'md': 'markdown',
        'json': 'json',
        'yaml': 'yaml',
        'yml': 'yaml'
    }.get(extension, 'text')
    
    console.print(Syntax(
        content,
        language,
        theme=config.theme,
        line_numbers=True,
        word_wrap=True
    ))
    
def display_running_apps(apps: list):
    """Special display for running applications list"""
    if not apps:
        display_error("No running applications found")
        return
    
    console.print("\n[bold]Running Applications:[/bold]")
    for i, app in enumerate(apps, 1):
        console.print(f"[cyan]{i}.[/cyan] {app}")