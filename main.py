import click
from rich.syntax import Syntax
from ui import (
    console,
    display_welcome,
    display_response,
    display_error,
    show_progress,
)
from ai_client import AIClient
from utils import detect_language, get_file_content
from config import config
from os_ops.file_handling import FileHandler
from os_ops.app_control import AppController
from os_ops.git_utils import GitManager
from os_ops.web_resources import WebResourceFinder


@click.group()
@click.version_option("0.1.0", prog_name="DevOS AI")
def cli():
    """DevOS AI - Your AI Development Assistant"""
    pass


@cli.command()
def chat():
    """Start interactive chat session"""
    display_welcome()
    ai_client = AIClient()

    while True:
        try:
            prompt = click.prompt("\n[devos-ai]", prompt_suffix=" >>> ")

            if prompt.lower() in ('exit', 'quit', '!exit', '!quit'):
                click.echo("Exiting DevOS AI. Goodbye!")
                break
            
            if prompt.startswith('!apps'):
                apps = AppController.list_running_apps()
                display_response("Running applications:\n" + "\n".join(apps))
                continue

            # Handle special commands
            if prompt.startswith('!config'):
                handle_config_command(prompt)
                continue

            elif prompt.startswith('!git'):
                repo_path = prompt[4:].strip() or '.'
                status = GitManager.get_status(repo_path)
                if 'error' in status:
                    display_error(status['error'])
                else:
                    display_response(
                        f"Git status for {repo_path}:\nBranch: {status['branch']}\n{status['status']}"
                    )
                continue

            elif prompt.startswith('!open'):
                app_name = prompt[5:].strip()
                result = AppController.open_app(app_name)
                display_response(result)
                continue

            elif prompt.startswith('!find'):
                pattern = prompt[5:].strip()
                files = FileHandler.find_files(pattern)
                display_response("Found files:\n" + "\n".join(files))
                continue

            elif prompt.startswith('!search'):
                query = prompt[7:].strip()
                results = WebResourceFinder.search_web(query)
                display_response("Web results:\n" + "\n".join(results))
                continue

            # Handle file input
            if prompt.startswith('@'):
                file_path = prompt[1:].strip()
                file_content = get_file_content(file_path)
                if file_content:
                    prompt = f"Analyze this file:\n```\n{file_content}\n```"
                else:
                    display_error(f"File not found: {file_path}")
                    continue

            # Detect language
            language, clean_prompt = detect_language(prompt)
            if not clean_prompt:
                continue

            # Get AI response
            with show_progress("Processing..."):
                response = ai_client.send_prompt(clean_prompt)

            if "error" in response:
                display_error(response["error"])
            else:
                ai_response = response.get("choices", [{}])[0].get("message", {}).get("content", "")
                if ai_response:
                    display_response(ai_response, language)
                else:
                    display_error("Received empty response from AI")

        except KeyboardInterrupt:
            click.echo("\nExiting DevOS AI. Goodbye!")
            break
        except Exception as e:
            display_error(f"An error occurred: {str(e)}")
            continue


def handle_config_command(prompt: str):
    """Handle configuration commands."""
    args = prompt.split()[1:]

    if not args:
        click.echo("\nCurrent Configuration:")
        click.echo(f"Model: {config.model}")
        click.echo(f"Theme: {config.theme}")
        click.echo(f"Max Tokens: {config.max_tokens}")
        click.echo(f"Temperature: {config.temperature}")
        return

    if args[0] == "set":
        if len(args) < 3:
            display_error("Usage: !config set <key> <value>")
            return

        key, value = args[1], args[2]
        try:
            if key == "model":
                config.model = value
            elif key == "theme":
                config.theme = value
            elif key == "max_tokens":
                config.max_tokens = int(value)
            elif key == "temperature":
                config.temperature = float(value)
            else:
                display_error(f"Invalid config key: {key}")
                return

            config.save_config()
            click.echo(f"Updated {key} to {value}")
        except ValueError as e:
            display_error(f"Invalid value: {str(e)}")


@cli.command()
@click.argument('path', default='.')
def git_status(path):
    """Show Git status for a repository"""
    status = GitManager.get_status(path)
    if 'error' in status:
        display_error(status['error'])
    else:
        console.print(f"\nGit Status for [bold]{path}[/bold]")
        console.print(f"Branch: [green]{status['branch']}[/green]")
        console.print("Changes:")
        console.print(Syntax(status['status'], 'diff', theme=config.theme))


@cli.command()
@click.argument('app_name')
def open_app(app_name):
    """Open an application"""
    result = AppController.open_app(app_name)
    console.print(result)


@cli.command()
@click.argument('pattern')
@click.argument('directory', default='.')
def find_files(pattern, directory):
    """Find files matching pattern"""
    files = FileHandler.find_files(pattern, directory)
    console.print("\nFound files:")
    for file in files:
        console.print(f"- [green]{file}[/green]")


@cli.command()
@click.argument('query')
def web_search(query):
    """Search the web for resources"""
    results = WebResourceFinder.search_web(query)
    console.print(f"\nTop resources for [bold]{query}[/bold]:")
    for i, url in enumerate(results, 1):
        console.print(f"{i}. [blue][link={url}]{url}[/link][/blue]")


if __name__ == "__main__":
    cli()
