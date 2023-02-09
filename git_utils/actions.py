import sys

def unwrap(statement: bool, error_msg: str):
    if not statement:
        panic(error_msg)


def panic(error_msg: str):
    print(error_msg, file=sys.stderr)
    exit(1)

def force_present(msg: str):
    unwrap(msg.split()[0][-2:] != "ed", f"Use present tense in commits! (\"{msg.split()[0]}\" is in past tense)")


def directory_prefix(msg: str):
    pass


def force_title(msg: str):
    unwrap(":" in msg, "Commits must have a title! Syntax: <commit title>: <commit msg>")
