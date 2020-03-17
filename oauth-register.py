""" Register user with pre-commit usage reporting """
from __future__ import print_function
from http.server import HTTPServer, BaseHTTPRequestHandler
from runner import run

import json
import webbrowser


try:
    input = raw_input  # type: ignore
except NameError:
    pass


def inputc(text):
    try:
        return input(text)
    except KeyboardInterrupt:
        print("\nRegistration cancelled.")
        exit()


def html_response(text):
    return str.encode(
        f"""
    <div style="font:2em Helvetica;width: 100%;text-align: center;margin-top: 1em;">
    <a href="https://github.com/alphagov/gds-pre-commit">gds-pre-commit</a><br>
    {text}
    </div>
    """
    )


def get_query_string(raw, param):
    res = ""
    if "?" in raw:
        qs_raw = raw.split("?", 1)[1]
        for qs in qs_raw.split("&"):
            if f"{param}=" in qs:
                res = qs.split("=", 1)[1]
                break
    return res


def send_to_alert_controller(code, mode="dev"):
    post_dict = {
        "code": code,
        "client_id": "4b49a3d16a97bad96672",
        "client_secret": "XXXXX",  # insert secret here somehow...
    }
    post_data = json.dumps(post_dict)

    auth_resp = run(
        "curl -s "
        '"'
        "https://github.com/login/oauth/access_token?"
        f"code={code}&"
        "client_id=4b49a3d16a97bad96672&"
        "client_secret=053a34707159f1c353423abbafc270e547f19bbc"
        '"'
    )

    token = get_query_string(auth_resp, "access_token")

    if mode == "prod":
        endpoint = "alert-controller.gds-cyber-security.digital"
    else:
        endpoint = "alert-controller.staging.gds-cyber-security.digital"

    print("Submitting registration request...")
    registration_json = run(
        "curl -s"
        ' -H "Authorization: github ' + token + '"'
        ' -H "User-Agent: GitHub/Hook"'
        ' -d \'{"action":"register"}\''
        " https://" + endpoint + "?alert_name=register"
    )
    print("Done!")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_request(self, code="", size=""):
        return

    def do_GET(self):
        code = get_query_string(self.path, "code")

        self.send_response(200)
        self.end_headers()

        if code == "":
            self.wfile.write(
                html_response("Something went wrong, close this window and try again.")
            )
            print(
                "That didn't worth, if you'd like to try registering again, run: python oauth-register.py"
            )
        else:
            # registered to the OAuth app at this point
            # could run send_to_alert_controller(code) if needed but has
            # sensistive app details
            self.wfile.write(
                html_response(
                    "Thanks! You can close this window and return to the terminal now."
                )
            )
            print("Thanks, you successfully registered.")


def register():
    resp = inputc("Register use of gds-pre-commit with the Cyber Security Team? (Y/n) ")
    if resp.lower().startswith("y") or resp == "":
        webbrowser.open(
            "https://github.com/login/oauth/authorize?"
            "client_id=4b49a3d16a97bad96672&"
            "scope=read:user read:org"
        )
        try:
            httpd = HTTPServer(("localhost", 9817), SimpleHTTPRequestHandler)
            httpd.handle_request()
        except KeyboardInterrupt:
            print("\nRegistration cancelled.")
            exit()


if __name__ == "__main__":
    register()
