#!/usr/bin/env python
from __future__ import print_function

import distutils.spawn
import os

from register import register
from runner import run

print("⏳ Installing pip dependencies.")
if distutils.spawn.find_executable("pip3"):
    run("pip3 install -q pre-commit detect-secrets")
elif distutils.spawn.find_executable("pip"):
    run("pip install -q pre-commit detect-secrets")
else:
    print("Can't find `pip` or `pip3` on your PATH, please install pip.")


def hookpath():
    p = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(p, "global_install", "hooks")


run("git config --global core.hooksPath " + hookpath())

print()
print("✔️ Detect-secrets hook installed")

register("test")  # Remove test mode argument for production

print()
print("✔️ User registered")
