import os
import subprocess
import hashlib
import json
from base64 import b64encode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import paramiko
import getpass
import pexpect
import git
import fire


def repeat_to_length(one_time, length):
    return (one_time * (int(length / len(one_time)) + 1))[:length]


def divider():
    print(repeat_to_length("-", 40))


def private_key_sign(message, private_key):
    signed_data = private_key.key.sign(
        message.encode("utf-8"), padding=padding.PKCS1v15(), algorithm=hashes.SHA256()
    )
    b64_bytes = b64encode(signed_data)
    b64_data = b64_bytes.decode("utf-8")
    return b64_data


def get_ssh_key(host="github.com"):
    home = os.environ.get("HOME")

    identity_file = f"{home}/.ssh/id_rsa"

    result = subprocess.run(["cat", f"{home}/.ssh/config"], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    lines = output.split("\n")
    for linenumber, line in enumerate(lines):
        if host in line:
            hostline = linenumber + 1
            line = lines[hostline]
            while "Host" not in line:
                if "IdentityFile" in line:
                    terms = line.split()
                    identity_file = terms.pop()
                hostline = hostline + 1
                line = lines[hostline]

    identity_file = identity_file.replace("~", home)
    return identity_file


def load_private_key(key_file, ssh_password=None):
    private_key = paramiko.RSAKey.from_private_key_file(key_file, ssh_password.encode())
    return private_key


def read_file(file_path, flags="r"):
    file_handle = open(file_path, flags)
    contents = file_handle.read()
    file_handle.close()
    return contents


def write_file(file_path, content, flags="w"):
    file_handle = open(file_path, flags)
    file_handle.write(content)
    file_handle.close()


def calc_md5(source_string):
    """Implement hashlib to calculate md5 from a given string"""
    undigested = source_string.encode("utf-8")
    hashed = hashlib.md5()
    hashed.update(undigested)
    digest = hashed.hexdigest()
    return digest


def get_username(private_key, ssh_password):
    # result = subprocess.run(["ssh", "-T", "git@gihub.com"], stdout=subprocess.PIPE)
    cmd = "ssh -T git@github.com"
    run = pexpect.spawn(cmd)
    if ssh_password:
        run.expect("Enter passphrase for key")
        run.sendline(ssh_password)
    run.expect("Hi [a-zA-Z0-9-_]+!")
    decoded_username = run.after.decode()
    username = decoded_username.split()[1][:-1]
    run.expect(pexpect.EOF)
    run.close()
    return username


class Hook:
    @classmethod
    def setup(cls):
        home = os.environ.get("HOME")
        if "GDS_GH_USERNAME" in os.environ:
            username = os.environ.get("GDS_GH_USERNAME")

            signed_file_path = os.environ.get("GDS_GH_PC_SIGN")
            verify_file_path = os.environ.get("GDS_GH_PC_RAW")
            with open(signed_file_path, "r") as signed_file:
                signed_data = signed_file.read().encode('utf-8').hex()
            with open(verify_file_path, "r") as verify_file:
                verify_data = verify_file.read().encode('utf-8').hex()

            git_config = git.GitConfigParser(
                f"{home}/.gitconfig",
                read_only=False,
                merge_includes=False
            )
            git_config.set_value("gds", "signed-data", f"{signed_data}").release()
            git_config.set_value("gds", "verify-data", f"{verify_data}").release()
            git_config.set_value("gds", "github-user", username).release()

            print("Your config has been installed")
        else:
            print("Please run source generate_signed_message.sh first to generate your config")

    @classmethod
    def notify(cls):
        home = os.environ.get("HOME")
        endpoint = os.environ.get("ENDPOINT")

        git_config = git.GitConfigParser(
            f"{home}/.gitconfig",
            read_only=True,
            merge_includes=False
        )

        post_data = {"commit": {"number": 12524, "type": "issue", "action": "show"}}
        sign = git_config.get_value("gds", "signed-data")
        post_data["verify"] = git_config.get_value("gds", "verify-data")
        post_data["username"] = git_config.get_value("gds", "github-user")
        post_data["auth_type"] = "ssh_signed"
        headers = {
            "Authorization": f"Signed {sign}",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "GitHub/Hook/pre-commit",
        }

        post_data["headers"] = headers

        body = json.dumps(post_data, indent=4)

        write_file("../event.json", body)

        print(body)

        url = f"https://{endpoint}/?alert_name=pre-commit"

        # conn = http.client.HTTPSConnection(endpoint, 443)
        # print("Connected")
        # conn.request("POST", url, body, headers)
        # print("Posted")
        # response = conn.getresponse()
        # print("Responded")
        # print(response.status, response.reason)
        # data = response.read()
        # conn.close()


if __name__ == "__main__":
    fire.Fire(Hook)