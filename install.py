#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import distutils.spawn
import os
import sys

from register import register
from runner import run

try:
    input = raw_input  # type: ignore
except NameError:
    pass

print("⏳ Installing pip dependencies.")
if distutils.spawn.find_executable("pip3"):
    run("pip3 install -q pre-commit detect-secrets")
elif distutils.spawn.find_executable("pip"):
    run("pip install -q pre-commit detect-secrets")
else:
    print(
        "Can't find `pip` or `pip3` on your PATH, please install pip.", file=sys.stderr
    )
    sys.exit(1)


def hookpath():
    p = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(p, "global_install", "hooks")


run("git config --global core.hooksPath " + hookpath())

print()
print("✔️  Detect-secrets hook installed")
print()

print("⏳ Registering your installation with GDS Cybersecurity...")

register()  # Add "test" argument to switch to non-production mode

print()
print("✔️  Installation done. Questions to #cyber-security-team. Thanks!")
