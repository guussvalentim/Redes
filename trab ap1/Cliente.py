from socket import *


class PTATClient():
    
    serverPort = 12000
    serverName = '127.0.0.1'
    
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def read(nome_arq):
        arq = open(nome_arq, 'r')
        arq




    def main():
        while True:

        
