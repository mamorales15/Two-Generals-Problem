# Two-Generals-Problem

An implementation of the two generals problem.
A server recieves UDP messages, randomly chooses whether to acknowledge them, and then acknowledge them if so.
A client sends a message to a server, waits for an acknowledgement, and may timeout if acknowledgement is not recieved within a set amount of time.

### How to use
To run the server:
~~~
$ python server.py
~~~

To run the client:
~~~
$ python client.py
~~~
