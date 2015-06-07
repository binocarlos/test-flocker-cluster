#!/usr/bin/env bash

export BOX_URL=${BOX_URL:=http://build.clusterhq.com/results/vagrant/master/flocker-tutorial.json}
export BASE_URL=${BASE_URL:=http://doc-dev.clusterhq.com}
export DOWNLOAD_FOLDER=${DOWNLOAD_FOLDER:=_files}
#vagrant box add $BOX_URL

if [[ -f "$DOWNLOAD_FOLDER/Vagrantfile" ]]; then
    >&2 echo "Existing installation found: $DOWNLOAD_FOLDER"
    >&2 echo "vagrant destroy - remove that folder and try again"
    exit 1
fi

rm -rf $DOWNLOAD_FOLDER
mkdir -p $DOWNLOAD_FOLDER
cd $DOWNLOAD_FOLDER

# remove the box_url and box_version lines from the Vagrantfile 
curl -s ${BASE_URL}/_downloads/Vagrantfile \
    | grep -vE 'config\.vm\.box_url|config\.vm\.box_version' > Vagrantfile

# download the certs
curl -sO ${BASE_URL}/_downloads/cluster.crt
curl -sO ${BASE_URL}/_downloads/user.crt
curl -sO ${BASE_URL}/_downloads/user.key