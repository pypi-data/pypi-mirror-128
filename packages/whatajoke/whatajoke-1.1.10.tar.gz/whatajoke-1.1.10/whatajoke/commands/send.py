import click
import whatajoke.service


@click.command()
@click.option("--group", "-g",
              required=True,
              prompt="Name of the group or person to send the joke to",
              help="Name of the group or person to send the joke to!")
@click.option("--category", "-c",
              type=click.Choice(["any", "programming", "misc", "dark", "pun", "spooky", "christmas"],
                                case_sensitive=False),
              default="any",
              help="Category of the joke. Default value is \"any\".")
@click.option("--flag", "-f",
              type=click.Choice(["none", "nsfw", "religious", "political", "racist", "sexist", "explicit"],
                                case_sensitive=False),
              default="none",
              help="Flag to add to category. Default value is \"none\".")
@click.option("--headed", "-h",
              is_flag=True,
              help="Runs in headed mode.")
def send(group, category, flag, headed):
    try:
        # Parse choice to String
        category = str(category)
        flag = str(flag)
        group = str(group)

        whatajoke.service.send_joke(group, category, flag, headed)

    except Exception as e:
        print(e)

    finally:
        print("See you soon!")
