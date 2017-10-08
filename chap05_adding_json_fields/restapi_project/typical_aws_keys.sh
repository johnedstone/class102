# Source this file  for Env Vars, e.g. local devlopment, sever deployment, etc
unset AWS_ACCESS_KEY
unset AWS_SECRET_KEY
unset AWS_HTTPS_PROXY
unset AWS_HTTP_PROXY

export AWS_ACCESS_KEY='access_key'
export AWS_SECRET_KEY='secret_key'
export AWS_HTTPS_PROXY='https://ip:port'
export AWS_HTTP_PROXY='http://ip:port'

# Postgresql local development, not needed for openshift template
unset DATABASE_SERVICE_NAME
unset DATABASE_ENGINE
unset DATABASE_NAME
unset DATABASE_USER
unset DATABASE_PASSWORD

export DATABASE_SERVICE_NAME=postgresql
export DATABASE_ENGINE=postgresql
export DATABASE_NAME=db_name
export DATABASE_USER=db_user
export DATABASE_PASSWORD=db_password

## Optional
# unset DEBUG
# unset ALLOWED_HOSTS
# unset SECRET_KEY
# unset SUCCESS_MSG_NEW_BUCKET
# unset SUCCESS_MSG_PREEXISTING_BUCKET
# unset AWS_NO_RESPONSE
# unset PROJECT_LOGGING_LEVEL
# export DEBUG=
# export ALLOWED_HOSTS=
# export SECRET_KEY=
# export SUCCESS_MSG_NEW_BUCKET=
# export SUCCESS_MSG_PREEXISTING_BUCKET=
# export AWS_NO_RESPONSE=
# export PROJECT_LOGGING_LEVEL= # WARNING|INFO
