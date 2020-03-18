## Pre-requisites

### Hook
 - Python 2 or 3 with pip

### Registration script
 - Python 3

The pre-commit framework is installed by pip, the Python package manager. To install it on your machine either brew install it or get it from your distributions package manager (it might be called `python3-pip`, or `pip3`)

Currently, our registration script's GitHub Oauth flow only works with OTP systems (such as Google Authenticator, Authy, Yubikeys that type in a code). If you use a U2F system, please skip registration.

## Quick Install

If you are happy with the default location, run the following two commands to install:

The script installs the hook config to your global `git config` and reports 
your registration to us. During the registration step you'll be asked for your 
GitHub credentials to create an OAuth token with `read:user` and `read:org` 
scopes - this allows us to verify your identity and your GitHub org membership.

```shell
git clone https://github.com/alphagov/gds-pre-commit.git ~/.gds-pre-commit/
```

```shell
~/.gds-pre-commit/install.py
```

Once you've run the above commands the pre-commit framework will be installed with the detect-secrets plugin added to it's config globally for git.


## Usage

The first time you run `git commit` **in a repository** will throw a warning to tell you that you need to create a secrets baseline, as shown below:

```shell
Unable to open baseline file: REPO_ROOT/.secrets.baseline
Please create it via
   detect-secrets scan > $HOME/<your-git-repo>/.secrets.baseline
```

Once you've added your secrets baseline, the first time you run `git commit` **on your machine**, will install the hooks that have been added to your global config.

It will look something like this:

```shell
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for git@github.com:Yelp/detect-secrets.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
Detect Private Key.......................................................Passed
Detect secrets...........................................................Passed
```



# gds-pre-commit
This repository is here to assist GDS users in setting up pre-commit hooks that can improve the quality and security of projects hosted on GitHub.

## Secrets
One of the main motivations for using pre-commit hooks is to prevent secrets being pushed to GitHub repositories. When we say secrets we mean things like private keys, API tokens, SSH keys, AWS keys or Slack keys. All of these 'secrets' are used to authenticate or authorise users to services we use or own and would be beneficial for an attacker to steal.

The detect-secrets tool was tested against AWS keys, a private SSH key and a random hash with the tool successfully catching them all, however pre-commit hooks should not be used as a catch-all solution and users should ensure they are following Secure Software Development Lifecycles.

## pre-commit framework
One of the easiest ways to get started with pre-commit hooks is by using the [pre-commit framework](https://pre-commit.com/).

Read on for step-by-step instruction:

### Installing pre-commit manually
#### Please note that the quick install section at the top will run these commands globally

To get started you can either run:

`$ brew install pre-commit`

or

`$ pip3 install pre-commit`

## detect-secrets
The detect-secrets pre-commit hook requires some initialisation before it is run with the framework.

First you will need to install detect-secrets system-wide:

`$ pip3 install detect-secrets`

Then run the following commands in your local repository:

`$ detect-secrets scan > .secrets.baseline`

`$ detect-secrets audit .secrets.baseline`

This will create a baseline for your repository, initialising [plugins](https://github.com/Yelp/detect-secrets/tree/master/detect_secrets/plugins) used and then scan all of the files in your repository. It will ask you about potential secrets it finds and if they are to real secrets or false positives.

The newly created `.secrets.baseline` file should be committed to Github.


Once that's completed, you're all done! If you want to add any other hooks, take a look at the [extensive list](https://pre-commit.com/hooks.html). There are various handy linters and formatters for Go, Ruby, Python and Terraform.

## Supported editors
This pre-commit hook has been tested and is working with the following editors:

* Atom
* VScode
* IntelliJ
* Pycharm
* Emacs
* Vim (with Fugitive.vim)

