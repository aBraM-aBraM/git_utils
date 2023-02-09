from pathlib import Path
from subprocess import Popen, PIPE
from dataclasses import dataclass
import sys
from typing import TextIO

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SCRIPT_DIR / "git_utils.toml"


@dataclass
class Commit:
    msg: str
    msg_file_obj: TextIO
    config: dict


def unwrap(statement: bool, error_msg: str):
    if not statement:
        panic(error_msg)


def panic(error_msg: str):
    print(error_msg, file=sys.stderr)
    exit(1)


def get_status():
    stdout, _ = Popen("git status -s", shell=True, cwd=PROJECT_DIR, stdout=PIPE).communicate()
    stdout = set(stdout.decode().splitlines())

    staged = set(line[1:] for line in stdout if "??" not in line)
    untracked = set(line[1:] for line in stdout.difference(staged))

    return staged, untracked


def yes_no(msg: str):
    user_input = input(msg).lower()
    return user_input == "y" or user_input == ""


def set_msg(msg: str, msg_file_obj: TextIO):
    msg_file_obj.seek(0)
    msg_file_obj.write(msg)
