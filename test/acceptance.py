# Copyright ClusterHQ Inc. See LICENSE file for details.

"""
Acceptance tests for a temporary version of the Flocker tutorial box along
with TLS certificates that can authenticate

To run these tests you first need a running Flocker cluster.

You can point these tests at an existing cluster or create one
using the boot.sh script in this repo

$ trial test.acceptance
"""
import sys, os, json, treq, datetime

from treq.client import HTTPClient
from twisted.internet import defer, reactor
from twisted.web.client import Agent
from twisted.trial.unittest import TestCase
from twisted.python.filepath import FilePath
from txflocker.client import get_client

# the base test folder
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# the IP address of the control node
CONTROL_IP = os.environ.get("CONTROL_IP", "172.16.255.250")
# the IP address of the agent node
AGENT_IP = os.environ.get("AGENT_IP", "172.16.255.251")
# the port of the control node
CONTROL_PORT = os.environ.get("CONTROL_PORT", 4523)
# the folder where the credentials live
CERTS_FOLDER = os.environ.get("CERTS_FOLDER", 
    os.path.realpath(BASE_PATH + "/../_files"))
# the name of the cluster.crt file
CLUSTER_CERT = os.environ.get("CLUSTER_CERT", "cluster.crt")
# the name of the user.crt file
USER_CERT = os.environ.get("USER_CERT", "user.crt")
# the name of the user.key file
USER_KEY = os.environ.get("USER_KEY", "user.key")
# the name of the volume to use for these tests
epoch = datetime.datetime.utcfromtimestamp(0)
delta = datetime.datetime.now() - epoch
VOLUME_NAME = "volume" + str(int(delta.total_seconds()))
# the size of the volume to create
VOLUME_SIZE = 1024 * 1024 * 200

def unix_time(dt):
    """
    Return the seconds since the epoch
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

class FlockerTutorialTests(TestCase):
    """
    Use the txflocker client library to do some basic tests against
    the existence of a working Flocker cluster
    """

    def setUp(self):
        """
        Get the cluster setup:

        * vagrant up to start & provision the 2 nodes
        * create a client using txflocker and the credentials folder
        """
        self.base_url = "https://%s:%s/v1" % (
            CONTROL_IP,
            CONTROL_PORT,)
        self.agent = Agent(reactor) # no connectionpool
        self.client = get_client(
            certificates_path=FilePath(CERTS_FOLDER),
            cluster_certificate_filename=CLUSTER_CERT,
            user_certificate_filename=USER_CERT,
            user_key_filename=USER_KEY,
            target_hostname=CONTROL_IP,)

    def tearDown(self):
        """
        Stop the vagrant cluster
        """
        pass

    def test_list_nodes(self):
        """
        Check that we can see both nodes using the txflocker client.

        We are looking for the host property in each object from a
        call to the /state/nodes endpoint.  We should see both 
        CONTROL_IP and AGENT_IP in the results
        """
        d = self.client.get(self.base_url + "/state/nodes")
        d.addCallback(treq.json_content)
        def got_nodes(nodes):
            ips = {}
            for node in nodes:
                ips[node["host"]] = True
            self.assertEqual(ips[CONTROL_IP], True)
            self.assertEqual(ips[AGENT_IP], True)
        return self._list_nodes()
        d.addCallback(got_nodes)
        return d

    def test_create_volume(self):
        """
        Check that we can create a volume on node1
        First map the nodeip -> nodeuuid
        Then POST to /configuration/datasets
        Then GET /configuration/datasets
        Then WAIT /state/datasets
        """
        def create_volume(node_uuid):
            """
            Use the node uuid to create a volume against it
            We post a JSON body with a 200Mb maximum size
            and a name - we then check /configuration/datasets
            for a volume with that name and size
            """
            self.assertTrue(len(node_uuid) > 0)
            body = {
                "metadata":{
                    "name":VOLUME_NAME
                },
                "maximum_size":VOLUME_SIZE,
                "primary":node_uuid
            }
            
            d = self.client.post(
                self.base_url + "/configuration/datasets",
                json.dumps(body),
                headers={'Content-Type': ['application/json']})
            d.addCallback(treq.json_content)
            def dataset_created(data):
                self.assertEqual(data["deleted"], False)
                self.assertEqual(data["metadata"]["name"], VOLUME_NAME)
                self.assertEqual(data["maximum_size"], VOLUME_SIZE)
                self.assertEqual(data["primary"], node_uuid)                
            d.addCallback(dataset_created)
            return d
        # first we must get the uuid for the AGENT_IP
        d = self._uuid_from_ip(AGENT_IP)
        # once we have the uuid of the node we create the volume
        d.addCallback(create_volume)
        return d

    def test_configuration(self):
        """
        Check the configuration for the volume we just created
        """
        def load_volumes(uuid):
            def volumes_loaded(volumes):
                found_volume = None
                for volume in volumes:
                    print "%s = %s" % (volume["metadata"]["name"], VOLUME_NAME,)
                    if volume["metadata"]["name"] == VOLUME_NAME:
                        found_volume = volume
                        break
                print "NODE UUID %s" % (uuid,)
                self.assertTrue(found_volume is not None)
                self.assertEqual(found_volume["deleted"], False)
                self.assertEqual(found_volume["primary"], uuid)
                self.assertEqual(found_volume["metadata"]["name"], VOLUME_NAME)
                self.assertEqual(found_volume["maximum_size"], VOLUME_SIZE)
            d = self._list_configuration()
            d.addCallback(volumes_loaded)
            return d
        d = self._uuid_from_ip(AGENT_IP)
        d.addCallback(load_volumes)
        return d

    def _list_nodes(self):
        """
        Query the /state/nodes endpoint
        """
        d = self.client.get(self.base_url + "/state/nodes")
        d.addCallback(treq.json_content)
        return d

    def _list_configuration(self):
        """
        Query the /configuration/datasets endpoint
        """
        d = self.client.get(self.base_url + "/configuration/datasets")
        d.addCallback(treq.json_content)
        return d

    def _list_state(self):
        """
        Query the /state/datasets endpoint
        """
        d = self.client.get(self.base_url + "/state/datasets")
        d.addCallback(treq.json_content)
        return d

    def _uuid_from_ip(self, nodeip):
        """
        Loop over the nodes in the cluster and try to 
        match the given ip and return the uuid for that node
        """
        def got_nodes(nodes):
            for node in nodes:
                if node["host"] == nodeip:
                    return node["uuid"]
            return None
        d = self._list_nodes()
        d.addCallback(got_nodes)
        return d