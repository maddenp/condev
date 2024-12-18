"""
A Python/C hello-world demo.
"""

import ctypes
import json
from importlib.resources import read_text


def hello() -> str:
    """
    The 1st word in a programming trope.
    """
    return "hello"


def main() -> None:
    """
    Main entry point.
    """
    sep = json.loads(read_text("hello.resources", "conf.json"))["separator"]
    print(f"{sep} ".join([hello(), world()]))


def world() -> str:
    """
    The 2nd word in a programming trope.
    """
    cworld = ctypes.CDLL("libworld.so")
    cworld.world.restype = ctypes.c_char_p
    return str(cworld.world().decode())
