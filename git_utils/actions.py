import os.path

from common import unwrap, get_status, yes_no, Commit, most


def force_present(commit: Commit) -> Commit:
    unwrap(commit.msg.split()[0][-2:] != "ed",
           f"Use present tense in commits! (\"{commit.msg.split()[0]}\" is in past tense)")
    return commit


def directory_prefix(commit: Commit) -> Commit:
    staged, untracked = get_status()

    most_in_dir = most(staged, lambda staged_path: len([p for p in os.path.split(staged_path) if p != ""]) > 1)

    staged = [os.path.split(path)[0] for path in staged]

    if most_in_dir:
        if len(set(staged)) <= 1:
            # same directory for all changed items
            commit.msg = f"{next(iter(staged))}: {commit.msg}"
        else:
            staged_list = list(staged)
            most_common = max(set(staged_list), key=staged_list.count)
            if commit.config.get("auto_common_directory") or \
                    yes_no(f"Would you like to use {most_common.strip()} as a prefix [Y/n]?"):
                commit.msg = f"{next(iter(staged))}: {commit.msg}"
    else:
        if commit.config.get("top_level_title"):
            commit.msg = f'{commit.config["top_level_title"]}: {commit.msg}'
    return commit


def force_title(commit: Commit) -> Commit:
    unwrap(":" in commit.msg, "Commits must have a title! Syntax: <commit title>: <commit msg>")
    return commit


def no_cr(commit: Commit) -> Commit:
    unwrap("cr" not in commit.msg.lower().split(), "Please amend CR related commits!")
    return commit
