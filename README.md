# test-flocker-cluster

A scripted run through of the [Getting Started Guide](http://doc-dev.clusterhq.com/gettingstarted/index.html) from [flocker master](https://github.com/clusterhq/flocker/tree/master)

## install

The script is a single bash script that spins up a Vagrant cluster based on the latest tutorial box.  You need Virtualbox and Vagrant installed on your machine then:

```
$ git clone https://github.com/binocarlos/test-flocker-cluster
$ cd test-flocker-cluster
```

## boot

To start a 2 node Vagrant cluster with TLS keys:

```
$ make boot
```

Variables to control this script:

#### BOX_URL
Where to download the Vagrant box from:
`http://build.clusterhq.com/results/vagrant/master/flocker-tutorial.json`

#### BASE_URL
Where to download the Vagrantfile and certs from:
`http://doc-dev.clusterhq.com`

## test
Once the cluster has spun up you can use the TLS certs directly:

```
$ curl -s \
    --cacert $PWD/credentials/cluster.crt \
    --cert $PWD/credentials/user.crt \
    --key $PWD/credentials/user.key \
    https://172.16.255.250:4523/v1/state/nodes
```

To run the acceptance tests:

```
$ make test
```

## use in other projects
You can git clone this repo to use as a basic acceptance test target for other
projects.