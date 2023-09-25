from typing import Optional

import typer

from polaris.hub.client import PolarisHubClient

app = typer.Typer(
    add_completion=False,
    help="Polaris is a framework for benchmarking methods in drug discovery.",
)


@app.command("login", help="Log in to the Polaris Hub")
def login(
    client_env_file: Optional[str] = None,
    auto_open_browser: bool = True,
    overwrite: bool = False,
):
    """Uses the OAuth2 protocol to gain token-based access to the Polaris Hub API"""
    with PolarisHubClient(env_file=client_env_file) as client:
        client.login(auto_open_browser=auto_open_browser, overwrite=overwrite)


if __name__ == "__main__":
    app()
