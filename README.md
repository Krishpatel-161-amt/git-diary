# Local Proof of Work Tracker

A small command-line tool for checking the status of Git commits in a local repository. It reads the repository state from Git itself and shows which commits have been pushed and which are still local-only.

This project is designed to work fully offline. It does not rely on any remote API or network call. Instead, it uses Git commands to inspect the repository and display the result in the terminal.

## Features

- Works without a remote API or internet connection
- Checks whether a repository has a remote configured
- Detects commits that are not yet pushed
- Shows recent commit history in a simple table
- Uses Rich to color-code commit status in the terminal

## Requirements

- Python 3.10 or higher
- Git installed and available in your PATH
- Typer
- Rich

## Installation

Clone the repository and install the required packages:

```bash
git clone <your-repository-url>
cd <your-repository-folder>
pip install typer rich
```

## Usage

Run the tracker against the repository you want to inspect:

```bash
python tracker.py /path/to/your/git/project
```

To see the CLI options:

```bash
python tracker.py --help
```

## How it works

The tool uses a few Git commands to build the status report:

- `git log -n 5 --pretty=format:%h|%cd|%s` fetches the latest commits in a fixed format
- `git remote` checks whether the repository has a remote configured
- `git log --branches --not --remotes --format=%h` finds the commit hashes that exist locally but not on the remote

These values are parsed and categorized as:

- pushed
- unpushed
- local only

## Example output

The script displays recent commits in a terminal table with a color for each status:

- pushed: green
- unpushed: yellow
- local only: white

## Notes

This project is intended for quick repository checks during local development. It is useful when you want to confirm which commits are already on a remote and which ones still need to be pushed.
