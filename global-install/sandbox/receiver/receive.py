import json
from base64 import b64encode, b64decode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.exceptions import InvalidSignature
import paramiko
import requests


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


def get_github_keys(username):
    github_keys = requests.get(f"https://api.github.com/users/{username}/keys")
    return github_keys.json()


def load_public_key(key_data):
    content = key_data.encode()
    public_key = serialization.load_ssh_public_key(content, backend=default_backend())
    return public_key


def read_file(file_path, flags="r"):
    file_handle = open(file_path, flags)
    contents = file_handle.read()
    file_handle.close()
    return contents


def receive():
    event_json = read_file("../event.json")
    event = json.loads(event_json)
    public_keys = get_github_keys(event["username"])
    verified = False
    sign = event["headers"]["Authorization"].split()[1]
    for key_entry in public_keys:
        public_key = load_public_key(key_entry["key"])
        verified = verified or public_key_verify(sign, event["md5"], public_key)
    print("Verified?")
    print(verified)


if __name__ == "__main__":
    receive()
