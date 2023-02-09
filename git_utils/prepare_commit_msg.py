import os
import sys
import toml
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent
CONFIG_PATH = SCRIPT_PATH / "git_utils.toml"
STDIN_FILENO = 1


def unwrap(statement: bool, error_msg: str):
    if not statement:
        panic(error_msg)


def panic(error_msg: str):
    print(error_msg, file=sys.stderr)
    exit(1)


def read_config():
    with open(CONFIG_PATH) as config_file_obj:
        return dict((k.replace('-', '_'), v) for k, v in toml.load(config_file_obj).items())


def force_present(msg: str):
    unwrap(msg.split()[0][-2:] != "ed", f"Use present tense in commits! (\"{msg.split()[0]}\" is in past tense)")


def directory_prefix(msg: str):
    pass


def force_title(msg: str):
    unwrap(":" in msg, "Commits must have a title! Syntax: <commit title>: <commit msg>")


def get_status():
    pass


ACTIONS = {"directory_prefix": directory_prefix,
           "force_present": force_present,
           "force_title": force_title}


def main():
    msg_path, cmdline = sys.argv[1:]
    with open(msg_path) as msg_file_obj:
        msg = msg_file_obj.read()
    cmdline = cmdline.split()[1:]
    sys.stdin.close()
    sys.stdin = os.fdopen(STDIN_FILENO)

    config = read_config()

    if "-m" in cmdline:
        for action in ACTIONS:
            if config[action]:
                ACTIONS[action](msg)


if __name__ == '__main__':
    main()
