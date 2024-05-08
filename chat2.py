import tkinter
import tkinter.messagebox
import customtkinter

from pygame import mixer # for music on/off function
import time # for sending messages function

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()



        # configure window
        self.title("Monogram")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        ### --- left sidebar ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
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
        self.second_column_upper = customtkinter.CTkFrame(self)
        self.second_column_upper.grid(row=0,column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.button_1 = customtkinter.CTkButton(master=self.second_column_upper, text='Online Users', command=self.second_column_get_users)
        self.button_1.grid(row=1, column=0, padx=20, pady=10)
        self.button_2 = customtkinter.CTkButton(master=self.second_column_upper, text='Disconnect', command=self.second_column_disconnect)
        self.button_2.grid(row=2, column=0, padx=20, pady=10)
        self.label_1 = customtkinter.CTkLabel(self.second_column_upper, text="Online Users")
        self.label_1.grid(row=3, column=0, padx=20, pady=10)
        self.online_box = customtkinter.CTkFrame(self.second_column_upper, width=150)
        self.online_box.grid(row=4, column=0, padx=10, pady=10)
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
        self.message_container.grid(row=0, rowspan=2, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # buttons
        self.chat_box = customtkinter.CTkTextbox(self)
        self.chat_box.grid(row=2, column=2, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.button_7 = customtkinter.CTkButton(master=self.chat_box, text='Send', command=self.third_column_send)
        self.button_7.grid(row=2, column=0, pady=(10,0))
        self.button_8 = customtkinter.CTkButton(master=self.chat_box, text='Clear', command=self.third_column_clear)
        self.button_8.grid(row=2, column=1, pady=(10,0))


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
    def third_column_send(self):
        print("third_column_send clicked")

    def third_column_clear(self):
        print("third_column_clear clicked")

    
        message_list = customtkinter.CTkText(self.message_container, height = 30, bg = 'white', fg="black") # ---
        message_list.configure(state='disabled')
        message_list.tag_config('myMessage',foreground = 'blue') 
        txt_msgsend = customtkinter.CTkText(self.chat_box,height = 10)
        txt_msgsend.bind('<KeyPress-Return>',self.messages_send_event) 


if __name__ == "__main__":
    app = App()
    app.mainloop()