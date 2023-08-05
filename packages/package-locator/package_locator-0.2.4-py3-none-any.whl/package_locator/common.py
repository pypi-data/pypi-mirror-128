import collections
from giturlparse import parse
import re

CARGO = "Cargo"
COMPOSER = "Composer"
GO = "Go"
MAVEN = "Maven"
NPM = "npm"
NUGET = "NuGet"
PYPI = "pypi"
RUBYGEMS = "RubyGems"
ecosystems = [CARGO, COMPOSER, GO, MAVEN, NPM, NUGET, PYPI, RUBYGEMS]


class NotPackageRepository(Exception):
    pass


def flatten(dictionary, parent_key=False, separator="."):
    """
    Turn a nested dictionary into a flattened dictionary
    :param dictionary: The dictionary to flatten
    :param parent_key: The string to prepend to dictionary's keys
    :param separator: The string used to separate flattened keys
    :return: A flattened dictionary
    :credit: https://stackoverflow.com/a/6027615/1445015
    """

    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)


def search_for_github_repo(data):
    urls = set()

    data = flatten(data)
    for k in data.keys():
        if isinstance(data[k], str) and data[k].startswith("https://github.com") and " " not in data[k]:
            parsed_url = parse(data[k])
            if parsed_url.valid:
                urls.add(parsed_url.url2https)

    if not urls:
        url_pattern = r"(https?://[www.]?github.com[^\s|)|.]+)"
        for k in data.keys():
            if isinstance(data[k], str):
                candidates = re.findall(url_pattern, data[k])
                for c in candidates:
                    parsed_url = parse(c)
                    if parsed_url.valid:
                        urls.add("https://github.com/{}/{}".format(parsed_url.owner, parsed_url.repo))

    return urls
