#!/usr/bin/env python3
from __future__ import print_function

import distutils.spawn
import os

from runner import _subprocess_call, call
from register import register

print("⏳ Installing pip dependencies.")
if distutils.spawn.find_executable("pip3"):
    call("pip3 install -q pre-commit detect-secrets")
elif distutils.spawn.find_executable("pip"):
    call("pip install -q pre-commit detect-secrets")
else:
    print("Can't find `pip` or `pip3` on your PATH, please install pip.")


def hookpath():
    p = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(p, "global_install", "hooks")


call("git config --global core.hooksPath " + hookpath())

print()
print("✔️ Detect-secrets hook installed")

_subprocess_call([
    "bash",
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "register.sh"),
    "-t"  # Remove this for production version
])
# register("test")  # Remove test mode argument for production

print()
print("✔️ User registered")
