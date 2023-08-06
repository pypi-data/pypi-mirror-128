import json


def is_two_part(content: str) -> bool:
    return content['type'] == "twopart"


def format_one_part_joke(raw_joke: json) -> str:
    return raw_joke["joke"]


def format_two_part_joke(raw_joke: json) -> str:
    setup = raw_joke["setup"]
    delivery = raw_joke["delivery"]
    fill = " "

    full_joke = f'''{setup}{fill}{delivery}'''

    return full_joke


def format_joke(http_response_content: json) -> str:
    parsed_content = json.loads(http_response_content.decode('utf-8'))

    joke: str

    if is_two_part(parsed_content):
        joke = format_two_part_joke(parsed_content)
    else:
        joke = format_one_part_joke(parsed_content)

    return joke
