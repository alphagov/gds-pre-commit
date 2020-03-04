import subprocess
import sys

if sys.version_info < (3, 7):  # https://bugs.python.org/issue25942

    def _subprocess_call(cmd):  # this is the python 2.7 implementation
        return subprocess.Popen(cmd).wait()


else:
    _subprocess_call = subprocess.call


def call(cmd):
    return _subprocess_call(cmd.split())
