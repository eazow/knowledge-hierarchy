import re


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    print(name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
