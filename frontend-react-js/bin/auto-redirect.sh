#! /usr/bin/bash

aws cognito-idp update-user-pool-client \
--user-pool-id us-east-1_hPjcORESI \
--client-id 5t0cj7t22bfcegaji4ln3i716h \
--callback-urls https://3000-$GITPOD_WORKSPACE_ID.$GITPOD_WORKSPACE_CLUSTER_HOST \
--logout-urls https://3000-$GITPOD_WORKSPACE_ID.$GITPOD_WORKSPACE_CLUSTER_HOST \
--supported-identity-providers Google \
--allowed-o-auth-flows-user-pool-client \
--allowed-o-auth-flows implicit \
--allowed-o-auth-scopes {email,openid,profile,aws.cognito.signin.user.admin}