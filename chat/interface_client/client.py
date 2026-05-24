import socket
import threading
from tkinter import messagebox
import os


class  Client:
    def __init__(self,on_message):
        hostname=socket.gethostname()
        private_ipv4=socket.gethostbyname(hostname)
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.on_message=on_message
        self.client.connect((private_ipv4,7777))
        print("CONECTADO!")
        thread=threading.Thread(target=self.receive_messages,daemon=True)
        thread.start()
    
    def send_msg(self,msg:bytes):
        try:
            self.client.send(msg)
            print("Mensagem enviada para o servidor!")
        except Exception as error:
            print(f"Ocorreu um erro ao tentar enviar mensagem para o servidor: {error}")
            self.client.close()
            messagebox.showerror(title="UmDiaUmChat",message="A conexão com o servidor foi perdida!")
    
    def receive_messages(self):
        try:
            print("Receive_messages iniciada!")
            while True:
                try:
                    msg=self.client.recv(2048)
                    if b"M3SAG3C0O%$D3" in msg:
                        message=self.message_extractor(msg)
                        print("message retornada")
                        self.on_message(message)
                    elif b"f1l3n4m3c0d&" in msg:
                        print("Arquivo vai ser recebido")
                        self.receive_files(msg)
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
        print("message extractor iniciada")
        header_extracter=msg.split(b"M3SAG3C0O%$D3")[1]
        len_extracter=header_extracter.split(b"M33SS4GL3N")[0]
        len_msg=len(msg)
        print("Tamanho da mensagem: ", len_extracter)
        print("Tamanho esperado: ",len_msg)
        data_collector=b""
        if int(len_extracter.decode())>len_msg:
            print("Len extracter menor, entrei no while")
            while True:
                data=self.client.recv(2048)
                if not data: break
                len_msg=len_msg+len(data)
                data_collector+=data
                if len_msg==int(len_extracter.decode()):break
        message=header_extracter.split(b"M33SS4GL3N")[1]+data_collector
        return message
        
    def send_file(self,filename:str,directory:str):
        print("Função send_file iniciada!")
        file=b"f1l3n4m3c0d&"+filename.encode()+b"3NDF1L3N4M3C0D&"
        with open(directory,"rb") as f:
            lines=f.read()
            print("Len de lines: ",len(lines))
            lines=lines+b"3NDF1L3N4M3C0D&"
        file_length=len(lines)+len(file)+len("4RKH1V3L3N")
        file_length=file_length+len(str(file_length))
        file=file+str(file_length).encode()+b"4RKH1V3L3N"+lines
        self.client.sendall(file)
        print(f"Arquivo: {filename} {file_length} enviado com sucesso!")
    
    def receive_files(self,file):
        print("Receive_files iniciada!")
        extract_file_name=file.split(b"f1l3n4m3c0d&")
        extract_file_name2=extract_file_name[1].split(b"3NDF1L3N4M3C0D&")
        file_name=extract_file_name2[0].decode()
        extract_file_length=extract_file_name2[1].split(b"4RKH1V3L3N")
        file_length=int(extract_file_length[0].decode())
        file_bytes=extract_file_length[1]
        total=len(file)
        print("Nome do arquivo: ",file_name)
        print("Tamanho esperado: ",file_length)
        print("Tamanho até o momento: ",len(file))
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
            print("Arquivo escrito!")
        print("Função receive_files encerrada!")
        