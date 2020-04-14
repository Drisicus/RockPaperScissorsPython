import pickle
import socket
from _thread import *

from Version2.player import Player


def threaded_client(connection, player):
    connection.send(pickle.dumps(players[player]))
    reply = ""
    connectionStablish = True
    while connectionStablish:
        try:
            data = pickle.loads(connection.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                connectionStablish = False
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending: ", reply)

            connection.sendall(pickle.dumps(reply))
        except:
            connectionStablish = False
            pass
    print("Lost connection")
    connection.close()


server = "192.168.1.37"
port = 5555

# AF_INET -> ipv4, SOCK_STREAM -> TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    str(err)

# numero de peticiones que acepta
s.listen(2)
print("Waiting for a connection. Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(50, 50, 50, 50, (0, 255, 0))]

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
