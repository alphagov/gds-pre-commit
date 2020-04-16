""" Register user with pre-commit usage reporting """
from __future__ import print_function

import json
import urllib.parse

from runner import run


def register(mode="prod"):
    """
    Perform pre-commit registration

    send a registration message to a cybersecurty spreadsheet
    """
    username = run("git config --global user.name")
    email = run("git config --global user.email")

    if mode == "prod":
        url = (
            "https://script.google.com/macros/s/AKfycbyJJ7jtvIHhn3MPTwmvDgm2kQ3Be5KJ1sXqJY_2L_AvaISQlss/exec?name=%s&email=%s"
            % (urllib.parse.quote(username), email)
        )
    else:
        url = (
            "https://script.google.com/macros/s/AKfycbyJJ7jtvIHhn3MPTwmvDgm2kQ3Be5KJ1sXqJY_2L_AvaISQlss/exec?name=%s&email=%s"
            % (urllib.parse.quote(username), email)
        )

    output = run("curl -Ls " + url)

    if json.loads(output).get("result") == "success":
        print("You have been registered successfully.")
    else:
        print("Registration failed. Please report this to #cyber-security-help.")


if __name__ == "__main__":
    register()
