from socket import *
import os
import datetime


class PTATServer():
    host = '127.0.0.1'
    serverPort = 12000

    def __init__(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.serverPort))
        self.serverSocket.listen(1)


    def realiza_requisicao(self):
        match(self.op):
            case '0':
                # read
                caminho_arq = str(self.path + "\\" + self.filename)

                try:
                    with open(caminho_arq, 'r') as file:
                        
                        self.length = os.path.getsize(caminho_arq)
                        self.body = file.read()

                        self.code = 0
                        self.message = "Arquivo lido com sucesso"
                
                except FileNotFoundError:
                    self.length = 1  
                    self.code = 2      
                    self.body = "."
                    self.message = "Nome de arquivo não existente no servidor"
                    raise


            case '1':
                # write
                caminho_arq = str(self.path + "\\" + self.filename)

                try:
                    with open(caminho_arq, 'w') as file:
                        file.write(self.body)
                except FileNotFoundError:
                    self.length = 1
                    self.code = 1
                    self.message = "Caminho não existente no servidor"
                    self.body = "."
                    raise

            case '2':
                # delete
                caminho_arq = str(self.path + self.filename)
                
                try:
                    os.remove(caminho_arq)

                except FileNotFoundError:
                    self.length = 1
                    self.code = 1
                    self.message = "Caminho não existente no servidor"
                    self.body = ""
                    raise

            case '3':
                # list
                diretorio = self.path
                try:
                    arquivos_diretorio = os.listdir(diretorio)
                    
                    for arquivo in arquivos_diretorio:
                        body = body + "\n" + arquivo
                    
                except FileNotFoundError:
                    self.length = 1
                    self.code = 1
                    self.message = "Caminho não existente no servidor"
                    self.body = ""
                    raise
                    

            case _:
                self.length = 1
                self.code = 4
                self.message = "Operação inválida"
                self.body = "."

        horario = datetime.datetime.now().strftime("%H:%M:%S")

        return f"{horario}, {self.op}, {self.path}, {self.code}"

    def enviar_resposta(self):
        string_resposta = f"{op},{}"
        
        self.connectionSocket.send(str(self.op).encode())
        self.connectionSocket.send(str(self.length).encode())
        self.connectionSocket.send(str(self.filename).encode())
        self.connectionSocket.send(str(self.path).encode())
        self.connectionSocket.send(str(self.code).encode())
        self.connectionSocket.send(str(self.message).encode())
        self.connectionSocket.send(str(self.body).encode())

    def aguarda_requisicao(self):
        while True:
            self.connectionSocket, self.addr = self.serverSocket.accept()

            try:
                self.recebe_requisicao()
                log = self.realiza_requisicao()
                self.enviar_resposta()

                yield log

            except BufferError:
                self.code = 3
                self.message = "Tamanho do arquivo para ser escrito maior que tamanho máximo permitido"

            self.connectionSocket.close()

    def recebe_requisicao(self):   
        string_recebida = self.connectionSocket.recv(1000000000).decode()

        print(string_recebida)

        self.op, self.length, self.filename, self.path, self.body = string_recebida.split(",")

        

        print(f"op = {self.op}, length = {self.length}, filename = {self.filename}, path = {self.path}, body = {self.body}")
               


def main():
    server = PTATServer()

    print("Server aberto")

    for log in server.aguarda_requisicao():
        print(log)

        

main()
        
