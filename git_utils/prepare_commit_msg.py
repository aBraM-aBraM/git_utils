import os
import sys
import toml
import common
import actions

from common import Commit

STDIN_FILENO = 1


def read_config():
    with open(common.CONFIG_PATH) as config_file_obj:
        prepare_commit_msg_config = toml.load(config_file_obj).get("prepare-commit-msg")
        if prepare_commit_msg_config:
            return dict((k.replace('-', '_'), v) for k, v in prepare_commit_msg_config.items())
    return None


ACTIONS = {"force_present": actions.force_present,
           "directory_prefix": actions.directory_prefix,
           "force_title": actions.force_title,
           "no_cr": actions.no_cr}


def main():
    msg_path, cmdline = sys.argv[1:]
    with open(msg_path) as msg_file_obj:
        msg = msg_file_obj.read()
    cmdline = cmdline.split()[1:]
    sys.stdin.close()
    sys.stdin = os.fdopen(STDIN_FILENO)

    config = read_config()

    if config and "-m" in cmdline:
        with open(msg_path, 'r+') as msg_file_obj:
            commit = Commit(msg, config)
            for action in ACTIONS:
                if action in config.keys():
                    commit = ACTIONS[action](commit)
            common.set_msg(commit.msg, msg_file_obj)
    else:
        common.print_error(f"{os.path.basename(__file__)} executes without a configuration")


if __name__ == '__main__':
    main()
