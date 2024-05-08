import tkinter
import tkinter.messagebox
import customtkinter
from CTkListbox import * # for list of users
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

        # Configure grid rows and columns
        rows = [6, 1, 0] # the weight of the rows
        columns = [0, 0, 6] # the weight of the columns
        for r in range(len(rows)):
            self.rowconfigure(r, weight=rows[r])
        for c in range(len(columns)):
            self.columnconfigure(c, weight=columns[c])

        # functions to create placeholder frames for visual structure
        def create_frame(self, parent, row, column, rowspan=1, columnspan=1, pady=(20, 0), padx=(0, 20), width=0, height=0, corner_radius=10, border_color='white', border_width=0):
            self.frame = customtkinter.CTkFrame(master=parent, width=width, height=height, corner_radius=corner_radius, border_color=border_color, border_width=border_width)
            self.frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
            return self.frame
        
        def create_label(self, parent, row, column, rowspan=1, columnspan=1, width=0, height=0, pady=(20, 0), padx=20, corner_radius=10, text='Label', anchor="w"):
            self.label = customtkinter.CTkLabel(master=parent, text=text, width=width, height=height, anchor=anchor)
            self.label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew", pady=pady, padx=padx)
            return self.label
        
        def create_button(self, parent, row, column, rowspan=1, columnspan=1, pady=(20,0), padx=20, text='Button', corner_radius=5, command=self.test):
            self.button = customtkinter.CTkButton(master=parent, text=text, command=command, corner_radius=corner_radius)
            self.button.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky="nsew")
            return self.button
        
        def create_option_menu(self, parent, row, column, rowspan=1, columnspan=1, pady=(20, 0), padx=20, values=[], command=self.test):
            self.option_menu = customtkinter.CTkOptionMenu(master=parent, values=values, command=command)
            self.option_menu.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky="nsew")
            return self.option_menu
        
        def create_textbook(self, parent, row, column, rowspan=1, columnspan=1, pady=(20, 0), padx=(0, 20), width=0, height=0, corner_radius=10, border_color='white', border_width=0):
            self.textbook = customtkinter.CTkTextbox(master=parent, width=width, height=height, corner_radius=corner_radius, border_color=border_color, border_width=border_width)
            self.textbook.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky="nsew")
            return self.textbook
        
        ### --- sidebar ---
        self.sidebar_frame = create_frame(self, self, 0, 0, rowspan=3, pady=0, corner_radius=0)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = create_label(self, self.sidebar_frame, 0, 0, text="Username")
        self.sidebar_button_1 = create_button(self, self.sidebar_frame, 1, 0, text='Pfp', command=self.second_column_music_on)
        self.sidebar_button_2 = create_button(self, self.sidebar_frame, 2, 0, text='Profile', command=self.second_column_music_on)
        self.appearance_mode_label = create_label(self, self.sidebar_frame, 5, 0, text='Appearance Mode')
        self.appearance_mode_optionemenu = create_option_menu(self, self.sidebar_frame, 6, 0, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.scaling_label = create_label(self, self.sidebar_frame, 7, 0, text='UI Scaling:')
        self.scaling_optionemenu = create_option_menu(self, self.sidebar_frame, 8, 0, pady=(20, 20), values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)

        ### --- middle ---
        self.middle = create_frame(self, self, 0, 1)
        self.middle.grid_rowconfigure(4, weight=1)
        self.middle_button_1 = create_button(self, self.middle, 0, 0, text='Online Users', command=self.get_users)
        self.middle_button_2 = create_button(self, self.middle, 1, 0, text='Disconnect', command=self.disconnect)

        self.whoOnline = StringVar()
        self.users = create_label(self, self.middle, 2, 0, text="Here are online users! \nClick to chat with:")
        self.whoListBox = Listbox(self.middle, listvariable=self.whoOnline, width=10, height=5)
        self.whoListBox.grid(row=3, column=0, rowspan=1, columnspan=1, padx=10, pady=10, sticky="nsew")
        self.whoListBox.bind('<Double-Button-1>', self.connectTo)
        # middle buttons
        self.middle_middle = create_frame(self, self, 1, 1)
        self.middle_middle.grid_rowconfigure(2, weight=1)
        self.middle_button_3 = create_button(self, self.middle_middle, 0, 0, text='Music On', command=self.second_column_music_on)
        self.middle_button_4 = create_button(self, self.middle_middle, 1, 0, text='Music Off', command=self.second_column_music_off)
        # bottom buttons
        self.middle_bottom = create_frame(self, self, 2, 1, pady=(20, 20))
        self.middle_bottom.grid_rowconfigure(2, weight=1)
        self.middle_label_1 = create_label(self, self.middle_bottom, 0, 0, text='TicTacToe Game')
        self.middle_button_5 = create_button(self, self.middle_bottom, 1, 0, text='Player X', command=self.player_X)
        self.middle_button_6 = create_button(self, self.middle_bottom, 2, 0, text='Player O', command=self.player_O)

        ### --- textbox ---
        # message container
        self.messageList = create_textbook(self, self, 0, 2)
        self.messageList.configure(state='disabled')
        self.messageList.tag_config('myMessage', foreground = 'white')
        # chatbox
        self.txt_msgsend = create_textbook(self, self, 1, 2)
        self.txt_msgsend.bind('<KeyPress-Return>',self.msgsendEvent)
        # buttons
        self.main_buttons = create_frame(self, self, 2, 2, pady=(20, 20))
        self.main_buttons.grid_columnconfigure(2, weight=1)
        self.main_button_1 = create_button(self, self.main_buttons, 0, 3, text='Send', command=self.msgsend)
        self.main_button_2 = create_button(self, self.main_buttons, 0, 4, text='Clear', command=self.clear)


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

        def online_update(): #update
            if client.sm.get_state() != S_OFFLINE:
                onlinedict=client.sm.whoOnLine
                # print(onlinedict)
                # onlinedict = onlinedict.split(",")

            else:
                onlinedict = {}
            self.whoOnline.set(list(onlinedict))
            self.whoListBox.after(1000, online_update)
    
        online_update()

    ### --- functions ---
    # test
    def test(self):
        pass

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
    def get_users(self):
        client.console_input.append('who')

    def disconnect(self):
        client.console_input.append('bye')

    def getWhoOnline(self):
        client.console_input.append("who")      
        print("getWhoOnline "+client.sm.whoOnLine)   
        whoOnlineList = client.sm.whoOnLine

        whoOnlineList = whoOnlineList.split(',') 
        # print(type(whoOnlineList)) 
        self.whoOnline.set(whoOnlineList)

    #@staticmethod
    def connectTo(self, event):
        connectToWhom =  self.whoListBox.get(self.whoListBox.curselection())
        print("double click")
        print(connectToWhom)
        if connectToWhom != client.name:
            client.console_input.append('c ' + connectToWhom)

        if client.sm.get_state() == S_CHATTING:
            client.console_input.append('bye')
            client.console_input.append('c ' + connectToWhom)

    # def getWhoOnline(self):
    #     client.console_input.append("who")      
    #     print("getWhoOnline "+client.sm.whoOnLine)   
    #     whoOnlineList = client.sm.whoOnLine

    #     whoOnlineList = whoOnlineList.split(',') 
    #     # print(type(whoOnlineList)) 
    #     self.whoOnline.set(whoOnlineList)

    def second_column_music_on(self):
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.play()
    
    def second_column_music_off(self):
        mixer.music.pause()

    def player_O(self):
        print("player_O clicked")
        # runpy.run_path(path_name='playero.py')
    
    def player_X(self):
        print("player_X clicked")
        # runpy.run_path(path_name='playerx.py')

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

        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    chat = Chatbox()
    chat.mainloop()
