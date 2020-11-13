import socket
from _thread import *
from settings import SERVER_IP, SERVER_PORT

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


def threaded_client(conn):
    conn.send(str.encode('connected to the server'))

    while True:
        try:
            data = conn.recv(2048).decode()

            if not data:
                break
            else:
                print(data)
        except BaseException:
            break

    print("Lost connection")
    print("Closing Game")
    conn.close()


if __name__ == '__main__':
    while True:
        # close()
        try:
            conn, addr = s.accept()
            print(conn, addr)

            start_new_thread(threaded_client, (conn, ))

        except KeyboardInterrupt:
            print("[!] Keyboard Interrupted!")
            close()
            break
