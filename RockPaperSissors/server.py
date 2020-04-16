import pickle
import socket
from _thread import *
from RockPaperSissors.network import SERVER
from RockPaperSissors.network import PORT

from RockPaperSissors.game import Game
from Version2.player import Player

server = SERVER
port = PORT

# Store the IP addresses of the clients
connected = set()
# Disctionary: Id as key Game object as value
games = {}
# Id of the games, so is possible to have several games
idCount = 0


def threaded_client(connection, player, gameId):
    global idCount, games
    connection.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = connection.recv(4096).decode()
            if gameId in games and data:
                game = games[gameId]

                if data == "reset":
                    game.resetWent()

                elif data != "get": # Move
                    game.play(player, data)

                reply = game
                connection.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("Lost connection")
    print("Closing game: ", gameId)
    try:
        del games[gameId]
    except:
        pass
    connection.close()



# AF_INET -> ipv4, SOCK_STREAM -> TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    str(err)

# numero de peticiones que acepta
s.listen()
print("Waiting for a connection. Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(50, 50, 50, 50, (0, 255, 0))]


while True:
    # Blocks until connection
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    currentPlayer = 0
    gameId = (idCount - 1) // 2 # 2 people for 1 game

    # For the odd connections 1, 3, 5... we need to create a new game. Even connects to already created game
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating new game id: ", gameId)
    else:
        games[gameId].ready = True
        currentPlayer = 1

    start_new_thread(threaded_client, (conn, currentPlayer, gameId))
