from utils import camel_to_snake


def test_camel_to_snake():
    camel_to_snake("HelloWorld") == "hello_world"