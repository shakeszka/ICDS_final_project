import tkinter
import tkinter.messagebox
import customtkinter
import pickle
import argparse
import time

from tkinter import *
# from mttkinter import *
from tkinter import messagebox
import time
from pygame import mixer
import threading
from chat_utils import *
from chat_client_class import *
from client_state_machine import *
import json
import argparse
import os
import pickle
import random
import runpy

from chat_utils import *
from chat_client_class import *
from client_state_machine import *

from pygame import mixer # for music on/off function
import time # for sending messages function

parser = argparse.ArgumentParser(description='chat client argument')
parser.add_argument('-d', type=str, default=None, help='server IP addr')
args = parser.parse_args()

client = Client(args) 
client.init_chat()
print(client.socket)

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Starting the Home Page
        self.title('Home Page')
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        # ==============================================================================
        # Design of Home Page
        # ==============================================================================
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Text
        customtkinter.CTkLabel(self, text='Nihao! Welcome to Monogram!',font=('Calibri',40)).place(x=275, y= 10)
        customtkinter.CTkLabel(self, text='Login Page',font=('Calibri',36)).place(x=445, y= 75)
        self.main_body = customtkinter.CTkFrame(self, width=500)
        self.main_body.grid(column=2, row=1)

        self.main_body_label_1 = customtkinter.CTkLabel(self.main_body, text='Already have an account? ', font=('Calibri',20))
        self.main_body_label_1.grid(row=0, column=0, pady=10, padx=10)

        self.main_body_label_2 = customtkinter.CTkLabel(self.main_body, text='Enter your username: ', font=('Calibri',20))
        self.main_body_label_2.grid(row=1, column=0, pady=10, padx=10)
        self.input_username = StringVar()
        self.input_username.set('')
        self.username_entry = customtkinter.CTkEntry(self.main_body, textvariable=self.input_username, width=35, placeholder_text="Username")
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.main_body_label_3 = customtkinter.CTkLabel(self.main_body, text='Enter your password: ',font=("Calibri",20))
        self.input_password = StringVar()
        self.password_entry = customtkinter.CTkEntry(self.main_body, textvariable=self.input_password, width=35,show='*', placeholder_text="Password")
        self.password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.username=''

        self.main_body_label_4 = customtkinter.CTkButton(self.main_body, text='Log In', command=self.usrLogin)
        self.main_body_label_4.grid(row=4, column=0, pady=10, padx=10)

        self.main_body_label_5 = customtkinter.CTkLabel(self.main_body, text='New User? ',font=('Calibri',20))
        self.main_body_label_5.grid(row=5, column=0, pady=10, padx=10)
        self.main_body_label_6 = customtkinter.CTkButton(self.main_body, text='Sign Up', command=self.usrSignUp)
        self.main_body_label_6.grid(row=6, column=0, pady=10, padx=10)
    
    def usrLogin(self):
        global usrName
        usrName = self.input_username.get()
        usrPwd = self.input_password.get()
        try:
            with open('usrs_info.pickle', 'rb') as usrFile:
                usrsInfo = pickle.load(usrFile)   
        except FileNotFoundError: #if file doesn't exist yet, create a new file
            with open('usrs_info.pickle', 'wb') as usrFile:
                usrsInfo = {'admin': 'admin'}
                pickle.dump(usrsInfo, usrFile)    
        if usrName in usrsInfo:
            if usrPwd == usrsInfo[usrName]:
                messagebox.showinfo('Successfully Login!', 'Welcome to the chat system ' + usrName+'! Have a good time!') 
                client.login(usrName)
                self.startChatting()
            else:
                messagebox.showinfo('Wrong Password!')
        else:
            signedUpAlready = messagebox.askyesno("Oops, seems like you don't haven an account yet! Please sign up below first.")
            if signedUpAlready:
                self.usrSignUp()

    def startChatting(self):
        self.destroy()
        chat = Chatbox()
        chat.mainloop()
    
    def usrSignUp(self):
        def signUp():
            password = newPassword.get()
            passwordConfirm = newPasswordConfirm.get()
            name = signName.get()
            with open('usrs_info.pickle', 'rb') as usrFile:
                userlist = pickle.load(usrFile)
            if password != passwordConfirm:
                messagebox.showerror('Passwords do not match! Please try again!')
            elif name in userlist:
                messagebox.showerror('You have signed up! Please login with your username.')
            elif name == "":
                messagebox.showerror("Forget to enter your name?")
            elif password == "":
                messagebox.showerror("Forget to enter your password?")
            else:
                userlist[name] = password
                with open('usrs_info.pickle', 'wb') as usrFile:
                    pickle.dump(userlist, usrFile)
                messagebox.showinfo('You have successfully signed up!')
                self.signUpWindow.destroy()
                
        self.signUpWindow = Toplevel(self) #pop up the sign up window on the top
        self.signUpWindow.title('Sign up')
        self.signUpWindow.geometry(f"{1100}x{580}")
        self.signUpWindow.resizable(False, False)

        # configure grid layout (4x4)
        self.signUpWindow.grid_columnconfigure(1, weight=0)
        self.signUpWindow.grid_columnconfigure(2, weight=1)
        self.signUpWindow.grid_rowconfigure((0, 1, 2), weight=1)

        customtkinter.CTkLabel(self.signUpWindow, text='Create a new account!',font=('Calibri',40)).place(x=275, y= 30)

        self.signup_main_body = customtkinter.CTkFrame(self.signUpWindow, width=500)
        self.signup_main_body.grid(column=2, row=1)

        self.signup_main_body_label_1 = customtkinter.CTkLabel(self.signup_main_body, text='Please enter your username: ',font=('Calibri',20))
        self.signup_main_body_label_1.grid(row=0, column=0)
        signName = StringVar()
        self.entrySignName = customtkinter.CTkEntry(self.signup_main_body, textvariable=signName ,width=35)
        self.entrySignName.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.signup_main_body_label_2 = customtkinter.CTkLabel(self.signup_main_body, text='Please enter your password: ',font=("Calibri",20))
        self.signup_main_body_label_2.grid(row=2, column=0)
        newPassword = StringVar()
        self.entryUserPwd = customtkinter.CTkEntry(self.signup_main_body, textvariable=newPassword ,width=35)
        self.entryUserPwd.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.signup_main_body_label_3 = customtkinter.CTkLabel(self.signup_main_body, text='Please confirm your password: ',font=("Calibri",20))
        self.signup_main_body_label_3.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        newPasswordConfirm = StringVar()
        self.entryUserPwdConfirm = customtkinter.CTkEntry(self.signup_main_body, textvariable=newPasswordConfirm ,width=35)
        self.entryUserPwdConfirm.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        #
        self.signUpBtn2 = customtkinter.CTkButton(self.signup_main_body, text='Ready!', command=signUp)
        self.signUpBtn2.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        #loginBtn = customtkinter.CTkButton(self.signup_main_body, text='Login', command=self.usrLogin, width=13, bd=0).place(x=885, y=400)
        # loginBtn = Button(window, text='Login', command=usrLogin, borderwidth=0, width=10)
        #
        #signUpBtn = customtkinter.CTkButton(self.signup_main_body, text='Sign up', command=self.usrSignUp,width=13, borderwidth=0).place(x=885, y=515)

class Chatbox(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Monogram")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        # Configure grid rows and columns
        rows = [5, 1, 1] # the weight of the rows
        columns = [1, 1, 3] # the weight of the columns
        for r in range(len(rows)):
            self.rowconfigure(r, weight=rows[r])
        for c in range(len(columns)):
            self.columnconfigure(c, weight=columns[c])

        # Define a function to create placeholder frames for visual structure
        def create_widget(self, parent, row, column, rowspan=1, columnspan=1, padx=20, pady=(20,0), width=100):
            self.frame = customtkinter.CTkFrame(master=parent, width=width, height=100, corner_radius=10)
            self.frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
            return self.frame

        ### --- left sidebar ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Username", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # first two buttons
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text='Pfp', command=self.sidebar_button_pfp)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text='Profile', command=self.sidebar_button_profile)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # bottom button 1
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # bottom button 2
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        ### --- second column ---
        # upper bottons
        self.second_column_upper = customtkinter.CTkFrame(self, border_width=2, border_color="gray")
        self.second_column_upper.grid(row=0, column=1, padx=(20, 20), pady=(0, 0)) #, sticky="nsew"
        #self.second_column_upper.grid_rowconfigure(3, weight=0)

        self.button_1 = customtkinter.CTkButton(master=self.second_column_upper, text='Online Users', command=self.second_column_get_users)
        self.button_1.grid(row=0, column=0, padx=20, pady=10)
        self.button_2 = customtkinter.CTkButton(master=self.second_column_upper, text='Disconnect', command=self.second_column_disconnect)
        self.button_2.grid(row=1, column=0, padx=20, pady=10)

        # self.label_1 = customtkinter.CTkLabel(self.second_column_upper, text="Online Users")
        # self.label_1.grid(row=3, column=0, padx=20, pady=10)
        # self.online_box = customtkinter.CTkFrame(self.second_column_upper, width=150)
        # self.online_box.grid(row=3, column=0, padx=10, pady=10)

        # middle buttons
        self.second_column_middle = customtkinter.CTkFrame(self)
        self.second_column_middle.grid(row=2, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.button_4 = customtkinter.CTkButton(master=self.second_column_middle, text='Music On', command=self.second_column_music_on)
        self.button_4.grid(row=1, column=0, padx=20, pady=10)
        self.button_5 = customtkinter.CTkButton(master=self.second_column_middle, text='Music Off', command=self.second_column_music_off)
        self.button_5.grid(row=2, column=0, padx=20, pady=10)
        # bottom buttons
        self.second_column_bottom = customtkinter.CTkFrame(self)
        self.second_column_bottom.grid(row=3, column=1, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.second_column_bottom, text="TicTacToe Game", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.button_5 = customtkinter.CTkButton(master=self.second_column_bottom, text='Player X', command=self.second_column_playerX)
        self.button_5.grid(row=2, column=0, padx=20, pady=10)
        self.button_6 = customtkinter.CTkButton(master=self.second_column_bottom, text='Player O', command=self.second_column_playerO)
        self.button_6.grid(row=3, column=0, padx=20, pady=10) 

        ### --- textbox ---
        # message container
        self.message_container = customtkinter.CTkFrame(self)
        self.message_container.grid(row=0, rowspan=3, column=2,padx=(20, 20), pady=(20, 20), sticky="nsew")
        # to send msgs
        self.messageList = customtkinter.CTkTextbox(self.message_container, height = 500,width=700)
        self.messageList.configure(state='disabled') 
        self.messageList.tag_config('myMessage', foreground = 'white')
        # buttons
        # self.chat_box = customtkinter.CTkTextbox(self)
        self.txt_msgsend = customtkinter.CTkTextbox(self)
        self.txt_msgsend.grid(row=2, column=2, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.txt_msgsend.bind('<KeyPress-Return>',self.msgsendEvent)

        #self.txt_msgsend.bind('<KeyPress-Return>',self.msgsendEvent)
        self.button_7 = customtkinter.CTkButton(master=self.txt_msgsend, text='Send', command=self.msgsend)
        self.button_7.grid(row=2, column=0, pady=(10,0))
        self.button_8 = customtkinter.CTkButton(master=self.txt_msgsend, text='Clear', command=self.third_column_clear)
        self.button_8.grid(row=2, column=1, pady=(10,0))
        # to send msgs
        #self.txt_msgsend = customtkinter.CTkTextbox(self.chat_box,height = 10)
        #self.txt_msgsend.bind('<KeyPress-Return>',self.msgsendEvent)

        # some gridding
        self.messageList.grid() 
        self.txt_msgsend.grid()

        # sending msgs
        self.messageList.configure(state='normal')
        self.messageList.insert(END,menu)
        client.system_msg = ''
        self.messageList.configure(state='disabled')
        
        #code from chat_client_class
        reading_thread = threading.Thread(target = self.refresh)
        reading_thread.daemon = True
        reading_thread.start()

        # set default values
        # sidebar
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    ### --- functions ---
    # sidebar
    def sidebar_button_pfp(self):
        print("sidebar_button_pfp clicked")
    
    def sidebar_button_profile(self):
        print("sidebar_button_profile click")

    def random_button(self):
        print("random_button clicked")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # second column
    def second_column_get_users(self):
        print("second_column_get_users clicked")

    def second_column_disconnect(self):
        print("second_column_disconnect clicked")

    def second_column_music_on(self):
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.play()
    
    def second_column_music_off(self):
        mixer.music.pause()

    def second_column_playerX(self):
        print("second_column_playerX clicked")
        # runpy.run_path(path_name='playerx.py')
    
    def second_column_playerO(self):
        print("second_column_playerO clicked")
        # runpy.run_path(path_name='playero.py')

    # third column
    def msgsend(self):
        msg = ' Me '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
        self.messageList.configure(state='normal')
        self.messageList.insert(END,msg,'myMessage') 
        self.messageList.insert(END,self.txt_msgsend.get('0.0',END))
        m = self.txt_msgsend.get('0.0',END).strip()
        self.txt_msgsend.delete('0.0',END) 
        self.messageList.configure(state='disabled')
        self.messageList.see(END)
        client.proc()
        client.console_input.append(m)            
            
    def clear(self):
        self.txt_msgsend.delete('0.0',END) 

    def msgsendEvent(self, event):
        if event.keysym == 'Return':
            self.msgsend()
            x=threading.Thread(target=self.after_return)
            x.start()
    
    def after_return(self):
        time.sleep(0.01)
        self.clear()

    def refresh(self):
        while True:
            client.proc()
            # getWhoOnline()
            #time.sleep(CHAT_WAIT)
            if client.system_msg != '':
                m = client.system_msg
                # print("m " + m[-3:])
                if m[-3:] != "who":
                    self.messageList.configure(state='normal')
                    self.messageList.insert(END,'\n' + client.system_msg + '\n')
                    self.messageList.configure(state='disabled')
                    self.messageList.see(END)
                client.system_msg = ''

    def third_column_clear(self):
        print("third_column_clear clicked")

if __name__ == "__main__":
    # app = App()
    # app.mainloop()
    chat = Chatbox()
    chat.mainloop()
