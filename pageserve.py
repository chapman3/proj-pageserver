"""
  David Chapman
  CIS399 Winter 2016
  Project 1
  Socket programming in Python
  as an illustration of the basic mechanisms of a web server.

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible. 

  FIXME:
  Currently this program always serves an ascii graphic of a cat.
  Change it to serve files if they end with .html and are in the current directory

  Currently pageserve.py runs on a local machine, then the user accesses https://localhost:(Port) to be served
  a webpage (trivia.html). When attempting to run it on ix, it simply initiates the server socket and listens.
  I have not been able to figure out how to connect to it on ix from a web browser.
"""

import socket  # Basic TCP/IP communication on the internet
import random  # To pick a port at random, giving us some chance to pick a port not in use
try:
    import thread
except ImportError:
    import _thread as thread #Py3K changed it.
    #  Response computation runs concurrently with main program
import sys

def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket

    try:
    #create an AF_INET, STREAM socket (TCP)
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print ('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit();

    print('Socket Created')
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)  # A real server would have multiple listeners
    return serversocket


def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        print("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept()
        _thread.start_new_thread(func, (clientsocket,))


def respond(sock):
    """
    Respond (only) to GET

    """

    sent = 0
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    print("\nRequest was {}\n".format(request))

    parts = request.split()
    if len(parts) > 1 and parts[0] == "GET":
        transmit("HTTP/1.0 200 OK\n\n", sock)
        try:
            file_handler = open("trivia.html")
            transmit(file_handler.read(), sock)
        except Exception as e:
            print("404 File Not Found")
            file_handler = \
                "<html>" \
                "<body>" \
                "<p>Error 404: File not found</p>" \
                "<p>Python HTTP server</p>" \
                "</body>" \
                "</html>"
            transmit(file_handler, sock)

    else:
        transmit("\nI don't handle this request: {}\n".format(request), sock)

    sock.close()

    return


def transmit(msg, sock):
    """It might take several sends to get the whole buffer out"""
    sent = 0
    while sent < len(msg):
        buff = bytes(msg[sent:], encoding="utf-8")
        sent += sock.send(buff)


def main():
    port = random.randint(5000,8000)
    sock = listen(port)
    print("Listening on port {}".format(port))
    print("Socket is {}".format(sock))
    serve(sock, respond)


main()
