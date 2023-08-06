import click
from whatajoke.commands import send, login


@click.group(help="CLI tool to send jokes to your friends by Whatsapp")
def cli():
    pass


cli.add_command(send.send)
cli.add_command(login.login)


def main():
    cli()
