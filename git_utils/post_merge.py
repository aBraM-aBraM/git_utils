import os
import sys
import toml
import common
import actions

from common import Commit

STDIN_FILENO = 1


def read_config():
    with open(common.CONFIG_PATH) as config_file_obj:
        return dict((k.replace('-', '_'), v) for k, v in toml.load(config_file_obj).items())


ACTIONS = {"force_present": actions.force_present,
           "directory_prefix": actions.directory_prefix,
           "force_title": actions.force_title,
           "no_cr": actions.no_cr}


def main():
    is_squash, cmdline = sys.argv[1:]
    cmdline = cmdline.split()[1:]
    sys.stdin.close()
    sys.stdin = os.fdopen(STDIN_FILENO)

    config = read_config()


if __name__ == '__main__':
    main()
