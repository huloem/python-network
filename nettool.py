#!/usr/bin/python3

import sys
import socket
import getopt
import threading
import subprocess
import signal

listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(
                target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    try:
        output = subprocess.check_output(
                command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = b'Failed to execute command.\r\n'
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = b''
        while True:
            data = client_socket.recv(1024)
            if len(data) == 0:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            client_socket.send("Successfully saved file".encode('utf-8'))
        except:
            client_socket.send("Failed to save file".encode('utf-8'))
    if len(execute):
        output1 = run_command(execute)
        client_socket.send(output1)
    if command:
        while True:
            cmd_buffer = ""
            cmd_buffer += client_socket.recv(1024).decode('utf-8')
            output2 = run_command(cmd_buffer)
            client_socket.send(output2)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode('utf-8'))
        while True:
            recv_len = 1
            response = b''
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print(response.decode('utf-8'))
            buffer = input()
            if buffer == "quit":
                client.send(buffer.encode('utf-8'))
                break
            client.send(buffer.encode('utf-8'))
    except:
        print("[*] Exception! Exiting.")
        client.close()

def usage():
    print("Net Tool")
    print("client:  ./nettool.py -t server_host -p port")
    print("server:  ./nettool.py -l [-t client_host] -p port")
    print("options:")
    print("     -c                     exec shell")
    print("     -e program             exec program")
    print("     -h                     help")
    print("     -l                     listen mode")
    print("     -u filename            upload destination filename")
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # parse command line option
    try:
        opts, args = getopt.getopt(
                sys.argv[1:],
                "hle:t:p:cu:")
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o == "-h":
            usage()
        elif o == "-l":
            listen = True
        elif o == "-e":
            execute = a
        elif o == "-c":
            command = True
        elif o == "-u":
            upload_destination = a
        elif o == "-t":
            target = a
        elif o == "-p":
            port = int(a)
        else:
            assert False, "Unhandled option"

    # listen? or send data received from stdin?
    if not listen and len(target) and port > 0:
        buffer = input()
        client_sender(buffer)

    # listen
    if listen:
        server_loop()

main()