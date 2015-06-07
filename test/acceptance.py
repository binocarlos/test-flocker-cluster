# Copyright ClusterHQ Inc. See LICENSE file for details.

"""
Acceptance tests for a temporary version of the Flocker tutorial box along
with TLS certificates that can authenticate

To run these tests:

$ trial test.acceptance
"""
import sys, os, json, treq

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
        d.addCallback(got_nodes)
        return d

def get_tls_client():
    """
    Return a txflocker tls client using the credentials from this folder

    :returns: A ``treq.client.HTTPClient`` instance.
    """
    #return get_client(certificates_path=FilePath(BASE_PATH + "/credentials"),
    #    user_certificate_filename="user.crt",
    #    user_key_filename="user.key",
    #    target_hostname=CONTROL_IP,
    #)
