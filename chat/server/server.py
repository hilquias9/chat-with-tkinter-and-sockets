import socket
import threading
import os
import random

class Server():
    def __init__(self):
        hostname=socket.gethostname()
        private_ipv4=socket.gethostbyname(hostname)
        self.clients={}
        self.nicknames=[]
        self.number_of_clients=0
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
                self.clients[self.number_of_clients]={"client":client,"username_past":[]}
                self.number_of_clients+=1
                thread=threading.Thread(target=self.messages_treatment,args=(client,),daemon=True)
                thread.start()
        except KeyboardInterrupt:
            for index in self.clients.keys():
                    if self.clients[index]["client"]==client:
                        client.close()
                        self.clients.pop(index)
            self.server.close()
            print("Server encerrado!")
        
    def messages_treatment(self,client):
        while True:
            try:
                msg=client.recv(2048)
                if not msg:
                    break
                if b"M3SAG3C0O%$D3" in msg:
                    self.broadcast(msg,client)
                elif b"f1l3n4m3c0d&" in msg:
                    self.receive_files(client,msg)
                elif b"S3NDdUS3N4M3!" in msg:
                    self.receive_username(client,msg)
                elif b"SERV3R_S3ND_F1LEC0OOODE3" in msg:
                    self.send_files(client,msg)

            except Exception as error:
                print(f"Ocorreu um erro na messages_treatment, erro: {error}")
                break
        self.delete_client(client)

    def broadcast(self,msg,client):
        header_extracter=msg.split(b"M3SAG3C0O%$D3")[1]
        len_extracter=header_extracter.split(b"M33SS4GL3N")[0]
        len_msg=len(msg)
        data_collector=b""
        if int(len_extracter.decode())>len_msg:
            while True:
                data=client.recv(2048)
                if not data: break
                len_msg=len_msg+len(data)
                data_collector+=data
                if len_msg==int(len_extracter.decode()):break
        message=msg+data_collector
        for index in self.clients.keys():
            if self.clients[index]["client"]!=client:
                try:
                    self.clients[index]["client"].sendall(message)
                except Exception as error:
                    self.delete_client(self.clients[index])
                    print(f"Ocorreu um erro funcao broadcast, erro: {error}")


    def delete_client(self,client):
        for index in self.clients.keys():
            if self.clients[index]["client"]==client:
                client.close()
                self.clients.pop(index) 
                break
                


    def receive_files(self,client,file):
        extract_file_name=file.split(b"f1l3n4m3c0d&")
        extract_file_name2=extract_file_name[1].split(b"3NDF1L3N4M3C0D&")
        file_name=extract_file_name2[0].decode()
        extract_file_length=extract_file_name2[1].split(b"4RKH1V3L3N")
        file_length=int(extract_file_length[0].decode())
        file_bytes=extract_file_length[1]
        total=len(file)
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
        msg=Server_msgs.file_msg(self.clients,client,file_name)
        self.send_msg(client=client,msg=msg)
        

    def send_files(self,client,msg):
        filename=msg.split(b"SERV3R_S3ND_F1LEC0OOODE3")[1]
        filename=filename.decode()
        path=os.getcwd()
        complete_path=f"{path}\\downloads\\{filename}"
        file=b"f1l3n4m3c0d&"+filename.encode()+b"3NDF1L3N4M3C0D&"
        with open(complete_path,"rb") as f:
            lines=f.read()
            lines=lines+b"3NDF1L3N4M3C0D&"
        file_length=len(lines)+len(file)+len("4RKH1V3L3N")
        file_length=file_length+len(str(file_length))
        file=file+str(file_length).encode()+b"4RKH1V3L3N"+lines
        for index in self.clients.keys():
            if self.clients[index]["client"]!=client:
                self.clients[index]["client"].sendall(file)
                
    
    def receive_username(self,client,msg):
        username=msg.split(b"S3NDdUS3N4M3!")[1]
        for index in self.clients.keys():
            if self.clients[index]["client"]==client:
                if username.decode() not in self.nicknames:
                    self.clients[index]["actual_username"]=username.decode()
                    self.clients[index]["username_past"].append(username.decode())
                    self.nicknames.append(username.decode())
                    if len(self.clients[index]["username_past"])>1:
                        self.send_username_2_everyone(index)
                    else:
                        welcome_msg=Server_msgs.welcome_msg(self.clients[index]["actual_username"])
                        self.send_msg_2_everyone(welcome_msg)
                    break
                else:
                    while True:
                        nickname=username.decode()+str(random.randint(0,100))
                        if nickname not in self.nicknames:
                            self.clients[index]["actual_username"]=nickname
                            self.clients[index]["username_past"].append(nickname)
                            self.nicknames.append(nickname)
                            msg=Server_msgs.server_force_username(nickname)
                            client.send(msg)
                            if len(self.clients[index]["username_past"])>1:
                                self.send_username_2_everyone(index) 
                                print("PRECISEI ENTRAR NO IF")
                            else:
                                welcome_msg=Server_msgs.welcome_msg(self.clients[index]["actual_username"])
                                self.send_msg_2_everyone(welcome_msg)
                            break
        

    
    def send_msg(self,client,msg):
        #this function send a msg to everyone less the client who call the function
        for index in self.clients.keys():
                if self.clients[index]["client"]!=client:
                    try:
                        self.clients[index]["client"].send(msg)
                    except Exception as error:
                        self.delete_client(self.clients[index]["client"])
                        print("Ocorreu um erro ao enviar o nome do arquivo na função server_msg: ",error)

    def send_msg_2_everyone(self,msg):
        #this function send a message to everyone in the chat
        for index in self.clients.keys():
            try:
                self.clients[index]["client"].send(msg)
            except Exception as error:
                self.delete_client(self.clients[index]["client"])
                print("Ocorreu um erro ao utilizar a função send_msg_2_everyone: ",error)
    
    def send_username_2_everyone(self,index):
        try:
            print("FUNÇÃO SEND_USERNAME_2_EVERYONE INICIADA")
            new_username=self.clients[index]["actual_username"]
            old_username=self.clients[index]["username_past"][-2]
            msg=Server_msgs.send_username_2_everyone(old_username,new_username)
            print("Mensagem que vai ser enviada: ",msg)
            self.send_msg_2_everyone(msg)
            print("Função finalizada!")
        except Exception as error:
            print("Ocorreu um erro ao usar a função send_username_2_everyone: ",error)

    
class Server_msgs():
    def find_client(clients:dict,client):
        try:
            for index in clients.keys():
                    if clients[index]["client"]==client:
                        return index
        except Exception as error:
            print("Aconteceu um erro ao usar a funcao find_client da classe Server_msgs: ",error)


    def file_msg(clients:dict,client,filename:str):
        try:
            index=Server_msgs.find_client(clients,client)
            msg=b"S3RV3RF1iL3C0D3"+clients[index]["actual_username"].encode()+b"US3ERN4AM3EC0D3E"+filename.encode()
            return msg
        except Exception as error:
            print("Aconteceu um erro ao usar a funcao file_msg da classe Server_msgs: ",error)
    

    def server_force_username(username):
        msg=b"S3RV3RF0ORC3U53RN4M3"+username.encode()
        return msg
    
    def send_username_2_everyone(old_username,new_username):
        msg=b"S3RV3RS3ND0LDU53RNA4M3E"+old_username.encode()+b"NE3EWNA4AME3"+new_username.encode()
        return msg
    
    def welcome_msg(username):
        msg=b"S3RV3RW3ELC0OM3MS5G"+username.encode()
        return msg

server=Server()