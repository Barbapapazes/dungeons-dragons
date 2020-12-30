from server.network import Network
import socket            # Import socket module

s = Network()        # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 3000                # Reserve a port for your service.

print(s.connect())
