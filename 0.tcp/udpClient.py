##!/usr/bin/env python
import socket

target_host = '192.168.1.111'
target_port = 80

# Creat a Socket object named 'client'
# AF_INET means we using IPv4 address or Host named
# SOCK_DGRAM means this is a UDP client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send message
client.sendto('AAABBBCCC', (target_host, target_port))

# Receive message
adta, addr = client.recvfrom(4096)

print data, addr
