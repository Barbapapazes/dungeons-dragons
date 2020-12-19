import socket
import pickle
from logger import logger
from config.server import SERVER_IP, SERVER_PORT


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = SERVER_IP
        self.port = SERVER_PORT
        self.addr = (self.host, self.port)

    def connect(self):
        """
        connects to server and returns the id of the client that connected
        :return: int representing id
        """
        self.client.connect(self.addr)
        val = self.client.recv(8)
        return int(val.decode())  # can be int because will be an int id

    def disconnect(self):
        """
        disconnects from the server
        :return: None
        """
        self.client.close()

    def send(self, data, pick=False):
        """
        sends information to the server

        :param data: str
        :param pick: boolean if should pickle or not
        :return: str
        """
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(2048*4)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                logger.exception(e)

            return reply
        except socket.error as e:
            logger.exception(e)
