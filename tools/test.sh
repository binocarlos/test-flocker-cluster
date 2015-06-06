#!/bin/sh

export TOOLS_REPO=${TOOLS_REPO:="https://github.com/binocarlos/unofficial-flocker-tools"}
# this branch is a merge of the install-plugin and install-zfs branches
export TOOLS_BRANCH=${TOOLS_BRANCH:="master"}
export PLUGIN_REPO=${PLUGIN_REPO:="https://github.com/clusterhq/flocker-docker-plugin"}
export PLUGIN_BRANCH=${PLUGIN_BRANCH:="txflocker-env-vars"}

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# manually configure the nodes from the vagrantfile
runner1=172.16.160.10
runner2=172.16.160.11
master=172.16.160.12

# use this ssh key to connect to the nodes
sshkey=$DIR/insecure_private_key

# ensure that permissions are set correctly on the ssh keys
chmod 0600 $DIR/insecure_private_key $DIR/insecure_private_key.pub

if [[ -d "$DIR/unofficial-flocker-tools" ]]; then
  rm -rf $DIR/unofficial-flocker-tools
fi

cd $DIR && git clone $TOOLS_REPO
cd $DIR/unofficial-flocker-tools

cat << EOF > $DIR/unofficial-flocker-tools/cluster.yml
cluster_name: flockerdemo
agent_nodes:
 - {public: $master, private: $master}
 - {public: $runner1, private: $runner1}
 - {public: $runner2, private: $runner2}
control_node: $master
users:
 - flockerdemo
os: ubuntu
private_key_path: $sshkey
agent_config:
  version: 1
  control-service:
     hostname: $master
     port: 4524
  dataset:
    backend: "zfs"
EOF

cd $DIR/unofficial-flocker-tools && ./install.py cluster.yml
#cd $DIR/unofficial-flocker-tools && ./deploy.py cluster.yml
#cd $DIR/unofficial-flocker-tools && \
#  DOCKER_BINARY_URL=http://storage.googleapis.com/experiments-clusterhq/docker-binaries/docker-volumes-network-combo \
#  DOCKER_SERVICE_NAME=docker.io \
#  PLUGIN_REPO=https://github.com/clusterhq/flocker-docker-plugin \
#  PLUGIN_BRANCH=txflocker-env-vars \
#  ./plugin.py cluster.yml