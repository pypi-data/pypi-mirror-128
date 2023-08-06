import click
import re
from art import text2art

try:
    from helpers.web3Helper import w3
    from service import dashboard_service, stake_service
    from __version__ import __version__
except ImportError:
    from .helpers.web3Helper import w3
    from .service import dashboard_service, stake_service
    from .__version__ import __version__

user_hmny_addr = "0x18bdAD1211eed7808Dbca6Beb6a387F5F9c77Efd"
hmny_addr_pattern = re.compile(r"^0x[a-fA-F0-9]{40}$")


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--address", "-a", help="Set the account address in '0x' format")
@click.option("-v", "--version", help="Version of the app", is_flag=True)
def euphoria(ctx, address, version):
    if version:
        click.echo(__version__)
    elif address:
        res = hmny_addr_pattern.match(str(address))
        if res:
            user_hmny_addr = w3.toChecksumAddress(address)
            click.echo(f"Address saved => {address}")
        else:
            return
    elif ctx.invoked_subcommand is None:
        x = text2art("euphoria", font="larry3d")
        click.secho(x, fg="green")
        click.echo("Stake WAGMI and earn harmonious compounding interest (🤝,🤝)")


@euphoria.command()
def dashboard():
    data = dashboard_service.getData()
    for k, v in data.items():
        click.secho(f"{k}", fg="blue", nl=False)
        click.echo(":", nl=False)
        click.secho(f" {v}", fg="green")


@euphoria.command()
def stake():
    data = stake_service.getData(user_hmny_addr)
    for k, v in data.items():
        click.secho(f"{k}", fg="blue", nl=False)
        click.echo(":", nl=False)
        click.secho(f" {v}", fg="green")


if __name__ == "__main__":
    euphoria()
