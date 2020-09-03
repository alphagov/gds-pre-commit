#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from register import register
from runner import run

try:
    input = raw_input  # type: ignore
except NameError:
    pass

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
print("✔️  Installation done. Questions to #cyber-security-help. Thanks!")
