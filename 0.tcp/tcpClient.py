##!/usr/bin/env python
import socket

target_host = '0.0.0.0'#'www.bilibili.com'
target_port = 3732#80

# Creat a Socket object named 'client'
# AF_INET means we using IPv4 address or Host named
# SOCK_STREAM means this is a TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to target server
client.connect((target_host, target_port))

# Send message
#client.send('GET / HTTP/1.1\r\nHost: bilibili.com\r\n\r\n')
client.send('hello!!!')

# Receive message
response = client.recv(4096)

print response
