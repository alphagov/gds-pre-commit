""" Register user with pre-commit usage reporting """
from __future__ import print_function

import json
import sys

from runner import call

# Get raw_input if exists and fallback on input
try:
    safe_input = raw_input
except NameError:
    safe_input = input


def register(mode="prod"):
    """
    Perform pre-commit registration

    Perform an OAuth grant with GitHub and
    send a registration message to cyber
    """
    if mode == "prod":
        endpoint = "alert-controller.gds-cyber-security.digital"
    else:
        endpoint = "alert-controller.staging.gds-cyber-security.digital"

    username = call("git config --global gds.github-username")
    if not username:
        # Prompt user for github username
        username = safe_input("Enter your github username:")

    # OAuth for registration credentials
    token = call("git config --global gds.github-registration-token")
    if not token:
        print("Performing GitHub OAuth")
        print(
            "This creates a personal access token with read:user and read:org scopes. "
        )
        # Prompt user for 2FA
        otp = safe_input("Please enter your GitHub 2FA code:")
        print(
            "Requesting authorization from GitHub - "
            "You will be prompted for your GitHub password."
        )
        timestamp = call("date")
        post_dict = {
            "scopes": ["read:user", "read:org"],
            "note": "GDS GitHub Usage Reporting " + timestamp,
        }
        post = json.dumps(post_dict)

        authorization_json = call(
            "curl -s"
            ' -H "X-GitHub-OTP: ' + otp + '"'
            " -u " + username + " "
            ' -d "' + post + '"'
            " https://api.github.com/authorizations"
        )
        try:
            authorization = json.loads(authorization_json)
            token = authorization["token"]
            call("git config --global gds.github-registration-token " + token)
        except json.JSONDecodeError:
            print("Failed to authenticate with GitHub.")
            print("Please check your credentials and try again.")
            sys.exit(1)

    # Register and get reporting credentials

    print("Submit registration request.")
    registration_json = call(
        "curl -s"
        ' -H "Authorization: github ' + token + '"'
        ' -H "User-Agent: GitHub/Hook"'
        ' -d \'{"action":"register"}\''
        " https://" + endpoint + "?alert_name=register"
    )

    try:
        registration = json.loads(registration_json)

        secret = registration["user_secret"]
        username = registration["username"]
        call("git config --global gds.github-reporting-token " + secret)
        call("git config --global gds.github-username " + username)
        config_user = call("git config --global gds.github-username")
        config_token = call("git config --global gds.github-reporting-token")
        if config_user and config_token:
            print("You have been registered successfully.")
        else:
            raise Exception
    except Exception:
        print("Registration failed. Please report to #cyber-security-help.")


if __name__ == "__main__":
    register("test")