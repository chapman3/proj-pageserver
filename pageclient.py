import socket
import sys

def connect(sock, port):
    host = 'localhost'
    try:
        sock.connect((host, port))
        print("connected")
    except Exception as e:
        print("no connection")
        sys.exit()

    return

def receive(sock):
    sock.recv(1024)
    return

def main():
    sock = socket.socket()
    port = 5000
    connect(sock, port)
    print(receive(sock))

main()
