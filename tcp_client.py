#!/usr/bin/python3

import socket

target_host = "127.0.0.1"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send(b'Client\'s send data')
response = client.recv(1024)

print(response.decode('ascii'))