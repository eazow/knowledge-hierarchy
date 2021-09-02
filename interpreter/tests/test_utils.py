from inflection import underscore

from utils import camel_to_snake


def test_camel_to_snake():
    camel_to_snake("HelloWorld") == "hello_world"
    underscore("HelloWorld") == "hello_world"
