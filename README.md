Update - October 2021
I switched from certbot to dehydrated.sh script
This hook should still work for certbot, but will no longer be maintained.
Dehydrated hooks can be found in this repository: https://github.com/BrandonSk/dehydrated-hooks-for-websupport.sk

Update - November 2019
v2.0 released

### It is now mandatory to use the image brandonsk/certbot_websupportsk
* it is a certbot image where python3 module requests is added
* on top of that timezone of the image is set to CET time (and must remain so, until websupport makes its api compatible with other timezone settings)

# tl;dr or Quickstart
This quickstart is for running this as a docker container:
* create directories for certbot, directory for certificates, and directory for scripts
* (e.g. ~/docker/certbot; ~/docker/certbot/scripts; ~/docker/shared/letsencrypt/etc; ~/docker/shared/letsencrypt/var)
* In certbot directory place the files first_run.sh; renewal.sh;
first_run.sh
```
#!/bin/bash

docker run \
	--rm \
	-v /your/letsencrypt/etc/directory:/etc/letsencrypt \
	-v /your/certbot/scripts/directory:/scripts \
	-v /your/letsencrypt/var/directory:/var/lib/letsencrypt \
	-v /var/run/docker.sock:/var/run/docker.sock \
	brandonsk/websupport_certbot \
  certonly \
  --manual \
  --non-interactive \
  --preferred-challenges=dns \
  --agree-tos \
  --email your@email.here \
  --manual-public-ip-logging-ok \
  --manual-auth-hook /scripts/websupport_auth_hook.sh \
  --manual-cleanup-hook /scripts/websupport_cleanup_hook.sh \
  -d yourdomain.com \
  -d *.yourdomain.com
```
renewal.sh
```
docker run \
	--rm \
	-v v_certs:/etc/letsencrypt \
	-v v_certbot:/scripts \
	-v /var/run/docker.sock:/var/run/docker.sock \
	brandonsk/websupport_certbot \
	renew
```

* In certbot/scripts directory place the hook files (websupport_auth_hook.sh and websupport_cleanup_hook.sh) as well as the python scripts (create_dns_record.py, erase_dns_record.py).
* Finally in scripts directory also place the ws_secrets file and replace your apikey and apisecret inside. Make this file owned by root and chmod 400.
* Run the "first_run.sh"
* Schedule the renewal.sh in root's cron to run on schedule as you find appropriate. Mine is once a week.

Final note: The cleanup script is not erasing things at the moment, but that does not matter, as the certificates get generated anyway.

========== End of Quickstart ==========

(information below may not be up to date and will be eventually updated)

# certbot_websupportsk
Hook-up scripts (provider WebSupport.sk) for certbot manual mode with DNS challenge for generating wildcard certificates.
Scripts should be POSIX compliant according to shellcheck.net

Created by Branislav Susila, May 2018.

## Requirements
* Linux system with curl (tested on Debian, should work on other systems too)
* certbot supporting wildcard certificates (ideally the latest version)
> careful, certbot in repositories might be too old, in that case download from github
* OR use docker! *(note: docker requires an image with curl installed! Tested with image soshnikov/certbot which is original certbot/certbot with curl)*

## Installation
1. download hookup scripts and the secrets file and place all 3 files into a directory of your choosing
2. edit the ws_secrets file: First line -> your websupport login name; Second line -> your websupport password
3. change permissions of ws_secrets to 400 or 600 and make sure its owned by root
4. make the two hookup scripts executable

*Alternative to the steps 2 & 3 is to store username and password directly in both of the scripts in variables (not recommended)*

## Usage
This guide does not cover certbot options - study certbot documentation for variety of modes how to use it.

### First start with tests - option --staging
Here is a basic example, which will:
* create wildcard certificate for domain example.com and \*.example.com
* save the certificate and private key into /etc/letsencrypt/live and /etc/letsencrypt/keys respectively
(scripts and secrets file are located in /home/foobar/scripts)

Obtain certificate from staging server:
```
sudo certbot certonly \
  --manual \
  --preferred-challenges=dns \
  --non-interactive \
  --staging \
  --agree-tos \
  --manual-public-ip-logging-ok \
  --manual-auth-hook /home/foobar/scripts/websupport_auth_hook.sh \
  --manual-cleanup-hook /home/foobar/scripts/websupport_cleanup_hook.sh \
  -d example.com \
  -d *.example.com
```
Test if renewal also works:
```
sudo certbot renew --force-renewal
```

### Get production certificates
To get production certificates, you should first clear content of /etc/letsencrypt.
Next modify the above command:
* remove the --staging line
* consider adding option -m your_email@wherever.com (to get important notifications about your certificates)

Once the certificates are generated and saved, you can use them with your favorite software.

#### Renewal
You can use root's cron to renew.
Add line (once a day is more than enough): `certbot renew >> /dev/null`

## Docker example
```
docker run \
	--rm \
	-v /home/foobar/letsencrypt/:/etc/letsencrypt \
	-v /home/foobar/scripts/:/scripts \
	soshnikov/certbot \
  certonly \
  --manual \
  --preferred-challenges=dns \
  --non-interactive \
  --staging \
  --agree-tos \
  --email yourmail@yourdomain.com \
  --manual-public-ip-logging-ok \
  --manual-auth-hook /scripts/websupport_auth_hook.sh \
  --manual-cleanup-hook /scripts/websupport_cleanup_hook.sh \
  -d example.com \
  -d *.example.com
```
## Caviats and other information
1. Scripts tested and work under debian stretch with certbot 0.25.0.dev0 installed from git source.
2. Using special characters in webssuport's username/password might not work - I have not tested this yet. You may have to specify the username/password in escaped format (or modify the scripts and publish them here).
3. Scripts are POSIX compliant. Some lines could be written perhaps more efficient, but compatibility with busybox is needed to be able to use above mentioned docker image.
4. Using docker image (soshnikov/certbot) should give you the best way to use the most up-to-date certbot client. You can use volume mappings to save certificates to wherever you want.
5. It is possible to define post-hook scripts, which will restart/reload your software config to use updated certificate.
6. I'm not a programmer, so feel free to make the above scripts better ;)
