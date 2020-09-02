# `gds-pre-commit`

`gds-pre-commit` is a tool for preventing secrets being committed to git. It is based on Yelp’s detect-secrets (https://github.com/Yelp/detect-secrets) project.

If the tool detects that a git commit is being made in an alphagov repository, it scans the contents of the commit to see if contains anything that looks sensitive, like an SSH key, an AWS key or an API token. If it detects something that looks like a “secret”, it prevents the commit from going through; otherwise everything works as normal.

## Quick Install

First ensure you have Python 3 and pip installed.  On mac, run
`brew install python`; on ubuntu, run `apt-get install python3-pip`.

If you are happy with the default location, run the following two commands to install:

The script installs the hook config to your global `git config` and reports
your registration to us.

```shell
git clone https://github.com/alphagov/gds-pre-commit.git ~/.gds-pre-commit/
```

```shell
~/.gds-pre-commit/install.py
```

Once you've run the above commands the pre-commit framework will be installed with the detect-secrets plugin added to its config globally for git.

## Pre-requisites in detail

### Hook
 - Python 2 or 3 with pip

### Registration script
 - Python 3

The pre-commit framework is installed by pip, the Python package manager. To install it on your machine either brew install it or get it from your distributions package manager (it might be called `python3-pip`, or `pip3`)

#### Why does the script register your installation?

Initially the goal of registration is to enable us to get an idea 
of coverage. Registration gives us coverage of the alphagov 
membership. We can then get coverage of (active) alphagov 
repositories by looking for the baseline file. 

Neither of those on their own give us a good idea of how many 
commits are being made against alphagov without protection so 
hopefully in time we can actually report by commit with another 
hook.

## Ignoring secrets
1. In-line `# pragma: allowlist secret` In any language's comment format.
1. Add to your repository's `.pre-commit-config.yaml`, eg:
```
$ cat .pre-commit-config.yaml
-   repo: git@github.com:Yelp/detect-secrets
    rev: v0.14.3
    hooks:
    -   id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: .*/tests/.*
```

## Privacy

By installing this tool, you will send the GDS Cyber team:

* your name as configured in your global git configuration
* your email address as configured in your global git configuration
* your IP address
* the version of curl installed on your machine

## Further Reading

 - [Usage](usage.md)
 - [Useful Hooks and plugins](pre-commit-plugins.md)
