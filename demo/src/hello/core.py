"""
A Python/C hello-world demo
"""


def hello() -> str:
    """The first word in a programming trope"""
    return "hello"


def main() -> None:
    """Main entry point"""
    print(", ".join([hello()]))
