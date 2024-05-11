from customtkinter import *
from CTkListbox import * # for list of users
import pickle
import argparse

from tkinter import *
from tkinter import messagebox
from pygame import mixer
import threading
from chat_utils import *
from chat_client_class import *
from client_state_machine import *
import json
import os
import random
import runpy
from PIL import Image

from pygame import mixer # for music on/off function
import time # for sending messages function

parser = argparse.ArgumentParser(description='chat client argument')
parser.add_argument('-d', type=str, default=None, help='server IP addr')
args = parser.parse_args()

client = Client(args) 
client.init_chat()
print(client.socket)

set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(CTk):
    def __init__(self):
        super().__init__()

        # Starting the Home Page
        self.title('Home Page')
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        # ==============================================================================
        # Design of Home Page
        # ==============================================================================
        # --- main frame ---
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True)
        self.heading_label = CTkLabel(self.main_frame, text='Nihao! Welcome to Monogram!',font=('Calibri',40))
        self.heading_label.place(relx=0.5, rely=0.02, anchor="n")
        self.login_frame = CTkFrame(self.main_frame)
        self.login_frame.place(relx=0.05, rely=0.15, relwidth=0.40, relheight=0.80)
        self.img_frame = CTkFrame(self.main_frame)
        self.img_frame.place(relx=0.50, rely=0.15, relwidth=0.45, relheight=0.80)

        # --- login frame --- 
        self.login_label_1 = CTkLabel(self.login_frame, text='Log In',font=('Calibri',26))
        self.login_label_1.place(relx=0.5, rely=0.1, anchor="n")
        self.login_label_2 = CTkLabel(self.login_frame, text='Already have an account? ', font=('Calibri',20))
        self.login_label_2.place(relx=0.3, rely=0.2, anchor='n')

        # username
        self.login_label_3 = CTkLabel(self.login_frame, text='Enter your username: ', font=('Calibri',16))
        self.login_label_3.place(relx=0.25, rely=0.3, anchor="n")
        self.input_username = StringVar()
        self.input_username.set('')
        self.username_entry = CTkEntry(self.login_frame, textvariable=self.input_username, placeholder_text="Username") #width=35
        self.username_entry.place(relx=0.315, rely=0.375, anchor="n", relwidth=0.5, relheight=0.075)
        
        # password
        self.login_label_4 = CTkLabel(self.login_frame, text='Enter your password: ', font=('Calibri',16))
        self.login_label_4.place(relx=0.25, rely=0.475, anchor="n")
        self.input_password = StringVar()
        self.password_entry = CTkEntry(self.login_frame, textvariable=self.input_password, show='*', placeholder_text="Password")
        self.password_entry.place(relx=0.315, rely=0.545, anchor="n", relwidth=0.5, relheight=0.075)

        self.login_button = CTkButton(self.login_frame, text='Start chatting',font=('Calibri',16), command=self.usrLogin)
        self.login_button.place(relx=0.5, rely=0.655, anchor='n')

        # sign up
        self.login_label_6 = CTkLabel(self.login_frame, text='New User?', font=('Calibri',20))
        self.login_label_6.place(relx=0.15, rely=0.75, anchor='n')

        self.signup_button = CTkButton(self.login_frame, text='Sign Up',font=('Calibri',16), command=self.usrSignUp)
        self.signup_button.place(relx=0.5, rely=0.86, anchor='n')

        # --- img frame --- 
        #the background image
        self.image = CTkImage(dark_image= Image.open('./kot.gif'), size=(500,500))
        self.image_label = CTkLabel(self.img_frame, image=self.image, text='')
        self.image_label.place(relx=0.4, rely=0.55, anchor="center")
    
    def usrLogin(self):
        global usrName
        usrName = self.input_username.get()
        usrPwd = self.input_password.get()
        try:
            with open('usrs_info.pickle', 'rb') as usrFile:
                usrsInfo = pickle.load(usrFile)   
        except FileNotFoundError: # if file doesnt exist, create a new file
            with open('usrs_info.pickle', 'wb') as usrFile:
                usrsInfo = {'admin': 'admin'}
                pickle.dump(usrsInfo, usrFile)    
        if usrName in usrsInfo:
            if usrPwd == usrsInfo[usrName]:
                messagebox.showinfo('Successfully Login!', 'Welcome to the chat system ' + usrName+'! Have a good time!') 
                client.login(usrName)
                self.startChatting()
            else:
                messagebox.showinfo('Incorrect','Wrong Password!')
        else:
            signedUpAlready = messagebox.askyesno("Small error :(", "Oops, Seems like you don't haven an account yet! Please sign up below first.")
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
                messagebox.showerror('Not matching', 'Passwords do not match! Please try again!')
            elif name in userlist:
                messagebox.showerror('Success!', 'You have signed up! Please login with your username.')
            elif name == "":
                messagebox.showerror('Forgot?',"Forget to enter your name?")
            elif password == "":
                messagebox.showerror('Forgot?',"Forget to enter your password?")
            else:
                userlist[name] = password
                with open('usrs_info.pickle', 'wb') as usrFile:
                    pickle.dump(userlist, usrFile)
                messagebox.showinfo("Ura!", 'You have successfully signed up!')
                self.signup_window.destroy()
        
        # pop up the sign up window on the top
        self.signup_window = Toplevel(self)
        self.signup_window.title('Sign up')
        self.signup_window.geometry(f"{1100}x{580}")
        self.signup_window.resizable(False, False)

        # configure grid layout (4x4)
        self.signup_window.grid_columnconfigure(1, weight=0)
        self.signup_window.grid_columnconfigure(2, weight=1)
        self.signup_window.grid_rowconfigure((0, 1, 2), weight=1)

        CTkLabel(self.signup_window, text='Create a new account!',font=('Calibri',40)).place(x=275, y= 30)

        self.signup_main_body = CTkFrame(self.signup_window, width=500)
        self.signup_main_body.grid(column=2, row=1)

        self.signup_main_body_label_1 = CTkLabel(self.signup_main_body, text='Please enter your username: ',font=('Calibri',20))
        self.signup_main_body_label_1.grid(row=0, column=0)
        signName = StringVar()
        self.entrySignName = CTkEntry(self.signup_main_body, textvariable=signName ,width=35)
        self.entrySignName.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.signup_main_body_label_2 = CTkLabel(self.signup_main_body, text='Please enter your password: ',font=("Calibri",20))
        self.signup_main_body_label_2.grid(row=2, column=0)
        newPassword = StringVar()
        self.entryUserPwd = CTkEntry(self.signup_main_body, textvariable=newPassword ,width=35)
        self.entryUserPwd.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.signup_main_body_label_3 = CTkLabel(self.signup_main_body, text='Please confirm your password: ',font=("Calibri",20))
        self.signup_main_body_label_3.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        newPasswordConfirm = StringVar()
        self.entryUserPwdConfirm = CTkEntry(self.signup_main_body, textvariable=newPasswordConfirm ,width=35)
        self.entryUserPwdConfirm.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.signUpBtn2 = CTkButton(self.signup_main_body, text='Ready!', command=signUp)
        self.signUpBtn2.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

class Chatbox(CTk):
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
            self.frame = CTkFrame(master=parent, width=width, height=height, corner_radius=corner_radius, border_color=border_color, border_width=border_width)
            self.frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
            return self.frame
        
        def create_label(self, parent, row, column, rowspan=1, columnspan=1, width=0, height=0, pady=(20, 0), padx=20, corner_radius=10, text='Label', anchor="w", font=('Calibri',20)):
            self.label = CTkLabel(master=parent, text=text, width=width, height=height, anchor=anchor, font=font)
            self.label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew", pady=pady, padx=padx)
            return self.label
        
        def create_button(self, parent, row, column, rowspan=1, columnspan=1, pady=(20,0), padx=20, text='Button', corner_radius=5, command=self.test):
            self.button = CTkButton(master=parent, text=text, command=command, corner_radius=corner_radius)
            self.button.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky="nsew")
            return self.button
        
        def create_option_menu(self, parent, row, column, rowspan=1, columnspan=1, pady=(20, 0), padx=20, values=[], command=self.test):
            self.option_menu = CTkOptionMenu(master=parent, values=values, command=command)
            self.option_menu.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky="nsew")
            return self.option_menu
        
        def create_textbook(self, parent, row, column, rowspan=1, columnspan=1, pady=(20, 0), padx=(0, 20), width=0, height=0, corner_radius=10, border_color='white', border_width=0):
            self.textbook = CTkTextbox(master=parent, width=width, height=height, corner_radius=corner_radius, border_color=border_color, border_width=border_width)
            self.textbook.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky="nsew")
            return self.textbook
        
        ### --- sidebar ---
        self.sidebar_frame = create_frame(self, self, 0, 0, rowspan=3, pady=0, corner_radius=0)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = create_label(self, self.sidebar_frame, 0, 0, text="Monogram", font=('Calibri',22))
        self.sidebar_button_1 = create_label(self, self.sidebar_frame, 1, 0, text=f'Hello, {usrName}!')
        #self.sidebar_button_2 = create_button(self, self.sidebar_frame, 2, 0, text='Profile', command=self.second_column_music_on)
        self.appearance_mode_label = create_label(self, self.sidebar_frame, 5, 0, text='Appearance Mode', font=('Calibri',14))
        self.appearance_mode_optionemenu = create_option_menu(self, self.sidebar_frame, 6, 0, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.scaling_label = create_label(self, self.sidebar_frame, 7, 0, text='UI Scaling:', font=('Calibri',14))
        self.scaling_optionemenu = create_option_menu(self, self.sidebar_frame, 8, 0, pady=(20, 20), values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)

        ### --- middle ---
        self.middle = create_frame(self, self, 0, 1)
        self.middle.grid_rowconfigure(4, weight=1)
        self.middle_button_1 = create_button(self, self.middle, 0, 0, text='Online Users', command=self.get_users)
        self.middle_button_2 = create_button(self, self.middle, 1, 0, text='Disconnect', command=self.disconnect)

        self.whoOnline = StringVar()
        self.users = create_label(self, self.middle, 2, 0, text="Here are online users! \nClick to chat with:", font=('Calibri',14))
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
        self.middle_label_1 = create_label(self, self.middle_bottom, 0, 0, text='Snake Game', font=('Calibri',14), anchor='n')
        self.middle_button_5 = create_button(self, self.middle_bottom, 1, 0, text='Play Snake', command=self.start_game)
        self.middle_button_6 = create_button(self, self.middle_bottom, 2, 0, text='Scoreboard', command=self.scoreboard)

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
        self.main_button_3 = create_button(self, self.main_buttons, 2, 4, text='Quit', command=self.quit)


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

        # updating
        def online_update():
            if client.sm.get_state() != S_OFFLINE:
                onlinedict=client.sm.whoOnLine
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
    def random_button(self):
        print("random_button clicked")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)

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
        self.whoOnline.set(whoOnlineList)

    def connectTo(self, event):
        connectToWhom =  self.whoListBox.get(self.whoListBox.curselection())
        print("double click")
        print(connectToWhom)
        if connectToWhom != client.name:
            client.console_input.append('c ' + connectToWhom)

        if client.sm.get_state() == S_CHATTING:
            client.console_input.append('bye')
            client.console_input.append('c ' + connectToWhom)

    def second_column_music_on(self):
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.play()
    
    def second_column_music_off(self):
        mixer.music.pause()

    def scoreboard(self):
        # pop up the sign up window on the top
        self.scoreboard_window = Toplevel(self)
        self.scoreboard_window.title('Scoreboard')
        self.scoreboard_window.geometry(f"{400}x{600}")
        self.scoreboard_window.resizable(False, False)

        # Column labels
        CTkLabel(self.scoreboard_window, text='#', width=120, height=25).grid(row=0, column=0)
        CTkLabel(self.scoreboard_window, text='Username', width=120, height=25).grid(row=0, column=1)
        CTkLabel(self.scoreboard_window, text='Highest Score', width=120, height=25).grid(row=0, column=2)

        # Load the data from the .pickle file
        with open('scoreboard.pickle', 'rb') as file:
            global scores
            scores = pickle.load(file)

        # Function to determine sort key
        def sort_key(item):
            username, score = item
            try:
                # Attempt to convert score to integer
                return (True, int(score))  # True means it's a valid integer, sort by negative value for descending order
            except ValueError:
                # Return False to put non-integers last, keep original order among non-integers
                return (False, 0)

        # Sort the scores dictionary by attempting to convert scores to integers, with alphabetic last
        sorted_scores = sorted(scores.items(), key=sort_key, reverse=True)

        # Display scores in the grid, adding a rank number
        for i, (username, score) in enumerate(sorted_scores, start=1):
            CTkLabel(self.scoreboard_window, text=str(i), width=120, height=25).grid(row=i, column=0)
            CTkLabel(self.scoreboard_window, text=username, width=120, height=25).grid(row=i, column=1)
            CTkLabel(self.scoreboard_window, text=str(score), width=120, height=25).grid(row=i, column=2)
    
    def load_score(self):
        # loading existing scores or initialize an empty dictionary
        print("Loading the score into .pickle")
        try:
            with open('scoreboard.pickle', 'rb') as pf:
                user_scores = pickle.load(pf)
        except (FileNotFoundError, EOFError):
            user_scores = {}  # creating if no file exists or file is empty

        # updating the score if the user exists and the new score is higher, or add new user
        if usrName in user_scores:
            if int(score) > int(user_scores[usrName]):
                user_scores[usrName] = score
                print(f"Updated score for {usrName} to {score}")
        else:
            user_scores[usrName] = score
            print(f"Added new user {usrName} with score {score}")

        # saving the updated dictionary back to the pickle file
        with open('scoreboard.pickle', 'wb') as pf:
            pickle.dump(user_scores, pf)

    def start_game(self):
        runpy.run_path(path_name='snake.py')
        print("Attempting to read score file...")
        try:
            with open('score.txt', 'r') as f:
                global score
                score = f.read().strip()
            print(f"Score: {score}")
            self.load_score()
        except:
            print("No score found.")


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

    def quit(self):
        client.quit()
        client.state = S_OFFLINE
        self.destroy()

    def refresh(self):
        while True:
            client.proc()
            if client.system_msg != '':
                m = client.system_msg
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
