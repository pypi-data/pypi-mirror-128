base_url = "https://v2.jokeapi.dev/joke/"


def get_url(category: str, flag: str) -> str:
    formatted_category = get_category(category)
    query = get_query(flag)

    full_url = base_url + formatted_category + query
    return full_url


def get_category(category: str) -> str:
    capitalized_category = str(category).capitalize()

    return capitalized_category


def get_query(flag: str) -> str:
    base_query = "?blacklistFlags="

    # When flag is 'none', api doesn't need query params
    if flag == 'none':
        return ''

    full_query = base_query + flag

    return full_query
