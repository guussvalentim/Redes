from socket import *
import os


class PTATClient():
    
    serverPort = 12000
    serverName = '127.0.0.1'
    
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def nova_requisicao(self, req):
        lista_req = req.split()
        op = lista_req[0]
        
        match op:
            case 'read':
                # read path/filename 
                op = 0
                str_pathRemoto = lista_req[1]
            
                lista_path = str_pathRemoto.split("/")
            
                filename = lista_path.pop()
                path = "/".join(lista_path)
                body = ""
                length = 0

            case 'write':
                op = 1
            
                str_pathLocal = lista_req[1]

                
                with open(str_pathLocal, 'r') as file:
                   body = file.read()
                
                length = os.path.getsize(str_pathLocal)

                str_pathRemoto = lista_req[2]
                lista_pathRemoto = str_pathRemoto.split("/")
            
                filename = lista_pathRemoto.pop()
                path = "/".join(lista_path)


            case 'del':
                # del caminho_arquivo/nome_arquivo_remoto
                op = 2
                str_pathRemoto = lista_req[1]

                lista_pathRemoto = str_pathRemoto.split("/")
                
                filename = lista_pathRemoto.pop()
                path = "/".join(lista_path)

                length = 0
                body = ""

                # fazer length

            case 'list':
                # list caminho_remoto
                op = 3
                pathRemoto = lista_req[1]

                length = 0
                filename = ""
                body = ""

            case _:
                op = 4
                length = 0
                body = ""
                filename = ""
                path = ""

        self.op = op
        self.length = length
        self.filename = filename
        self.path = path
        self.body = body


    def enviar_requisicao(self):
        self.clientSocket.send(str(self.op).encode())
        self.clientSocket.send(str(self.length).encode())
        self.clientSocket.send(self.filename.encode())
        self.clientSocket.send(self.path.encode())
        self.clientSocket.send(self.body.encode())

    def recebe_respostas(self):
        self.op = self.clientSocket.recv(1).decode()
        self.length = self.clientSocket.recv(6).decode()
        self.filename = self.clientSocket.recv(64).decode()
        self.path = self.clientSocket.recv(128).decode()
        self.code = self.clientSocket.recv(1).decode()
        self.message = self.clientSocket.recv(128).decode()
        self.body = self.clientSocket.recv(self.length).decode()

def main():
        cliente = PTATClient()
        
        while True:

            req = input("Digite uma requisição: ")

            cliente.nova_requisicao(req)
            cliente.enviar_requisicao()
            cliente.recebe_respostas()

        cliente.clientSocket.close()