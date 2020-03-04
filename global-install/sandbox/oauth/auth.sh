#! /bin/bash

# Print usage
function usage () {
  cat << EOF

Usage:

  auth.sh [-t | --test]

EOF
}

# Set default behaviour to real
mode="prod"
# Parse arguments
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
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

username=$(git config --global gds.github-username)
if [[ -z "${username}" ]]; then
  # Prompt user for github username
  echo "Enter your github username:"
  read username
fi
# OAuth for registration credentials
token=$(git config --global gds.github-registration-token)
if [[ -z "${token}" ]]; then
  echo "Performing GitHub OAuth"
  echo "This creates a personal access token with read:user and read:org scopes. "
  # Prompt user for 2FA
  echo "Please enter your GitHub 2FA code:"
  read otp
  echo "Requesting authorization from GitHub - You will be prompted for your GitHub password."
  timestamp=$(date)
  post='{"scopes":["read:user", "read:org"],"note":"GDS GitHub Usage Reporting '${timestamp}'"}'
  authorization=$(curl -s -H "X-GitHub-OTP: ${otp}" -u ${username} -d "${post}" https://api.github.com/authorizations)
  token=$(echo $authorization | jq -r '.token')
  git config --global gds.github-registration-token "${token}"
fi
# Register and get reporting credentials
echo "Submit registration request."
response=$(curl -s -H "Authorization: github ${token}" -H "User-Agent: GitHub/Hook" -d '{"action":"register"}' https://${endpoint}?alert_name=register)

# Check the response is JSON
response_type=$(echo $response | jq -r type)
if [[ $response_type == "object" ]]; then
  secret=$(echo $response | jq -r '.user_secret')
  username=$(echo $response | jq -r '.username')

  # Set credentials in git global config
  git config --global gds.github-reporting-token "${secret}"
  git config --global gds.github-username "${username}"
  config_user=$(git config --global gds.github-username)
  config_token=$(git config --global gds.github-reporting-token)
  if [[ -n config_token ]]; then
    echo "You have been registered successfully."
  fi
else
  echo "Registration failed please report to #cyber-security-help."
fi