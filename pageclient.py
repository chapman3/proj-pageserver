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


def transmit(msg, sock):
    sock.send(msg)
    return


def receive(sock):
    str(sock.recv(1024), 'UTF-8')
    print('received data')
    return


def main():
    sock = socket.socket()
    port = 5001
    connect(sock, port)
    transmit(bytes('GET /trivia.html', encoding='utf-8'), sock)
    receive(sock)


main()
