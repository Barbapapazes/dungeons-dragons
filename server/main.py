from config.sprites import PLAYER_HIT_RECT
import pickle
import socket

from logger import logger

from server.settings import SERVER_IP, SERVER_PORT

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
players = dict()
arrows = dict()
arrows_id = 0
connections = 0
_id = 0


def check_collisions():
    # on utilise le hit rect du player dans le sprite config et on check à une collision avec un point (la position de la flèche, faudra lui faire une hitbox dans la config), il faut checker si le owner de la flèche est différente du current_id alors on remove de la vie
    # ou alors on le fait dans le client si c'est une flèche qui lui appartient (c'est un peu relou)
    try:
        for key, value_arrow in arrows.items():
            for key, value_player in players.items():
                hit_rect = PLAYER_HIT_RECT.copy()
                hit_rect.center = (float(value_player["pos"]["x"]), float(value_player["pos"]["y"]))
                # logger.debug("%s, %s, %s", hit_rect, value_arrow["pos"]["x"], value_arrow["pos"]["y"])
                if hit_rect.collidepoint((float(value_arrow["pos"]["x"]), float(value_arrow["pos"]["y"]))):
                    # si on touche, alors il faut delete la flèche et remove de la  vie à la personne touchée
                    logger.debug("touch")
    except:
        logger.error("erreur dans les collisions")


def threaded_client(conn, _id):
    global connections, players, arrows, arrows_id

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
            data = conn.recv(64)

            if not data:
                break

            data = data.decode("utf-8")
            # logger.info("Data received: %s", data)
            send_data = pickle.dumps(None)

            check_collisions()

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

                send_data = pickle.dumps((players, arrows))

            if data.split(" ")[0] == "arrow":

                if data.split(" ")[1] == "remove":
                    split_data = data.split(" ")
                    id = split_data[2]
                    player_id = split_data[3]
                    if int(id) in arrows.keys() and arrows[int(id)]["player_id"] == player_id:
                        del arrows[int(id)]

                    # logger.debug(
                        # "il faut checker que c'est bien le owner qui veut la delete, et on le check dans le client directement, si c'set le joueur qui la détient qui veut la delete, alors on supprime")
                elif data.split(" ")[1] == "update":
                    split_data = data.split(" ")
                    id = split_data[2]
                    pos_x = split_data[3]
                    pos_y = split_data[4]
                    logger.debug("update")
                    arrows[int(id)]["pos"] = {
                        "x": float(pos_x),
                        "y": float(pos_y),
                    }

                else:
                    split_data = data.split(" ")
                    logger.debug(split_data)
                    pos_x = split_data[1]
                    pos_y = split_data[2]
                    dir_x = split_data[3]
                    dir_y = split_data[4]
                    damage = split_data[5]
                    _id = split_data[6]

                    arrows[arrows_id] = {
                        "pos": {
                            "x": pos_x,
                            "y": pos_y
                        },
                        "dir": {
                            "x": dir_x,
                            "y": dir_y
                        },
                        "damage": damage,
                        "player_id": _id
                    }

                    arrows_id += 1

                logger.debug(arrows)

            if data.split(" ")[0] == "get":
                send_data = pickle.dumps((players, arrows))

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
