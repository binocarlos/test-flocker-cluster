# tutorial

A Vagrant setup based on the [flocker tutorial box](http://doc-dev.clusterhq.com/gettinginvolved/infrastructure/vagrant.html#boxes) that will start 2 nodes and provide the TLS credentials to 
connect.  The agents are using the zfs backend.

The environment variables to control the Vagrant box:

 * VAGRANT_BOX (clusterhq/flocker-tutorial)
 * VAGRANT_BOX_URL (https://clusterhq-archive.s3.amazonaws.com/vagrant/flocker-tutorial.json)
 * VAGRANT_BOX_VERSION (= 0.4.1dev1)

```
$ vagrant up
$ curl -s \
    --cacert $PWD/credentials/cluster.crt \
    --cert $PWD/credentials/user.crt \
    --key $PWD/credentials/user.key \
    https://172.16.255.250:4523/v1/state/nodes
```