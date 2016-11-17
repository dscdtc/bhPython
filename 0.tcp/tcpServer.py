##!/usr/bin/env python
import socket
import threading

bind_ip = '192.168.1.181'
bind_port = 3732

# Creat a Socket object named 'server'
# AF_INET means we using IPv4 address or Host named
# SOCK_STREAM means this is a TCP client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify server ip and port to listen on
server.bind((bind_ip, bind_port))

# Set the max connection
server.listen(5)
print '[*] Listen on %s:%d' % (bind_ip, bind_port)

# This is client handle procsee
def handle_client(client_socket):

    # print client send message
    request = client_socket.recv(1024)
    print "[*] Received: %s" % request

    # return a packet
    client_socket.send('ACK!')
    client_socket.close()

while True:

    client, addr = server.accept()

    print '[*] Accepted connection from: %s:%d' % \
        (addr[0], addr[1])

    # Handle received message
    client_handler = threading.Thread(target=handle_client, \
                                      args=(client,))
    client_handler.start()
