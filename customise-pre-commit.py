#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from register import register
from runner import run

try:
    input = raw_input  # type: ignore
except NameError:
    pass


hookspath = run("git config --global core.hooksPath")
env_addition = """import os; os.environ["DETECT_SECRETS_SECURITY_TEAM"] = "in #cyber-security-help"
"""

input()

print()
print("✔️ GDS Detect-secrets customisation done.")
print()

print("⏳ Registering your installation with GDS Cybersecurity...")

register()  # Add "test" argument to switch to non-production mode

print()
print("✔️  Installation done. Questions to #cyber-security-help. Thanks!")
