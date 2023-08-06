from whatajoke.joke.joke_service import get_joke
from whatajoke.whatsapp.whatsapp_service import send_message


def send_joke(group: str, category: str, flag: str, headed: bool):
    # Get joke from joke service
    joke = get_joke(category, flag)

    # Send joke to Whatsapp Service
    send_message(group, joke, headed)
