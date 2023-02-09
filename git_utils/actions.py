import os.path
from typing import TextIO

from common import unwrap, get_status, set_msg, yes_no


def force_present(msg: str, msg_file_obj: TextIO) -> str:
    unwrap(msg.split()[0][-2:] != "ed", f"Use present tense in commits! (\"{msg.split()[0]}\" is in past tense)")
    return msg


def directory_prefix(msg: str, msg_file_obj: TextIO) -> str:
    staged, untracked = get_status()

    staged = [os.path.split(path)[0] for path in staged]

    if len(set(staged)) <= 1:
        # same directory for all changed items
        msg = f"{next(iter(staged))}: {msg}"
        set_msg(msg, msg_file_obj)
    else:
        staged_list = list(staged)
        most_common = max(set(staged_list), key=staged_list.count)
        if yes_no(f"Would you like to use {most_common.strip()} as a prefix [Y/n]?"):
            msg = f"{next(iter(staged))}: {msg}"
            set_msg(msg, msg_file_obj)
    return msg


def force_title(msg: str, msg_file_obj: TextIO) -> str:
    unwrap(":" in msg, "Commits must have a title! Syntax: <commit title>: <commit msg>")
    return msg
