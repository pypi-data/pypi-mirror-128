import os
import subprocess

import click


@click.group(
    help="CLI to manage pytest agent; a service that exposes pytest features via a REST API."
)
def cli():
    ...


@cli.command("start", help="Start pytest agent service")
@click.option(
    "--host",
    default="0.0.0.0",
    type=str,
    help="Specify network address or domain on which service is going to listen",
)
@click.option(
    "--port",
    default=10000,
    type=int,
    help="Specify port of host machine on which service is going to listen",
)
@click.option(
    "--workers",
    default=2,
    type=int,
    help="Defines max number of workers that can process tests simultaneously",
)
def start_pytest_agent(host: str, port: int, workers: int):
    environment = os.environ.copy()
    environment["MAX_WORKER_PROCESSES"] = str(workers)

    subprocess.call(
        ["uvicorn", "pytest_agent.api:api", "--host", host, "--port", str(port)],
        env=environment
    )


if __name__ == "__main__":
    cli()
