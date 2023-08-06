import click
import re
from art import text2art

try:
    from helpers.web3Helper import w3
    from service import dashboard_service, stake_service
    from __version__ import __version__
    from helpers.config_helper import *
except ImportError:
    from .helpers.web3Helper import w3
    from .service import dashboard_service, stake_service
    from .__version__ import __version__
    from .helpers.config_helper import *

# user_hmny_addr = ""
hmny_addr_pattern = re.compile(r"^0x[a-fA-F0-9]{40}$")
CONTEXT_SETTINGS = dict(obj={})


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option("--address", "-a", help="Set the account address in '0x' format")
@click.option(
    "--remove-addr", "-ra", help="Remove the address from config.", is_flag=True
)
@click.option(
    "--view-addr", "-va", help="view the address stored in config", is_flag=True
)
@click.option("-v", "--version", help="Version of the app", is_flag=True)
def euphoria(ctx, address, remove_addr, view_addr, version):
    if is_config_present():
        addr = read_config()
        if addr:
            ctx.obj["user_hmny_addr"] = w3.toChecksumAddress(addr)
    else:
        make_config_file()

    if version:
        click.echo(__version__)
    elif address:
        res = hmny_addr_pattern.match(str(address))
        if res:
            if is_config_present():
                save_to_config(w3.toChecksumAddress(address))
                click.secho(f"✅ Address saved => {address}", fg="green")
            else:
                make_config_file()
                save_to_config(w3.toChecksumAddress(address))
        else:
            click.secho(f"Address {address} is not in correct format", fg="red")
            return
    elif remove_addr:
        make_config_file()
        click.secho("❌ Address removed", fg="red")
    elif view_addr:
        x = read_config()
        click.secho(x, fg="blue")
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
@click.pass_context
def stake(ctx):
    user_hmny_addr = ctx.obj["user_hmny_addr"]
    data = stake_service.getData(user_hmny_addr)
    for k, v in data.items():
        click.secho(f"{k}", fg="blue", nl=False)
        click.echo(":", nl=False)
        click.secho(f" {v}", fg="green")


if __name__ == "__main__":
    euphoria()
