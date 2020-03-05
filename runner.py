import subprocess


def run(cmd):
    """ """
    try:
        return subprocess.check_output(cmd, shell=True).decode("UTF-8").strip()
    except subprocess.CalledProcessError:
        return None
