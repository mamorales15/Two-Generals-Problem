# udp server that will receive a message, randomly decide whether to drop the message, and send back an acknowledge if not
import sys, random
from socket import *
from select import select

# DEFAULT PARAMS
serverAddr = ("",50000) # any addr, port 50,000
maxSize = 2048 # max size of message willing to recieve
dropRate = 0.3 # percentage of packets dropped (0.1 = 10%, 0.5 = 50%)
timeout = 10 # seconds

def receiveMssg(sock):
    message, clientAddrPort = sock.recvfrom(maxSize)
    print "From %s, data recieved: %s" % (repr(clientAddrPort), message)

    if random.random() > dropRate:
        ackMssg = "Ack: message recieved"
        sock.sendto(ackMssg, clientAddrPort)
        print "Message transfer completed"
    else:
        print "ERR: Message dropped"

# SET UP SERVER
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
serverSocket.setblocking(False)

readSockFunc = {} # dictionaries from socket to function
writeSockFunc = {}
errorSockFunc = {}

readSockFunc[serverSocket] = receiveMssg

print "Server started"
while 1:
    readRdySet, writeRdySet, errorRdySet = select(readSockFunc.keys(),
                                                  writeSockFunc.keys(),
                                                  errorSockFunc.keys(),
                                                  timeout)
    if not readRdySet and not writeRdySet and not errorRdySet:
        print "Timeout: no events"

    for sock in readRdySet:
        readSockFunc[sock](sock)
