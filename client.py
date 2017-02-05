#! /bin/python
# udp client that will send a message to a server, and wait for acknowledgement or timeout
import sys, re
from socket import *
from select import select

# DEFAULT PARAMS
serverAddr = ('localhost', 50000)
clientAddr = ("", 40000)
maxSize = 2048 # max size of message willing to recieve
ackTimeout = 10 # seconds

def errorMssg():
    print "ERR: usage: %s [--serverAddr host:port]" % sys.argv[0]
    sys.exit(1)

def recvAck(sock):
    serverMssg, serverAddrPort = clientSocket.recvfrom(maxSize)
    print "Server at %s says: '%s'" % (repr(serverAddrPort), serverMssg)
    print "Message transfer completed"

# HANDLE ARGS
try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        else:
            print "ERR: unexpected parameter %s" % args[0]
            errorMssg()
except:
    errorMssg()

print "serverAddr = %s" % repr(serverAddr)

# SET UP CLIENT, SEND MSSG
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(clientAddr)
clientSocket.setblocking(False)
readSockFunc = {}
writeSockFunc = {}
errorSockFunc = {}

readSockFunc[clientSocket] = recvAck

# SEND MESSAGE TO SERVER
print "Input message to send to server:"
message = sys.stdin.readline()[:-1] # [:-1] -> delete final \n
clientSocket.sendto(message, serverAddr)

# RECIEVE ACK OR TIMEOUT
readRdySet, writeRdySet, errorRdySet = select(readSockFunc.keys(),
                                                  writeSockFunc.keys(),
                                                  errorSockFunc.keys(),
                                                  ackTimeout)
if not readRdySet and not writeRdySet and not errorRdySet:
    print "Timeout: no acknowledgement given"

for sock in readRdySet:
    readSockFunc[sock](sock)
    
