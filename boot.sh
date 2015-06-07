#!/usr/bin/env bash

export BOX_URL=${BOX_URL:=http://build.clusterhq.com/results/vagrant/master/flocker-tutorial.json}
export BASE_URL=${BASE_URL:=http://doc-dev.clusterhq.com}

#vagrant box add $BOX_URL

rm -rf _tutorial
mkdir -p _tutorial

# we just 
curl -s ${BASE_URL}/_downloads/Vagrantfile \
    | grep -vE 'config\.vm\.box_url|config\.vm\.box_version' > Vagrantfile

curl -O ${BASE_URL}/_downloads/Vagrantfile
curl -O ${BASE_URL}/_downloads/cluster.crt
curl -O ${BASE_URL}/_downloads/user.crt
curl -O ${BASE_URL}/_downloads/user.key