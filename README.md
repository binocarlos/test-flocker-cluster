# test-flocker-cluster

An acceptance test for the combination of:

 * [unofficial-flocker-tools](https://github.com/lukemarsden/unofficial-flocker-tools)
 * [flocker-docker-plugin](https://github.com/clusterhq/flocker-docker-plugin)

## test.sh
A script that does the following actions:

 * spin up a vagrant cluster of 3 nodes
 * remove the ./unofficial-flocker-tools folder (if present)
 * git clone unofficial-flocker-tools to the current folder
 * use unofficial-flocker-tools/install.py to install Flocker
 * use unofficial-flocker-tools/deploy.py to configure and start Flocker
 * use unofficial-flocker-tools/plugin.py to install, configure and start flocker-docker-plugin
 * it will then run some basic `docker run busybox` commands to test everything is working



