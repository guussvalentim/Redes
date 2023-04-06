from socket import *


class PTATClient():
    
    serverPort = 12000
    serverName = '127.0.0.1'
    
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def nova_requisicao(req):
        lista_req = req.split()
        op = lista_req[0]
        
        
        if(op == 'read'):
            # read path/filename 
            op = 0
            str_pathRemoto = lista_req[1]
            
            lista_path = str_pathRemoto.split("/")
            
            filename = lista_path.pop()
            
            path = "/".join(lista_path)


            
            body = ""



        elif(op == 'write'):
            # write path/filename_local path/filename_server
            op = 1
            
            str_pathLocal = lista_req[1]
            lista_pathLocal = str_pathLocal.split("/")
            
            filenameLocal = lista_pathLocal.pop()
            pathLocal = "/".join(lista_path)

            str_pathRemoto = lista_req[2]
            lista_pathRemoto = str_pathRemoto.split("/")
            
            filenameRemoto = lista_pathRemoto.pop()
            pathRemoto = "/".join(lista_path)

            # fazer length



        elif(op == 'del'):
            # del caminho_arquivo/nome_arquivo_remoto
            op = 2
            str_pathRemoto = lista_req[1]

            lista_pathRemoto = str_pathRemoto.split("/")
            filenameRemoto = lista_pathRemoto.pop()
            pathRemoto = "/".join(lista_path)

            # fazer length


        elif(op == 'list'):
            # list caminho_remoto
            op = 3
            pathRemoto = lista_req[1]


        else:
            op = -1
            #





    def main():
        while True:
