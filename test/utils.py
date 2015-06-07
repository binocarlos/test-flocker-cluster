# Copyright ClusterHQ Inc. See LICENSE file for details.
"""
A collection of utilities for the acceptance tests
"""
from pipes import quote as shell_quote
from subprocess import PIPE, Popen

def run_Vagrant(node, command, input):
    """
    Run a command using 'vagrant ssh <node> -c <command>

    :param node: The name of the vagrant node to run the command
    :type node: ``list`` of ``bytes``.
    :param command: The command to run via vagrant ssh on the node
    :type command: ``list`` of ``bytes``.

    :return: stdout as ``bytes``
    """
    return run_Command(
        "vagrant ssh %s -c \"%s\"" % (node, command,),
        input,
    )

def run_Command(command, input):
    """
    Run a command

    :param command: Command to run.
    :type command: ``list`` of ``bytes``.
    :param bytes input: Input to send to command.

    :return: stdout as ``bytes``
    """
    quotedCommand = ' '.join(map(shell_quote, command))
    command = [
        b'sh',
        b'-c',
        ]
    command.extend([
        quotedCommand
    ])

    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    result = process.communicate(input)
    if process.returncode != 0:
        raise Exception('Command Failed', command, process.returncode, result)

    return result[0]
