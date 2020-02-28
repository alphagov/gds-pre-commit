#! /bin/bash

# Print usage
function usage () {
  cat << EOF

Usage:

  source generate_signed_message.sh \\
    -u github_username \\
    -k /path/to/github/ssh/private/key

OR:

  source generate_signed_message.sh \\
    --username github_username \\
    --key-file /path/to/github/ssh/private/key

EOF
}

# Parse arguments
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -u | --username )
    shift; username=$1
    ;;
  -k | --key-file )
    shift; private_key=$1
    ;;
  -h | --help )
    usage
    return
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi


# Generate random message
head -c 128 /dev/urandom | base64 > /tmp/pc-b64-random.txt

# Sign with specified private key
openssl dgst -sha256 -sigopt rsa_padding_mode:pss -sign ${private_key} -out /tmp/pc-sign.sha256 /tmp/pc-b64-random.txt
cat /tmp/pc-sign.sha256 | base64 > /tmp/pc-b64-signed.txt

# Export env vars
export GDS_GH_USERNAME="${username}"
export GDS_GH_PC_RAW="/tmp/pc-b64-random.txt"
export GDS_GH_PC_SIGN="/tmp/pc-b64-signed.txt"

# Echo vars
env | Grep GDS_GH
