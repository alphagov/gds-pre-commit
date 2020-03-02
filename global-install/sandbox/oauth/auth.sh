#! /bin/bash

# Print usage
function usage () {
  cat << EOF

Usage:

  source auth.sh \\
    -u github_username \\
    -c otp-code

OR:

  source auth.sh \\
    --username github_username \\
    --otp-code otp-code

EOF
}

# Parse arguments
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -u | --username )
    shift; username=$1
    ;;
  -c | --otp-code )
    shift; otp=$1
    ;;
  -h | --help )
    usage
    return
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

timestamp=$(date)
curl -H "X-GitHub-OTP: ${otp}" -u ${username} -d '{"scopes":["read:user"],"note":"gh_auth ${timestamp}"}' https://api.github.com/authorizations > /tmp/gh_auth.json
token=$(cat /tmp/gh_auth.json | jq -r '.token')
curl -H "Authorization: github ${token}" -d '{"action":"register"}' https://alert-controller.staging.gds-cyber-security.digital?alert_name=register
rm /tmp/gh_auth.json