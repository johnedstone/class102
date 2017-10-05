# Source this file  for Env Vars, e.g. local devlopment, sever deployment, etc
unset AWS_ACCESS_KEY
unset AWS_SECRET_KEY
unset HTTPS_PROXY
unset HTTP_PROXY

export AWS_ACCESS_KEY='access_key'
export AWS_SECRET_KEY='secret_key'
export HTTPS_PROXY='https://ip:port'
export HTTP_PROXY='http://ip:port'

# Optional
unset DEBUG
unset ALLOWED_HOSTS
unset SECRET_KEY
unset SUCCESS_MSG_NEW_BUCKET
unset SUCCESS_MSG_PREEXISTING_BUCKET
unset AWS_NO_RESPONSE
unset PROJECT_LOGGING_LEVEL

export DEBUG=
export ALLOWED_HOSTS=
export SECRET_KEY=
export SUCCESS_MSG_NEW_BUCKET=
export SUCCESS_MSG_PREEXISTING_BUCKET=
export AWS_NO_RESPONSE=
export PROJECT_LOGGING_LEVEL= # WARNING|INFO
