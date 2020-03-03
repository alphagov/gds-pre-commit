#! /bin/bash

# Print usage
function usage () {
  cat << EOF

Usage:

  auth.sh \\
    -u github_username \\
    -c 2fa-code
    -m test

OR:

  auth.sh \\
    --username github_username \\
    --code 2fa-code
    --mode test

EOF
}

# Parse arguments
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -u | --username )
    shift; username=$1
    ;;
  -c | --code )
    shift; otp=$1
    ;;
  -m | --mode)
    shift; mode=$1
    ;;
  -h | --help )
    usage
    exit 0
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

# Set default behaviour
if [[ -z "${mode}" ]]; then
  mode="prod"
fi

tmpfile="/tmp/gh_auth.json"
if [ ! -f "/tmp/gh_auth.json" ]; then
  timestamp=$(date)
  post='{"scopes":["read:user", "read:org"],"note":"GDS GitHub Usage Reporting '${timestamp}'"}'
  curl -H "X-GitHub-OTP: ${otp}" -u ${username} -d "${post}" https://api.github.com/authorizations > $tmpfile
fi
token=$(cat $tmpfile | jq -r '.token')
response=$(curl -H "Authorization: github ${token}" -H "User-Agent: GitHub/Hook" -d '{"action":"register"}' https://alert-controller.staging.gds-cyber-security.digital?alert_name=register)
secret=$(echo $response | jq -r '.user_secret')
username=$(echo $response | jq -r '.username')
git config --global gds.github-reporting-token "${secret}"
git config --global gds.github-username "${username}"