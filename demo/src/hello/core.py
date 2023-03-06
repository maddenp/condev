"""
A Python/C hello-world demo
"""

import ctypes


def hello() -> str:
    """The 1st word in a programming trope"""
    return "hello"


def main() -> None:
    """Main entry point"""
    print(", ".join([hello(), world()]))


def world() -> str:
    """The 2nd word in a programming trope"""
    cworld = ctypes.CDLL("libworld.so")
    cworld.world.restype = ctypes.c_char_p
    return cworld.world().decode()
