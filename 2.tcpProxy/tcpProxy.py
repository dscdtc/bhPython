#!/usr/bin/env python
###__Author__ = "dscdtc"###
import sys
import socket
import optparse
import threading

def server_loop(local_host, local_port, remote_host,
                remote_port, is_receive):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print '[!] Failed to listen on %s:%d' % (local_host, local_port)
        print '[!] Check for other listening sockets or correct permissions'
        sys.exit(0)

    print '[*] Listening on %s:%d' % (local_host, local_port)

    server.listen(5)

    while True:
        print '.',
        client_socket, addr = server.accept()

        # print out the local connection information
        print '[==>] Received incoming connection from %s:%d' % (
            addr[0], addr[1])
        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, is_receive)
        )

# this is a pretty hex dumping function directly taken from
# http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
    '''
    This version is unicode-aware, but makes no attempt to display characters outside the 7-bit printable ASCII range.
    _by George V. Reilly
    '''
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )

    print b'\n'.join(result)

def proxy_handler(client_socket, remote_host, remote_port, is_receive):

    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if is_receive:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our request handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to our local client send it
        if remote_buffer:
            print '[<==] Sending %d bytes to localhost.' % \
                len(remote_buffer)
            client_socket.send(remote_buffer)

	# now let's loop and reading from local, send to remote, send to local
	# rinse wash repeat
    while True:
        # read from local host
        local_buffer = receive_from(client_socket)
        if local_buffer:
            print '[==>] Received %d bytes from localhost.' % \
                len(local_buffer)
            hexdump(local_buffer)
            # send it to our request handler
            local_buffer = request_handler(local_buffer)
            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print '[==>] Sent to remote.'

        # receive back the response
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            print '[<==] Received %d bytes from remote.' % \
            len(remote_buffer)
            hexdump(remote_buffer)
            # send to our response handler
            remote_buffer = request_handler(remote_buffer)
            # send the response to the local socket
            remote_socket.send(remote_buffer)
            print '[<==] Sent to localhost.'

        # if no more data on either side close the connections
        if not local_buffer or not remote_buffer:
            client_socket.close()
            remote_socket.close()
            print '[*] No more data. Closing connections.'
            break

def receive_from(connection):
    buffer = ''
    connection.settimeout(2)
    try:
        # keep reading into the buffer until there's no more data
        # or we time out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

# modify any requests destined for the remote host
def request_handler(buffer):
	# perform packet modifications #
    return buffer

# modify any responses destined for the local host
def response_handler(buffer):
	# perform packet modifications #
    return buffer

def main():
    usage = "%prog -l <local host> -p <local port> " + \
    "-R <Remote host> -P <remote Port> [-r <recceive data first>]"
    example = '''\r\nExample:
    [Linux] sudo ./tcpProxy.py -l 127.0.0.1 -p 21 -R ftp.target.ca -P 21 -r
    [Windows] tcpProxy.py -l 127.0.0.1 -p 21 -R ftp.target.ca -P 21 -r
    '''
    parser = optparse.OptionParser(usage, version="%prog 1.0")  #d
    parser.add_option('-l', dest='local_host',
                      type='string', default='',
                      help='specify local host to listen on')   #s
    parser.add_option('-p', dest='local_port',
                      type='int', default=0,
                      help='specify local port to listen on')   #c
    parser.add_option('-R', dest='remote_host',
                      type='string', default='',
                      help='specify target host to listen on')  #d
    parser.add_option('-P', dest='remote_port',
                      type='int', default=0,
                      help='specify target port to listen on')  #t
    parser.add_option('-r', dest='is_receive',
                      action='store_true', default=False,
                      help='connect and receive data before '+\
                      'sending to the remote host')             #c

    (options, args) = parser.parse_args()

    local_host = options.local_host
    local_port = options.local_port
    remote_host = options.remote_host
    remote_port = options.remote_port
    is_receive = options.is_receive

    print "\r\nWelcome to dscdtc's <TCP Proxy Tool>\r\n"
    if local_host and local_port and remote_host and remote_port:
        server_loop(local_host, local_port,
                    remote_host, remote_port, is_receive)
    else:
        print parser.print_help()
        print example
        exit(0)

if __name__ == '__main__':
    __Author__ = "dscdtc"
    main()
