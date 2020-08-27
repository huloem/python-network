#!/usr/bin/python3

import socket
import threading

bind_ip   = "127.0.0.1"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((bind_ip, bind_port))
print("[*] Waiting\t%s:%d" % (bind_ip,bind_port))

while True:
    data,addr = server.recvfrom(4096)
    print("[*] From\t%s:%d" % (addr[0],addr[1]))
    print("[*] Recerved\t%s" % data.decode('ascii'))
    server.sendto(b'UDP server\'s responce data', (addr[0], addr[1]))