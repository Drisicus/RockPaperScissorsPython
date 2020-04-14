import socket
from _thread import *
import sys

def readPosition(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def makePosition(tupple):
    return str(tupple[0]) + "," + str(tupple[1])

def threaded_client(conn, player):
    conn.send(str.encode(makePosition(positions[player])))
    reply = ""
    connectionStablish = True
    while connectionStablish:
        try:
            data = readPosition(conn.recv(2048).decode("utf-8"))
            positions[player] = data

            if not data:
                print("Disconnected")
                connectionStablish = False
            else:
                if player == 1:
                    reply = positions[0]
                else:
                    reply = positions[1]

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(makePosition(reply)))
        except:
            connectionStablish = False
            pass
    print("Lost connection")
    conn.close()


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

# posicion de player 1 y 2
positions = [(0, 0), (100, 100)]

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1