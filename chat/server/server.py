import socket
import threading
import os

class Server():
    def __init__(self):
        hostname=socket.gethostname()
        private_ipv4=socket.gethostbyname(hostname)
        self.clients=[]
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((private_ipv4,7777))
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
        header_extracter=msg.split(b"M3SAG3C0O%$D3")[1]
        len_extracter=header_extracter.split(b"M33SS4GL3N")[0]
        len_msg=len(msg)
        print("Tamanho da mensagem: ", len_extracter)
        print("Tamanho esperado: ",len_msg)
        data_collector=b""
        if int(len_extracter.decode())>len_msg:
            print("Len extracter menor, entrei no while")
            while True:
                data=client.recv(2048)
                if not data: break
                len_msg=len_msg+len(data)
                data_collector+=data
                if len_msg==int(len_extracter.decode()):break
        message=msg+data_collector
        print("Broadcast iniciada!")
        print(f"Len da mensagem que chegou no servidor: {len_extracter}")
        print(f"Usuario: {client.getpeername()[0]} Mensagem recebida")
        for client_obj in self.clients:
            if client_obj!=client:
                try:
                    client_obj.sendall(message)
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
        print("Receive_files iniciada!")
        extract_file_name=file.split(b"f1l3n4m3c0d&")
        extract_file_name2=extract_file_name[1].split(b"3NDF1L3N4M3C0D&")
        file_name=extract_file_name2[0].decode()
        extract_file_length=extract_file_name2[1].split(b"4RKH1V3L3N")
        file_length=int(extract_file_length[0].decode())
        file_bytes=extract_file_length[1]
        total=len(file)
        print("Nome do arquivo: ",file_name)
        print("Cliente: ",client.getpeername()[0])
        print("Tamanho esperado: ",file_length)
        print("Tamanho até o momento: ",len(file))
        while True:
            try:
                if file_length==total:
                    break
                lines=client.recv(2048)
                if not lines:
                    break
                file_bytes=file_bytes+lines
                total=total+len(lines)
            except Exception as error:
                print(f"Ocorreu um erro na Receive_files: {error}")
                self.delete_client(client)
                break
        path=os.getcwd()
        complete_path=f"{path}\\downloads\\{file_name}"
        os.makedirs(name="downloads",exist_ok=True)
        with open(complete_path,"wb") as f:
            f.write(file_bytes.split(b"3NDF1L3N4M3C0D&")[0])
            print("Arquivo escrito!")
        print("Função receive_files encerrada!")
        self.send_files(client,complete_path,file_name)

    def send_files(self,client,path,filename):
        print("Função send_file iniciada!")
        file=b"f1l3n4m3c0d&"+filename.encode()+b"3NDF1L3N4M3C0D&"
        with open(path,"rb") as f:
            lines=f.read()
            print("Len de lines: ",len(lines))
            lines=lines+b"3NDF1L3N4M3C0D&"
        file_length=len(lines)+len(file)+len("4RKH1V3L3N")
        file_length=file_length+len(str(file_length))
        file=file+str(file_length).encode()+b"4RKH1V3L3N"+lines
        for client_obj in self.clients:
            if client_obj!=client:
                client_obj.sendall(file)
                print(f"Arquivo: {filename} {file_length} enviado com sucesso ao cliente {client_obj.getpeername()[0]}")

server=Server()