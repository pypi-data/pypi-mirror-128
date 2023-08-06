import click
import whatajoke.whatsapp.whatsapp_service as service


@click.command(help="Open Whatsapp to read the QR code")
def login():
    service.login()
