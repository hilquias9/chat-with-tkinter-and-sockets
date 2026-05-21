import socket
import threading

class  Client:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.client.connect(("172.16.2.27",7777))
        thread=threading.Thread(target=self.receive_messages,args=(self.client,),daemon=True)
        thread.start()
    
    def send_msg(self,msg:str):
        b_msg=msg.encode()
        self.client.send(b_msg)
    
    def receive_messages(self):
        while True:
            try:
                msg=self.client.recv(2048)
                print("chegou uma mensagem")
                if msg:
                    return msg
            except Exception as error:
                print(f"Ocorreu um erro na receive_messages classe Clients, erro: {error}")
                self.client.close()


a=[11,34,6546,565]

print(a)


contador=0
while contador<len(a):
    print(a[contador])
    contador+=1