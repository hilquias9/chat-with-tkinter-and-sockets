import socket
import threading
from tkinter import messagebox
import os


class  Client:
    def __init__(self,username:str,on_message):
        hostname=socket.gethostname()
        private_ipv4=socket.gethostbyname(hostname)
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.username=username
        self.on_message=on_message
        self.client.connect((private_ipv4,7777))
        self.send_username(username)
        print("CONECTADO!")
        thread=threading.Thread(target=self.receive_messages,daemon=True)
        thread.start()
    
    def send_username(self,username):
        try:
            msg=b"S3NDdUS3N4M3!"+username.encode()
            self.client.send(msg)
        except Exception as error:
            print("Ocorreu um erro ao enviar o username: ",error)
            self.client.close()
    
    def send_msg(self,msg:bytes):
        try:
            self.client.send(msg)
        except Exception as error:
            print(f"Ocorreu um erro ao tentar enviar mensagem para o servidor: {error}")
            self.client.close()
            messagebox.showerror(title="UmDiaUmChat",message="A conexão com o servidor foi perdida!")
    
    def receive_messages(self):
        try:
            while True:
                try:
                    msg=self.client.recv(2048)
                    print("CHEGOU MENSAGEM: ",msg)
                    if b"M3SAG3C0O%$D3" in msg:
                        message=self.message_extractor(msg)
                        self.on_message(message)
                    elif b"f1l3n4m3c0d&" in msg:
                        self.receive_files(msg)
                    elif b"S3RV3RF1iL3C0D3" in msg:
                        self.server_msgs(msg)
                    elif b"S3RV3RF0ORC3U53RN4M3" in msg:
                        self.username=msg.split(b"S3RV3RF0ORC3U53RN4M3")[1].decode()
                        self.on_message(msg)
                    elif b"S3RV3RS3ND0LDU53RNA4M3E":
                        print("CLIENTE RECEBEU SERVER NEW AND OLD USERNAME: ",msg)
                        self.on_message(msg)
                    elif b"S3RV3RW3ELC0OM3MS5G" in msg:
                        self.on_message(msg)
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    self.client.close()
                    break
                except OSError as error:
                    print(f"A conexão foi perdida! {error}")
                    self.client.close()
                    break
        except KeyboardInterrupt:
            print(f"A conexão foi cancelada ctrl + c")
    
    def message_extractor(self,msg):
        header_extracter=msg.split(b"M3SAG3C0O%$D3")[1]
        len_extracter=header_extracter.split(b"M33SS4GL3N")[0]
        len_msg=len(msg)
        data_collector=b""
        if int(len_extracter.decode())>len_msg:
            while True:
                data=self.client.recv(2048)
                if not data: break
                len_msg=len_msg+len(data)
                data_collector+=data
                if len_msg==int(len_extracter.decode()):break
        message=header_extracter.split(b"M33SS4GL3N")[1]+data_collector
        return message
        
    def send_file(self,filename:str,directory:str):
        file=b"f1l3n4m3c0d&"+filename.encode()+b"3NDF1L3N4M3C0D&"
        with open(directory,"rb") as f:
            lines=f.read()
            lines=lines+b"3NDF1L3N4M3C0D&"
        file_length=len(lines)+len(file)+len("4RKH1V3L3N")
        file_length=file_length+len(str(file_length))
        file=file+str(file_length).encode()+b"4RKH1V3L3N"+lines
        self.client.sendall(file)
    
    def receive_files(self,file):
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
                lines=self.client.recv(2048)
                if not lines:
                    break
                file_bytes=file_bytes+lines
                total=total+len(lines)
            except Exception as error:
                print(f"Ocorreu um erro na Receive_files: {error}")
                self.client.close()
                break
        path=os.getcwd()
        os.makedirs(name="downloads",exist_ok=True)
        with open(f"{path}\\downloads\\{file_name}","wb") as f:
            f.write(file_bytes.split(b"3NDF1L3N4M3C0D&")[0])

        
    def server_msgs(self,msg):
        if b"S3RV3RF1iL3C0D3" in msg:
            extractor=msg.split(b"S3RV3RF1iL3C0D3")[1]
            name=extractor.split(b"US3ERN4AM3EC0D3E")[0]
            filename=extractor.split(b"US3ERN4AM3EC0D3E")[1]
            message=f"TYP31S3V3RR[SERVER MESSAGE]: O usuario {name.decode()} enviou f1l3n4m3c0d&{filename.decode()}3NDF1L3N4M3C0D&\n".encode()
            self.on_message(message)


