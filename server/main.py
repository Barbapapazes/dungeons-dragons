import socket
import pickle
from server.settings import SERVER_IP, SERVER_PORT
from logger import logger

# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# try to connect to server
try:
    S.bind((SERVER_IP, SERVER_PORT))
except socket.error as e:
    logger.exception(e)
    quit()

# listen for connections
S.listen()
logger.info("Server started, %s", SERVER_IP)

# dynamic variables
players = {}
connections = 0
_id = 0


def threaded_client(conn, _id):
    global connections, players

    # setup properties for each new player
    current_id = _id
    players[current_id] = {
        "pos": {
            "x": 300,
            "y": 300
        },
        "vel": {
            "x": 0,
            "y": 0
        },
    }

    # pickle data and send initial info to clients
    conn.send(str.encode(str(current_id)))

    while True:
        try:
            # receive data from client
            data = conn.recv(32)

            if not data:
                break

            data = data.decode("utf-8")
            # logger.info("Data received: %s", data)

            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                pos_x = int(split_data[1])
                pos_y = int(split_data[2])
                players[current_id]["pos"]["x"] = pos_x
                players[current_id]["pos"]["y"] = pos_y
                vel_x = int(split_data[3])
                vel_y = int(split_data[4])
                players[current_id]["vel"]["x"] = vel_x
                players[current_id]["vel"]["y"] = vel_y

                send_data = pickle.dumps((players))

            if data.split(" ")[0] == "get":
                send_data = pickle.dumps((players))

            conn.send(send_data)

            # else:
            #     # print(data)

            #     conn.sendall(pickle.dumps(data))
        except Exception as e:
            logger.exception(e)
            break

    logger.info("Client %s disconnected", current_id)

    # client disconected
    connections -= 1
    del players[current_id]
    conn.close()
