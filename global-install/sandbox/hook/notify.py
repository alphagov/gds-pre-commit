import os
import subprocess
import hashlib
import json
from base64 import b64encode, b64decode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.exceptions import InvalidSignature
import paramiko
from paramiko.message import Message
import getpass


def repeat_to_length(one_time, length):
    return (one_time * (int(length / len(one_time)) + 1))[:length]


def divider():
    print(repeat_to_length("-", 40))


def private_key_sign(message, private_key):
    signed_data = private_key.sign(
        message.encode("utf-8"), padding=padding.PKCS1v15(), algorithm=hashes.SHA256()
    )
    b64_bytes = b64encode(signed_data)
    b64_data = b64_bytes.decode("utf-8")
    return b64_data


def public_key_verify(signature, message, public_key):
    try:
        b64_bytes = signature.encode("utf-8")
        bytes_data = b64decode(b64_bytes)
        public_key.verify(
            bytes_data, message.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
        )
        verified = True
    except InvalidSignature:
        verified = False
    return verified


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
    key_loader = paramiko.RSAKey.from_private_key_file(key_file, ssh_password)
    private_key = key_loader.key
    return private_key


def load_public_key(key_file):
    content = read_file(key_file, "rb")
    public_key = serialization.load_ssh_public_key(content, backend=default_backend())
    return public_key


def read_file(file_path, flags="r"):
    file_handle = open(file_path, flags)
    contents = file_handle.read()
    file_handle.close()
    return contents


def calc_md5(source_string):
    """Implement hashlib to calculate md5 from a given string"""
    undigested = source_string.encode("utf-8")
    hashed = hashlib.md5()
    hashed.update(undigested)
    digest = hashed.hexdigest()
    return digest


def notify(ssh_password=None):
    token = os.environ.get("TOKEN")
    endpoint = os.environ.get("ENDPOINT")
    post_data = {"commit": {"number": 12524, "type": "issue", "action": "show"}}

    post_data["md5"] = calc_md5(json.dumps(post_data["commit"]))

    ssh_file = get_ssh_key()
    print(ssh_file)
    private_key = load_private_key(ssh_file, ssh_password)
    public_key = load_public_key(f"{ssh_file}.pub")

    sign = private_key_sign(post_data["md5"], private_key)

    divider()
    print("Signed")
    print(sign)
    divider()

    verified = public_key_verify(sign, post_data["md5"], public_key)

    divider()
    print("Verified?")
    print(verified)
    divider()

    result = subprocess.run(["git", "config", "--global", "-l"], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    lines = output.split("\n")
    wanted = ["user.name", "user.email"]
    for line in lines:
        terms = line.split("=")
        if len(terms) > 1:
            key = terms[0]
            value = terms[1]
            if key in wanted:
                post_data[key] = value

    body = json.dumps(post_data)

    print(body)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "GitHub/Hook/pre-commit",
    }

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

    ssh_password = getpass.getpass("Password:").encode()
    notify(ssh_password)
