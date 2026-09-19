import typer
from rich.console import Console
from rich.table import Table
from engine import (
    get_logs, 
    check_remote, 
    get_unpushed_hashes,
    is_valid_repo, 
    split_lines
)

console = Console()

def track(target_directory: str):
    """
    Audits a local Git repository and categorizes commits by pushed/unpushed status
    """
    if not is_valid_repo(target_directory):
        console.print(f"[bold red]Fatal Error:[/] '{target_directory}' is not a valid Git repository.")
        raise typer.Exit(code=1)
    
    raw = get_logs(target_directory)
    has_remote = check_remote(target_directory)
    unpushed_list = get_unpushed_hashes(target_directory)

    parsed = split_lines(raw,has_remote,unpushed_list)

    if not has_remote:
        console.print("[bold yellow]Notice:[/] No upstream remote detected. All commits are local-only.")
        console.print("")

    table = Table(title="Summary Table")
    
    table.add_column("Commit", justify="left")
    table.add_column("Date", justify="center")
    table.add_column("Message", justify="right")
 
    # Iterates over the parsed list of dict to grab the current status and color code it
    for commits in parsed:
        status = commits["status"]
        if status == "pushed":
            color = "dim green"
        elif status == "unpushed":
            color = "bold yellow"
        elif status == "local only":
            color = "white"

        # Wraps the data in color tags
        styled_hash = f"[{color}]{commits['commit']}[/]"
        styled_date = f"[{color}]{commits['date']}[/]"
        styled_message = f"[{color}]{commits['message']}[/]"

        table.add_row(styled_hash, styled_date, styled_message)

    console.print(table)

if __name__ == "__main__":
    typer.run(track)