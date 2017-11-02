#!/bin/bash
[[ -z $1 || -z $2 ]] && { echo "Usage: $0 <TOKEN-CODE> <USERID>"; exit 1; }

unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN

USERNAME=$2
MFA_URN=$(aws iam list-mfa-devices --user-name ${USERNAME} | jq -r '.MFADevices[].SerialNumber')

STS_OUTPUT=$(aws sts get-session-token --serial-number ${MFA_URN} --token-code $1)

cat << EOF > token-env
export AWS_ACCESS_KEY_ID=$(echo ${STS_OUTPUT} | jq '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo ${STS_OUTPUT} | jq '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo ${STS_OUTPUT} | jq '.Credentials.SessionToken')
EOF
echo "Please set the access token via:"
echo -e "\t. "$(pwd)"/token-env && rm "$(pwd)"/token-env"
