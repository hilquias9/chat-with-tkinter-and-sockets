from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from client import Client
import os


class Interface(Frame):
    def __init__(self,root):
        super().__init__()
        root.title("UmDiaUmChat")
        root.geometry("1280x720")
        root.resizable(False,False)

        
        self.mid_frame=Frame(root,bg="#7D4698")
        self.mid_frame.place(x=256,relheight=1,relwidth=0.6)

        self.mid_entry=Entry(self.mid_frame)
        self.mid_entry.place(x=80,y=680,width=5,relwidth=0.8)
        self.mid_entry.bind("<Return>",self.entry_enter_pressed)

        self.mid_button_send_message=Button(self.mid_frame,text="➜",command=self.mid_button_send_message_func)
        self.mid_button_send_message.place(width=50,y=677,x=710)

        self.mid_button_send_files=Button(self.mid_frame,text="📄", command=self.mid_button_send_files_func)
        self.mid_button_send_files.place(width=50,y=677,x=16)


        self.text_frame=Frame(self.mid_frame,bg="#333A41")
        self.text_frame.place(y=5,relheight=0.9,relwidth=1)

        self.text=Text(self.text_frame,state="disabled")
        self.text.place(relheight=1,relwidth=1)

        self.right_frame=Frame(root,bg="#59316B")
        self.right_frame.place(relheight=1,x=1024,relwidth=1)


        self.right_label=Label(self.right_frame,text="Histórico\nde\nUsuários",font=("times",18),bg="#59316B",fg="white")
        self.right_label.place(relx=0.06,y=5)


        self.left_frame=Frame(root,bg="#59316B")
        self.left_frame.place(relheight=1,x=0,relwidth=0.2004)

    def entry_enter_pressed(self,event):
        self.mid_button_send_message_func()
    
    def mid_button_send_message_func(self):
        if self.mid_entry.get().strip()!="":
            mensagem="Usuario: "+self.mid_entry.get()+"\n"
            self.mid_entry.delete(0,END)
            self.put_message_on_text(mensagem)
            mensagem="M3SAG3C0O%$D3"+mensagem
            cliente.send_msg(mensagem)
    
    def mid_button_send_files_func(self):
        directory=filedialog.askopenfilename()
        filename=os.path.basename(directory)
        cliente.send_file(filename=filename,directory=directory)
        

    def put_message_on_text(self,msg:str):
        self.text.config(state="normal")
        self.text.insert(END,msg)
        self.text.config(state="disabled")

    def add_message_safe(self, msg):
        msg=msg.decode()
        msg_splitted=msg.split("M3SAG3C0O%$D3")
        self.after(0, self.put_message_on_text, msg_splitted[1])
    

if __name__=="__main__":
    root=Tk()
    app=Interface(root)
    try:
        cliente=Client(app.add_message_safe)
    except Exception as error:
        messagebox.showerror(title="UmDiaUmChat",message="Não foi possível conectar com o servidor!")
        print(f"Aconteceu um erro: {error}")
        root.destroy()
    root.mainloop()