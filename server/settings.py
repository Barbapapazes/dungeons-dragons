"""Settings for the server"""
import socket
import os

# HOST_NAME = socket.gethostname()
# SERVER_IP = socket.gethostbyname(HOST_NAME)
# SERVER_IP = "192.168.43.206"
# avec le téléphone, ça ne semble pas marcher, on va donc falloir le faire sur le wifi mais regarder comment faire pour que ça fonctionne en 4g
SERVER_IP = socket.gethostname() if os.getenv("SERVER_IP") is None else os.getenv("SERVER_IP")
SERVER_PORT = 3000
