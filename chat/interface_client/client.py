import socket
import threading
from tkinter import messagebox

class  Client:
    def __init__(self,on_message):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.on_message=on_message
        self.client.connect(("172.16.2.27",7777))
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
            while True:
                try:
                    msg=self.client.recv(2048)
                    if msg:
                        self.on_message(msg)
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    self.client.close()
        except KeyboardInterrupt:
            print(f"A conexão foi cancelada ctrl + c")
        
