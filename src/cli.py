"""Command line interface for Quantum Blot."""

import typer

app = typer.Typer(help="Quantum Blot command line interface")


@app.callback()
def main() -> None:
    """Entry point for the CLI."""
    pass


if __name__ == "__main__":
    app()