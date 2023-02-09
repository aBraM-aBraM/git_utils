# Git Utils

---
Are you pedantic? Do you love and appreciate the order in git log?
If so this is the repository for you!

This is a collection of easily configurable git hooks.

## Features

* force-present - no more past-tense commit messages 
* force-title - enforce commit messages syntax -> title: message
* directory-prefix - if all commits are in the same directory use it as title, pop a yesno dialog 
if not all are in the same directory to allow the user to choose (also allow automatic yes)
* no-cr - no more "cr" in commit messages


## Setup / Install

```shell
git clone https://github.com/aBraM-aBraM/git_utils git_utils

cp git_utils/git_utils your/project/path
cd your/project/path

pip install -r ./git_utils/requirements.txt

chmod +x ./git_utils/setup_env.sh
./setup_env.sh 
```

Configure [git_utils.toml](./git_utils/git_utils.toml) based on your
needs and morals.
