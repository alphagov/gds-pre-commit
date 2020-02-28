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


def read_file(file_path, flags="r"):
    file_handle = open(file_path, flags)
    contents = file_handle.read()
    file_handle.close()
    return contents


def receive():
    event_json = read_file("../event.json")
    print(event_json)
    event = json.loads(event_json)
    public_keys = get_github_keys(event["username"])
    verified = False
    signed_data = bytes.fromhex(event["headers"]["Authorization"].split()[1]).decode('utf-8')
    verify_data = bytes.fromhex(event["verify"]).decode('utf-8')

    for key_entry in public_keys:
        public_key = load_public_key(key_entry["key"])
        this_verified = public_key_verify(signed_data, verify_data, public_key)
        verified = verified or this_verified

    print(f"\nVerified? {verified}")


if __name__ == "__main__":
    receive()
