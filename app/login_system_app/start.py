import os
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle

from app.login_system_app.login import LoginSystem
from app.login_system_app.register import RegisterSystem


class StartApp(Tk):
    def __init__(self):
        """Start of application"""

        Tk.__init__(self)
        self.my_state = True

        # Attributes
        #self.resizable(0, 0)
        self.geometry('1000x620')
        self.title('Welcome')

        # themes
        self.style = ThemedStyle(self)
        self.style.theme_use('scidsand')

        # set paths for file handling
        self.database = os.getcwd() + '\\database\\users.db'
        self.temp_files = os.getcwd() + '\\app\\login_system_app\\temp'

        self._frame = None

        self.frames = {'start': StartWindow, 'login': LoginSystem, 'register': RegisterSystem}

        # starting frame
        self.switch_frame(self.frames['start'])

    def switch_frame(self, frame_class):
        new_frame = frame_class(self, width=1000, height=620)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill='both')


class StartWindow(ttk.Frame):
    def __init__(self, master, **kwargs):
        """Start window for app"""

        ttk.Frame.__init__(self, master, **kwargs)
        self.master = master

        # container
        self.scene = ttk.Frame(self)
        self.scene.pack(pady=110)

        # themes
        self.master.style.configure('start_page.TButton',
                                    font=('Arial', 15))
        self.master.style.configure("Placeholder.TEntry",
                                    foreground='grey')

        # Title
        ttk.Label(self.scene, text="CHESS GAME",
                  font=('Arial', 30))\
            .pack(side="top", padx=30, pady=15)

        # Login Button
        ttk.Button(self.scene, text="Login",
                    command=self.login,
                   style='start_page.TButton')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Registration button
        ttk.Button(self.scene, text="Register",
                   command=self.register,
                   style='start_page.TButton')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Guest mode button
        ttk.Button(self.scene, text="Enter as guest",
                   command=self.set_mode_guest,
                   style='start_page.TButton')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Just my name at the bottom
        Label(self.scene, text="Developed by Theo Brown",
              font=('Calibri', 10))\
            .pack()

    def set_mode_guest(self):
        """Sets the game mode"""

        mode_file = self.master.temp_files + '\\mode.txt'
        # Write the game mode 'guest' because user clicked 'enter as guest' button
        with open(mode_file, 'w') as f:
            f.write('guest')

        # We quit the start_page and start_app to start the chess app in guest mode
        self.master.my_state = False
        self.master.quit()

    def login(self):
        """Displays login window"""

        # We hide the start_app (withdraw), and
        # deiconify (unhide) the login system which was hidden
        # place 'LoginSystem' frame
        self.master.switch_frame(self.master.frames['login'])

    def register(self):
        """Displays registration window"""

        # We hide the start_app (withdraw),
        # and deiconify (unhide) the register system which was hidden
        self.master.switch_frame(self.master.frames['register'])
