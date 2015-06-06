# Copyright ClusterHQ Inc. See LICENSE file for details.

"""
Acceptance tests for a temporary version of the Flocker tutorial box along
with TLS certificates that can authenticate

To run these tests:

$ trial test_acceptance
"""
import sys, os, json

from twisted.internet import defer, reactor
from twisted.web.client import Agent
from twisted.trial.unittest import TestCase
from twisted.python.filepath import FilePath
from ..txflocker.client import get_client
from ..lib.utils import run_Command, run_Vagrant

CONTROL_IP = "172.16.255.250"
CONTROL_PORT = "4523"
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

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
            CONTROL_PORT,
            )
        self.agent = Agent(reactor) # no connectionpool
        self.client = get_tls_client()

    def test_list_nodes(self):
        """
        Check that we can see both nodes using the txflocker client.
        """
        d = self.client.get(self.base_url + "/state/nodes")
        d.addCallback(treq.json_content)
        def got_nodes(nodes):
            print "got nodes"
            print nodes
        d.addCallback(got_nodes)

def get_tls_client():
    """
    Return a txflocker tls client using the credentials from this folder

    :returns: A ``treq.client.HTTPClient`` instance.
    """
    return txflocker_get_client(certificates_path=FilePath(BASE_PATH + "/credentials"),
        user_certificate_filename="user.crt",
        user_key_filename="user.key",
        target_hostname=CONTROL_IP,
    )
