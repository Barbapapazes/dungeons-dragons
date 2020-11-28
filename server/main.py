import socket
import pickle
from server.settings import SERVER_IP, SERVER_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((SERVER_IP, SERVER_PORT))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for connection, Start Server")


def close():
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    print("closed")


player = (2, 3)


def threaded_client(conn):
    conn.send(pickle.dumps(player))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                break
            else:
                # print(data)

                conn.sendall(pickle.dumps(data))
        except BaseException:
            break

    print("Lost connection")
    print("Closing Game")
    conn.close()
