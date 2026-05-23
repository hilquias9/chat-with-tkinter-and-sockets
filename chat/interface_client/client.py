import socket
import threading
from tkinter import messagebox


class  Client:
    def __init__(self,on_message):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.on_message=on_message
        self.client.connect(("192.168.3.102",7777))
        print("CONECTADO!")
        thread=threading.Thread(target=self.receive_messages,daemon=True)
        thread.start()
    
    def send_msg(self,msg:str):
        try:
            b_msg=msg.encode()
            self.client.send(b_msg)
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
                    if b"&ND_F1L3_C@D3" in msg:
                        self.on_message(msg)
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    self.client.close()
        except KeyboardInterrupt:
            print(f"A conexão foi cancelada ctrl + c")
        
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
        