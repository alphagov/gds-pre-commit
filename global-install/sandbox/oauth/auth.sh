#! /bin/bash

# Print usage
function usage () {
  cat << EOF

You need to be on the GDS VPN or office network
Usage:

  auth.sh \\
    -u github_username \\
    -c github 2fa-code \\
    [-t]

OR:

  auth.sh \\
    --username github_username \\
    --code github 2fa-code \\
    [--test]

EOF
}

# Set default behaviour to real
mode="prod"
# Parse arguments
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -u | --username )
    shift; username=$1
    ;;
  -c | --code )
    shift; otp=$1
    ;;
  -t | --test)
    mode="test"
    ;;
  -h | --help )
    usage
    exit 0
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

# Change the submission URL based on the mode argument
if [[ $mode == "prod" ]]; then
  endpoint="alert-controller.gds-cyber-security.digital"
else
  endpoint="alert-controller.staging.gds-cyber-security.digital"
fi

# OAuth for registration credentials
echo "Perform GitHub OAuth - you will be prompted for your GitHub password."
echo "This creates a personal access token with read:user and read:org scopes. "
timestamp=$(date)
post='{"scopes":["read:user", "read:org"],"note":"GDS GitHub Usage Reporting '${timestamp}'"}'
authorization=$(curl -s -H "X-GitHub-OTP: ${otp}" -u ${username} -d "${post}" https://api.github.com/authorizations)
token=$(echo $authorization | jq -r '.token')

# Register and get reporting credentials
echo "Submit registration request."
response=$(curl -s -H "Authorization: github ${token}" -H "User-Agent: GitHub/Hook" -d '{"action":"register"}' https://${endpoint}?alert_name=register)
# This is a shared secret stored in SSM against your username - not your GitHub token
secret=$(echo $response | jq -r '.user_secret')
username=$(echo $response | jq -r '.username')

# Set credentials in git global config
git config --global gds.github-reporting-token "${secret}"
git config --global gds.github-username "${username}"
config_user=$(git config --global gds.github-username)
config_token=$(git config --global gds.github-reporting-token)
if [[ -n config_user and -n config_token ]]; then
  echo "You have been registered successfully."
fi