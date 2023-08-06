import click
import requests
import yaml

from gainr.api import APP


@click.group()
def cli():
    pass


@cli.command()
@click.option("--host", default="0.0.0.0",
              help="server host", envvar="HOST")
@click.option("--port", default=5000, type=int,
              help="server port", envvar="PORT")
def serve(host, port):
    APP.run(host=host, port=port, debug=True)


@cli.command()
@click.option("-c", "--config", "config_file", required=True, help="config file")
@click.option("--ch", "ch_levels", type=(int, int), multiple=True, help="level for a particular channel (e.g. --ch 0 240)")
def set(config_file, ch_levels):
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for ch_level in ch_levels:
        ch, level = ch_level
        config["channels"][ch] = level

    with requests.post(config["endpoint"] + "/api/channels", json=config) as resp:
        message = f"status code: {resp.status_code} message: {resp.json()['message']}"
        if resp.status_code != 200:
            print(f"Error: {message}")
            return
        print(f"OK: {message}")
