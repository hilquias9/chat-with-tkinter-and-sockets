import socket
import threading

class Server():
    def __init__(self):
        self.clients=[]
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("172.16.2.27",7777))
        self.server.listen(1)
        print("Servidor Iniciado!")
        self.server.settimeout(1)
        try:
            while True:
                try:
                    client,addr=self.server.accept()
                except socket.timeout:
                    continue
                print(f"Client {addr} Conectado!")
                self.clients.append(client)
                thread=threading.Thread(target=self.messages_treatment,args=(client,),daemon=True)
                thread.start()
        except KeyboardInterrupt:
            for client in self.clients:
                    client.close()
                    self.clients.remove(client)
            self.server.close()
            print("Server encerrado!")
        
    def messages_treatment(self,client):
        print("Entrei no tratamento de mensagens!")
        while True:
            try:
                msg=client.recv(2048)
                if not msg:
                    break
                print(f"Mensagem recebida: {msg}")
                self.broadcast(msg,client)
            except Exception as error:
                print(f"Ocorreu um erro na messages_treatment, erro: {error}")
                break
        self.delete_client(client)

    def broadcast(self,msg,client):
        print("Broadcast iniciada!")
        for client_obj in self.clients:
            if client_obj!=client:
                try:
                    client_obj.send(msg)
                    print(f"Mensagem enviada ao client: {client.getpeername()[0]}")
                except Exception as error:
                    self.delete_client(client_obj)
                    print(f"Ocorreu um erro funcao broadcast, erro: {error}")

    def delete_client(self,client):
        print("Delete_client iniciada!")
        if client in self.clients:
            print(f"Usuario desconectado: {client.getpeername()[0]}")
            client.close()
            self.clients.remove(client)

server=Server()