from socket import *


class PTATServer():
    host = '127.0.0.1'
    serverPort = 12000

    def __init__(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.serverPort))
        self.serverSocket.listen(1)
