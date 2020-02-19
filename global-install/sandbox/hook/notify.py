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


def repeat_to_length(one_time, length):
    return (one_time * (int(length / len(one_time)) + 1))[:length]


def divider():
    print(repeat_to_length("-", 40))


def private_key_sign(message, private_key):
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(chosen_hash, default_backend())
    hasher.update(message.encode('utf-8'))
    digest = hasher.finalize()
    sig = private_key.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        utils.Prehashed(chosen_hash)
    )
    return b64encode(sig).decode('utf-8')


def public_key_verify(signature, message, public_key):
    try:
        public_key.verify(
            b64decode(signature.encode('utf-8')),
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        verified = True
    except InvalidSignature:
        verified = False
    return verified


def get_ssh_key(host='github.com'):
    home = os.environ.get("HOME")

    identity_file = f"{home}/.ssh/id_rsa"

    result = subprocess.run(
        ["cat", f"{home}/.ssh/config"],
        stdout=subprocess.PIPE
    )
    output = result.stdout.decode('utf-8')
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


def load_private_key(key_file):
    content = read_file(key_file)
    private_key = serialization.load_pem_private_key(
        content.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    return private_key


def load_public_key(key_file):
    content = read_file(key_file)
    public_key = serialization.load_ssh_public_key(
        content.encode('utf-8'),
        backend=default_backend()
    )
    return public_key


def read_file(file_path):
    file_handle = open(file_path, "r")
    contents = file_handle.read()
    file_handle.close()
    return contents


def calc_md5(source_string):
    """Implement hashlib to calculate md5 from a given string"""
    undigested = source_string.encode('utf-8')
    hashed = hashlib.md5()
    hashed.update(undigested)
    digest = hashed.hexdigest()
    return digest


def notify(endpoint, token):
    post_data = {
        "commit": {
            'number': 12524,
            'type': 'issue',
            'action': 'show'
        }
    }

    post_data['md5'] = calc_md5(json.dumps(post_data['commit']))

    ssh_file = get_ssh_key()
    print(ssh_file)
    private_key = load_private_key(ssh_file)
    public_key = load_public_key(f"{ssh_file}.pub")

    sign = private_key_sign(post_data['md5'], private_key)

    divider()
    print("Signed")
    print(sign)
    divider()

    verified = public_key_verify(sign, post_data['md5'], public_key)

    divider()
    print("Verified?")
    print(verified)
    divider()

    result = subprocess.run(
        ['git', 'config', '--global', '-l'],
        stdout=subprocess.PIPE
    )
    output = result.stdout.decode('utf-8')
    lines = output.split("\n")
    wanted = ['user.name', 'user.email']
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
        "User-Agent": "GitHub/Hook/pre-commit"
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


if __name__ == '__main__':
    TOKEN = os.environ.get('TOKEN')
    ENDPOINT = os.environ.get('ENDPOINT')

    notify(ENDPOINT, TOKEN)
