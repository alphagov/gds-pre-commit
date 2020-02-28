import os
import json
from base64 import b64decode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import requests


def public_key_verify(signature, message, public_key):
    try:
        b64_bytes = signature.encode("utf-8")
        bytes_data = b64decode(b64_bytes)

        pss_padding = padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        )

        public_key.verify(
            bytes_data,
            message.encode("utf-8"),
            padding=pss_padding,
            algorithm=hashes.SHA256()
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

if __name__ == "__main__":
    username = os.environ.get("GDS_GH_USER")

    sign_file_path = os.environ.get("GDS_GH_PC_SIGN")
    raw_file_path = os.environ.get("GDS_GH_PC_RAW")
    with open(sign_file_path, "r") as sign_file:
        signature = sign_file.read()
    with open(raw_file_path, "r") as raw_file:
        message = raw_file.read()

    public_keys = get_github_keys(username)
    verified = False
    for key_entry in public_keys:
        public_key = load_public_key(key_entry["key"])
        verified = verified or public_key_verify(signature, message, public_key)
    print("Verified?")
    print(verified)