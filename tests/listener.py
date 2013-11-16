# Adafruit CC3000 Library Test Listener
# Created by Tony DiCola (tony@tonydicola.com)
# Released with the same license as the Adafruit CC3000 library (BSD)

# Create a simple server to listen by default on port 9000, accept any connections 
# and print all data received to standard output.  Can optionally echo received 
# data to the connected client.  Run at command line with -h option to see available 
# arguments.  Must be terminated by hitting ctrl-c to kill the process!

import argparse
from socket import *
import sys
import threading

# Parse command line parameters
parser = argparse.ArgumentParser(description='Adafruit CC3000 Library Test Listener')
parser.add_argument('-p', '--port', dest='port', type=int, default=9000, 
					help='port for listening for TCP connections')
parser.add_argument('-e', '--echo', dest='echo', action='store_true', default=False, 
					help='echo the data received back out to the client')
args = parser.parse_args()

# Create listening socket
server = socket(AF_INET, SOCK_STREAM)

# Ignore waiting for the socket to close if it's already open.  See the python socket
# doc for more info (very bottom of http://docs.python.org/2/library/socket.html).
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Listen on any network interface for the specified port
server.bind(('', args.port))
server.listen(5)

# Worker process to print all data received to standard output.
def process_connection(client):
	while True:
		data = client.recv(1024)
		if not data: 
			break
		sys.stdout.write(data) # Don't use print because it appends spaces and newlines
		sys.stdout.flush()
		if args.echo:
			client.send(data)
	client.close()

try:
	# Wait for connections and spawn worker threads to process them.
	while True:
		client, address = server.accept()
		thread = threading.Thread(target=process_connection, args=(client,))
		thread.setDaemon(True)
		thread.start()
except:
	server.close()