import configparser

configuration_file = 'config.txt'

# Read configuration file
config = configparser.ConfigParser()
config.read(configuration_file)


def get_url(category: str, flag: str) -> str:
    base_url = config['config']['api_url']

    formatted_category = get_category(category)
    query = get_query(flag)

    full_url = base_url + formatted_category + query
    return full_url


def get_category(category: str) -> str:
    categories = config['config']['categories']

    capitalized_category = str(category).capitalize()

    if capitalized_category in categories:
        return capitalized_category
    else:
        raise Exception('Invalid category')


def get_query(flag: str) -> str:
    base_query = "?blacklistFlags="

    flags = config['config']['flags']

    if flag in flags:
        # When flag is 'none', api doesn't need query params
        if flag == 'none':
            return ''
        full_query = base_query + flag
    else:
        raise Exception('Invalid flag')

    return full_query
