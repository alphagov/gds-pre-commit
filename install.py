#!/usr/bin/env python3
from __future__ import print_function

import distutils.spawn
import os
import subprocess
import sys

if sys.version_info < (3, 7):  # https://bugs.python.org/issue25942

    def _subprocess_call(cmd):  # this is the python 2.7 implementation
        return subprocess.Popen(cmd).wait()


else:
    _subprocess_call = subprocess.call


if distutils.spawn.find_executable("pip3"):
    _subprocess_call(["pip3", "install", "-q", "pre-commit", "detect-secrets"])
elif distutils.spawn.find_executable("pip"):
    _subprocess_call(["pip", "install", "-q", "pre-commit", "detect-secrets"])
else:
    print("Can't find `pip` or `pip3` on your PATH, please install pip.")

def hookpath():
    s = os.path.realpath(__file__)
    f = os.path.basename(s)
    p = s[:-(len(f))-1]
    p = os.path.join(p, "global_install/hooks")
    return p

_subprocess_call(
    [
        "git",
        "config",
        "--global",
        "core.hooksPath",
        hookpath(),
    ]
)
print()
print("✔️ Detect-secrets hook installed")
