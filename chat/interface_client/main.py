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

        self.right_text_frame=Frame(self.right_frame,bg="#59316B")
        self.right_text_frame.place(x=10,relwidth=0.185,y=100,relheight=0.8)


        self.right_text=Text(self.right_text_frame,state="disabled")
        self.right_text.place(relheight=1,relwidth=1)


        self.left_frame=Frame(root,bg="#59316B")
        self.left_frame.place(relheight=1,x=0,relwidth=0.2004)


        self.username="User"
        self.counter_tag=0
        self.left_button=Button(self.left_frame, text="🔧",command=self.user_configuration)
        self.left_button.place(width=50,y=10,x=10)



    def entry_enter_pressed(self,event):
        self.mid_button_send_message_func()
    
    def mid_button_send_message_func(self):
        if self.mid_entry.get().strip()!="":
            message=f"{self.username}: "+self.mid_entry.get()+"\n"
            self.mid_entry.delete(0,END)
            self.put_message_on_text(message)
            message_model=b"M3SAG3C0O%$D3"+message.encode()
            message_length=len(message_model)
            message_length=message_length+len(str(message_length).encode())+len(b"M33SS4GL3N")
            message=b"M3SAG3C0O%$D3"+(f"{message_length}").encode()+b"M33SS4GL3N"+message.encode()
            cliente.send_msg(message)
    
    def mid_button_send_files_func(self):
        directory=filedialog.askopenfilename()
        if directory:
            filename=os.path.basename(directory)
            cliente.send_file(filename=filename,directory=directory)
        

    def put_message_on_text(self,msg:str):
        self.text.config(state="normal")
        self.text.insert(END,msg)
        self.text.config(state="disabled")
        self.text.see(END)

    def add_message_safe(self, msg):
        if b"TYP31S3V3RR" in msg:
            msg_extractor=msg.decode().split("TYP31S3V3RR")[1]
            msg_fist_part=msg_extractor.split("f1l3n4m3c0d&")[0]
            filename_extractor=msg_extractor.split("f1l3n4m3c0d&")[1]
            filename=filename_extractor.split("3NDF1L3N4M3C0D&")[0]
            msg=msg_fist_part+filename+"\n"
            self.after(0,self.put_message_on_text,msg)
            self.after(0,self.file_on_text(msg,filename))
        elif b"S3RV3RF0ORC3U53RN4M3" in msg:
            self.username=msg.split(b"S3RV3RF0ORC3U53RN4M3")[1].decode()
        else:
            msg=msg.decode()
            self.after(0, self.put_message_on_text, msg)

    def user_configuration(self):
        user_config=Toplevel()
        
        user_config.geometry("400x400")
        user_config.title("Settings")


        username_label=Label(user_config,text="Username:")
        username_label.place(relx=0.01,y=10)
        
        username_entry=Entry(user_config,)
        username_entry.place(width=80,x=75,y=10)


        def username_button_command():
            self.username=username_entry.get().strip()
            if self.username:
                try:
                    cliente.send_msg(b"S3NDdUS3N4M3!"+self.username.encode())
                    username_entry.delete(0,END)
                    messagebox.showinfo(message="Username alterado com sucesso!")
                    user_config.destroy()
                except Exception as error:
                    print("Ocorreu um error ao tentar enviar a mudança de nome de usuário: ",error)
                    messagebox.showerror(title="UmDiaUmChat",message="Não foi possível alterar o nome de usuário!")
        def username_enter_pressed(event):
            username_button_command()
        
        username_entry.bind("<Return>",username_enter_pressed)
        

        username_button=Button(user_config,text="➜",command=username_button_command)
        username_button.place(width=70,x=170,y=5)
    
    def file_on_text(self,msg,filename):
        def click(event):
            clicked(msg)
        
        def clicked(msg):
            response=messagebox.askyesno(title="UmDiaUmChat",message="Deseja baixar o arquivo?")
            if response:
                msg=b"SERV3R_S3ND_F1LEC0OOODE3"+filename.encode()
                cliente.send_msg(msg)
        tag="download"
        color_tag="colortag"
        start = self.text.index(f"end-{len(msg)}c")
        end = self.text.index("end-2c")
        self.text.tag_add(f"{tag}{self.counter_tag}",start,end)
        self.text.tag_bind(f"{tag+str(self.counter_tag)}","<Button-1>", click)
        self.text.tag_config(color_tag+str(self.counter_tag),foreground="red")
        self.text.tag_add(color_tag+str(self.counter_tag), start, end)
        self.counter_tag=self.counter_tag+1
    

if __name__=="__main__":
    root=Tk()
    app=Interface(root)
    try:
        cliente=Client(username=app.username,on_message=app.add_message_safe)
    except Exception as error:
        messagebox.showerror(title="UmDiaUmChat",message="Não foi possível conectar com o servidor!")
        print(f"Aconteceu um erro: {error}")
        root.destroy()
    root.mainloop()