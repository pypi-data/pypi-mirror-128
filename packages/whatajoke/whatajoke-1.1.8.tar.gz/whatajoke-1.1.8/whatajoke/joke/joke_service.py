import requests
import whatajoke.joke.url_helper as url_helper
import whatajoke.joke.joke_formatter as joke_formatter


def get_joke(category: str, flag: str) -> str:
    """

    :rtype: object
    """
    # Get formatted url
    url = url_helper.get_url(category, flag)

    # Send request
    response = requests.get(url)
    # print(response.content)

    if response.status_code == 200:
        # Format joke
        joke = joke_formatter.format_joke(response.content)
    else:
        raise Exception("Ups! Something went wrong on joke request.")

    print(joke)
    return joke
