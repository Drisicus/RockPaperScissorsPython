import socket
import pickle

SERVER = "192.168.1.58"
PORT = 5555

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def getPlayer(self):
        return self.player

    ''' Connect and get player number - 0 or 1'''
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 4))
        except socket.error as err:
            print(err)
