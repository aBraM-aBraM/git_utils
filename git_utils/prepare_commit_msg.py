import os
import sys
import toml
from pathlib import Path
from subprocess import Popen, PIPE

import actions

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SCRIPT_DIR / "git_utils.toml"
STDIN_FILENO = 1


def read_config():
    with open(CONFIG_PATH) as config_file_obj:
        return dict((k.replace('-', '_'), v) for k, v in toml.load(config_file_obj).items())


def get_status():
    stdout, _ = Popen("git status -s", shell=True, cwd=PROJECT_DIR, stdout=PIPE).communicate()
    stdout = set(stdout.decode().splitlines())

    staged = set(line[1:] for line in stdout if "??" not in line)
    untracked = set(line[1:] for line in stdout.difference(staged))

    return staged, untracked


ACTIONS = {"directory_prefix": actions.directory_prefix,
           "force_present": actions.force_present,
           "force_title": actions.force_title}


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
                # ACTIONS[action](msg)
                get_status()


if __name__ == '__main__':
    main()
