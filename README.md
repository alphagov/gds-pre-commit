## Pre-requisites

### Hook
 - Python 2 or 3 with pip

### Registration script
 - Python 3

The pre-commit framework is installed by pip, the Python package manager. To install it on your machine either brew install it or get it from your distributions package manager (it might be called `python3-pip`, or `pip3`)

Currently, our registration script's GitHub Oauth flow only works with OTP systems (such as Google Authenticator, Authy, Yubikeys that type in a code). If you use a U2F system, please skip registration.

#### Why are we asking people to register?

Initially the goal of registration is to enable us to get an idea 
of coverage. Registration gives us coverage of the alphagov 
membership. We can then get coverage of (active) alphagov 
repositories by looking for the baseline file. 

Neither of those on their own give us a good idea of how many 
commits are being made against alphagov without protection so 
hopefully in time we can actually report by commit with another 
hook. 

The 2nd reason for registration is that it sets up your git config
to send those per commit stats to us if we choose to go down that 
route later.   

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

Once you've run the above commands the pre-commit framework will be installed with the detect-secrets plugin added to its config globally for git.

## Further Reading

 - [Usage](usage.md)
 - [Useful Hooks and plugins](pre-commit-plugins.md)
