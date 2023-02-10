import os
import sys
import toml
import common
import shutil

STDIN_FILENO = 1


def read_config():
    with open(common.CONFIG_PATH) as config_file_obj:
        post_merge_config = toml.load(config_file_obj).get("post-merge")
        if post_merge_config:
            return dict((k.replace('-', '_'), v) for k, v in post_merge_config.items())
    return None


def main():
    is_squash, cmdline = sys.argv[1:]
    cmdline = cmdline.split()[1:]
    sys.stdin.close()
    sys.stdin = os.fdopen(STDIN_FILENO)

    config = read_config()

    if config:
        copies = config.get("copies")
        for copy_action in copies:
            src, dst = copy_action
            src, dst = common.PROJECT_DIR / src, common.PROJECT_DIR / dst

            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy(common.PROJECT_DIR / src, common.PROJECT_DIR / dst)
    else:
        common.print_error(f"{os.path.basename(__file__)} executes without a configuration")


if __name__ == '__main__':
    main()
