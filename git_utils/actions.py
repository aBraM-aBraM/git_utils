import os.path

from common import unwrap, get_status, set_msg, yes_no, Commit


def force_present(commit: Commit) -> str:
    unwrap(commit.msg.split()[0][-2:] != "ed",
           f"Use present tense in commits! (\"{commit.msg.split()[0]}\" is in past tense)")
    return commit.msg


def directory_prefix(commit: Commit) -> str:
    staged, untracked = get_status()

    staged = [os.path.split(path)[0] for path in staged]

    if len(set(staged)) <= 1:
        # same directory for all changed items
        commit.msg = f"{next(iter(staged))}: {commit.msg}"
        set_msg(commit.msg, commit.msg_file_obj)
    else:
        staged_list = list(staged)
        most_common = max(set(staged_list), key=staged_list.count)
        if commit.config["auto_common_directory"] or \
                yes_no(f"Would you like to use {most_common.strip()} as a prefix [Y/n]?"):
            commit.msg = f"{next(iter(staged))}: {commit.msg}"
            set_msg(commit.msg, commit.msg_file_obj)
    return commit.msg


def force_title(commit: Commit) -> str:
    unwrap(":" in commit.msg, "Commits must have a title! Syntax: <commit title>:<commit msg>")
    return commit.msg


def no_cr(commit: Commit) -> str:
    unwrap("cr" not in commit.msg.lower(), "Please amend CR related commits!")
    return commit.msg
