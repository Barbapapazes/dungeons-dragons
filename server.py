"""Start the server"""
from server.main import close, threaded_client, s
from _thread import start_new_thread

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
