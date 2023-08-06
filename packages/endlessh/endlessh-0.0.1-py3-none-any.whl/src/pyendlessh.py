#!/usr/bin/env python
"""Honeypot SSH Server Utilizing Paramiko"""
import argparse
import os
import random
import socket
import sys
import threading
import time
import traceback
from contextlib import suppress

import codefast as cf
import paramiko
from codefast.logger import Logger

logger = Logger(logname='/tmp/endlessh.log')
logger.level = 'INFO'

HOST_KEY = paramiko.RSAKey(
    filename=os.path.join(cf.io.dirname(), 'keys/private.key'))
SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"


class EndlessSSHServer(paramiko.ServerInterface):
    """Settings for paramiko server interface"""
    def __init__(self):
        self.event = threading.Event()
        self.username = None
        self.password = None

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        logger.info('Received auth information: {}/{}'.format(
            username, password))
        self.username = username
        self.password = password
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        return True


def handle_connection(client, addr):
    """Handle a new ssh connection"""
    logger.info("Got an connection from {} {}".format(client, addr))
    with suppress(Exception):
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        # Change banner to appear legit on nmap (or other network) scans
        transport.local_version = SSH_BANNER
        server = EndlessSSHServer()
        transport.start_server(server=server)
        chan = transport.accept(20)
        sleep_time = random.randint(1, 10)
        logger.info("Sleeping for {} seconds for auth ({}/{})".format(sleep_time, server.username, server.password))
        time.sleep(sleep_time)
        chan.close()
        transport.close()


def start_server(port, bind):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        try:
            sock.listen(100)
            logger.info('Listening for connection ...')
            client, addr = sock.accept()
        except Exception as err:
            logger.error('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection,
                                      args=(client, addr))
        new_thread.start()
        threads.append(new_thread)
        logger.info('Active threads: {}'.format(threading.active_count()))


def main():
    parser = argparse.ArgumentParser(description='Run a fake ssh server')
    parser.add_argument("--port",
                        "-p",
                        help="The port to bind the ssh server to (default 22)",
                        default=22,
                        type=int,
                        action="store")
    parser.add_argument("--bind",
                        "-b",
                        help="The address to bind the ssh server to",
                        default="",
                        type=str,
                        action="store")
    args = parser.parse_args()
    start_server(args.port, args.bind)


if __name__ == "__main__":
    main()
