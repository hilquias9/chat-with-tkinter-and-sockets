import socket
import threading
import os

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
                if b"M3SAG3C0O%$D3" in msg:
                    self.broadcast(msg,client)
                elif b"f1l3n4m3c0d&" in msg:
                    self.receive_files(client,msg)

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

    def receive_files(self,client,file):
        file=file.decode()
        extract_file_name=file.split("f1l3n4m3c0d&")
        extract_file_name2=extract_file_name[1].split("3NDF1L3N4M3C0D&")
        file_name=extract_file_name2[0]
        extract_file_length=extract_file_name2[1].split("4R¢H1V3L£Nb")
        file_length=int(extract_file_length[0])
        print("Receive_files iniciada!")
        while True:
            try:
                if file_length==len(str(file)):
                    break
                lines=client.recv(2048)
                file=file+str(lines)
            except Exception as error:
                print(f"Ocorreu um erro na Receive_files: {error}")
                self.delete_client(client)
                break
        file_bytes=extract_file_length[1]
        path=os.getcwd()
        os.makedirs(name="downloads",exist_ok=True)
        with open(f"{path}\\downloads\\{file_name}","wb") as f:
            f.write(file_bytes.encode())
            print("Arquivo escrito!")
        print("Função receive_files encerrada!")

server=Server()