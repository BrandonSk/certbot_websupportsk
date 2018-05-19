#!/bin/bash
# (C) 2018 Branislav Susila

# SPECIFY LOGIN DETAILS BELOW:
# Option 1 - store login in these scripts by populating WS_USER and WS_PW variables
# Option 2 - store login details in a file (owned by root and permission 400 or 600): 1st line- name; 2nd- password
# 		and specify path into WS_USER variable

# Option 1
WS_USER=""
WS_PW=""
# Option 2 (below example expects file named ws_secrets to be in same directory as these scripts)
WS_USER=$(dirname "$(readlink -f "$0")") && WS_USER="${WS_USER}/ws_secrets"

# FUNCTIONS
_process_secrets_file() {
        [ ! $(stat -c %u "${1}") -eq 0 ] && echo "Secrets file must be owned by root!" && exit 2
        [ ! $(stat -c %a "${1}") -eq 600 ] && [ ! $(stat -c %a "${1}") -eq 400 ] \
                && echo "Secrets file not secure enough!" && exit 2
        i=1
        while IFS='' read -r line || [[ -n "$line" ]]; do
                [ ${i} -gt 2 ] && break
                a[$i]="$line"
                (( i ++ ))
        done < "${1}"
        WS_USER="${a[1]}"
        WS_PW="${a[2]}"
        unset a[1]
	unset a[2]
}

# >>>>>>> Main script starts here <<<<<<<<

[ -f "${WS_USER}" ] && _process_secrets_file "${WS_USER}"

ACMC="_acme-challenge"

# Parse the json output to get record ID
ID=$(echo "${CERTBOT_AUTH_OUTPUT}" | grep -Po '"id":(\d*?,|.*?[^\\]",)' | awk -F':' '{print $2}')
ID="${ID%,}"

#Erase record:
curl --silent "https://rest.websupport.sk/v1/user/self/zone/${CERTBOT_DOMAIN}/record/${ID}" \
  -X DELETE -u ${WS_USER}:${WS_PW} 2>&1
