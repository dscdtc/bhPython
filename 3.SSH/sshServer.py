#!/usr/bin/env python
###__Author__ = "dscdtc"###
import os
import sys
import socket
import threading
import traceback
import subprocess
import paramiko

# Use Paramiko demo key
# host_key = paramiko.RSAKey(filename='test_rsa.key')

# Use private key under ~/.ssh_port
key_path = os.path.expanduser(os.path.join('~','.ssh','id_rsa'))
host_key = paramiko.RSAKey.from_private_key_file(key_path, password='dscdtc')

paramiko.util.log_to_file("ssh.log")

# Creat SSH tube
class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event() #
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if username == 'root' and password == 'toor':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])
# Start socket listening
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print '[+] Listening for connection ...'
    client, addr = sock.accept()
    print '[+] Got a connection!'
except Exception, e:
    print '[-] Listen failed: ' + e
    traceback.print_exc()
    sys.exit(1)

# Set up Authentication mode
try:
    sshSession = paramiko.Transport(client)
    sshSession.add_server_key(host_key)
    server = Server()
    try:
        sshSession.start_server(server = server)
    except paramiko.SSHException, e:
        print '[-] SSH negotiation failed:' + str(e)
        traceback.print_exc()
    chan = sshSession.accept(20)
    print '[+] Authenticated!'
    if conn.recv_ready():
        print chan.recv(1024)
        chan.send('Welcome to dscdtc\'s ssh')
    while True:
        try:
            command = raw_input('Enter command: ').strip('\n')
            if command is not 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting...'
                sshSession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            sshSession.close()
except Exception, e:
    print '[-] Caught exception: ' + str(e)
    traceback.print_exc()
    try:
        sshSession.close()
    except:
        pass
    sys.exit(1)
