# test-flocker-cluster

A scripted run through of the [Getting Started Guide](http://doc-dev.clusterhq.com/gettingstarted/index.html) from [flocker master](https://github.com/clusterhq/flocker/tree/master)

There are 2 parts that can be used seperately:

##### `boot.sh`
A script that boots a 2 node Vagrant cluster based on the latest tutorial box
from buildbot (which uses the ZFS backend).

##### `tox`
Run some basic acceptance tests against a Flocker cluster

## quickstart

```
$ git clone https://github.com/binocarlos/test-flocker-cluster
$ cd test-flocker-cluster
$ make install
$ make boot
$ make test-install
```

## boot

To start a 2 node Vagrant cluster with TLS keys:

```
$ bash boot.sh
```

Variables to control this script:

##### `BOX_URL`
Where to download the Vagrant box from:
`http://build.clusterhq.com/results/vagrant/master/flocker-tutorial.json`

##### `BASE_URL`
Where to download the Vagrantfile and certs from:
`http://doc-dev.clusterhq.com`

##### `DOWNLOAD_FOLDER`
The folder to download the Vagrantfile and certs
`_files`

The download folder is where the Vagrantfile and .vagrant folder are created.

If you want to re-boot a new cluster make sure you `vagrant destroy` and `rm -rf $DOWNLOAD_FOLDER`.

## manual tests
Once the cluster has spun up you can use the TLS certs directly:

```
$ curl -s \
    --cacert $PWD/_files/cluster.crt \
    --cert $PWD/_files/user.crt \
    --key $PWD/_files/user.key \
    https://172.16.255.250:4523/v1/state/nodes
```

## acceptance tests
To run the acceptance tests the first time:

```
$ tox -r
```

Subsequent times:

```
$ tox
```

Variables to control the tests:

##### `CONTROL_IP`
The IP address of the control service
`172.16.255.250`

##### `CONTROL_PORT`
The port of the control service
`4523`

##### `CERTS_FOLDER`
The folder where the credentials live
`BASE_PATH + "/../_files"`

##### `CLUSTER_CERT`
The name of the cluster certificate file
`cluster.crt`

##### `USER_CERT`
The name of the user certificate file
`user.crt`

##### `USER_KEY`
The name of the user key file
`user.key`