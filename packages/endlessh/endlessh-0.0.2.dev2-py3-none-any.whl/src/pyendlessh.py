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
from abc import ABC, abstractmethod
from binascii import hexlify
from contextlib import suppress
from dataclasses import dataclass
from logging import log

import codefast as cf
import paramiko
from codefast.logger import Logger

logger = Logger(logname='/tmp/endlessh.log')
logger.level = 'INFO'


@dataclass
class SSHServer:
    HOST_KEY: str = paramiko.RSAKey(
        filename=os.path.join(cf.io.dirname(), 'keys/private.key'))
    SSH_BANNER: str = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"


class ClientCache(object):
    fingerprint = {}


class SleepTimer:
    def __init__(self, sleep_time):
        self.sleep_time = sleep_time

    def __enter__(self):
        time.sleep(self.sleep_time)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class BasicSshHoneypot(paramiko.ServerInterface):
    def __init__(self,
                 client_ip,
                 min_sleep_time: int = 1,
                 max_sleep_time: int = 10):
        self.client_ip = client_ip
        self.event = threading.Event()
        self.min = min_sleep_time
        self.max = max_sleep_time

    def check_channel_request(self, kind, chanid):
        logger.info('client called check_channel_request ({}): {}'.format(
            self.client_ip, kind))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        logger.info('client {} checked auth method with username {}'.format(
            self.client_ip, username))
        return "publickey,password"

    def check_auth_publickey(self, username, key):
        with SleepTimer(random.randint(self.min, self.max)) as timer:
            fingerprint = str(hexlify(key.get_fingerprint()))
            if fingerprint in ClientCache.fingerprint:
                logger.info(
                    'client sent publickey ({}) with fingerprint {}'.format(
                        self.client_ip, fingerprint))
                return paramiko.AUTH_FAILED
            ClientCache.fingerprint[fingerprint] = True

            logger.info(
                'client sent publickey, client ip: {}, usename: {}, md5 fingerprint: {}, base64: {}, bits: {}'
                .format(self.client_ip, username, fingerprint, key.get_base64(),
                        key.get_bits()))
            logger.info('sleep time {}'.format(timer.sleep_time))
            return paramiko.AUTH_PARTIALLY_SUCCESSFUL

    def check_auth_password(self, username, password):
        with SleepTimer(random.randint(self.min, self.max)) as timer:
            logger.info('client sent (username, password) pair ({}, {})'.format(
                username, password))
            logger.info('sleep time {}'.format(timer.sleep_time))
            return paramiko.AUTH_FAILED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        command_text = str(command.decode("utf-8"))
        cf.info('client sent command via check_channel_exec_request ({}): {}'.
                format(self.client_ip, channel, command_text))
        return True


def handle_connection(client, addr):
    """Handle a new ssh connection"""
    logger.info("Got an connection from {} {}".format(client, addr))
    with suppress(Exception) as _:
        transport = paramiko.Transport(client)
        transport.banner_timeout = 3600
        transport.add_server_key(SSHServer.HOST_KEY)
        # Change banner to appear legit on nmap (or other network) scans
        transport.local_version = SSHServer.SSH_BANNER
        server = BasicSshHoneypot(addr[0], 1, 1 << 11)
        transport.start_server(server=server)

        logger.debug('Waiting for SSH auth...')
        chan = transport.accept(10)
        if chan:
            chan.close()
        transport.close()


def start_server(port, bind):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        logger.warning('Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        logger.info('Active threads: {}'.format(threading.active_count()))
        try:
            sock.listen(100)
            client, addr = sock.accept()
        except Exception as err:
            logger.error('Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection,
                                      args=(client, addr))
        new_thread.start()
        threads.append(new_thread)


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
