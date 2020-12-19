"""Start the server"""
from server.main import threaded_client, S, _id, connections
from _thread import start_new_thread
from logger import logger

if __name__ == '__main__':
    while True:
        conn, addr = S.accept()
        logger.info("Connexion : %s | Address:  %s", conn, addr)

        connections += 1
        start_new_thread(threaded_client, (conn, _id))
        _id += 1
