import os
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle

from app.login_system_app.login import LoginApp
from app.login_system_app.register import RegisterApp


class StartApp(Tk):
    def __init__(self):
        """Start of application"""

        Tk.__init__(self)
        self.my_state = True

        # Attributes
        self.resizable(0, 0)
        self.title('Welcome')

        # themes
        self.style = ThemedStyle(self)
        self.style.theme_use('scidsand')
        # ('breeze', 'arc', 'adapta', 'radiance',
        # 'yaru', 'scidgrey')

        # set paths for file handling
        self.database = os.getcwd() + '\\database\\users.db'
        self.temp_files = os.getcwd() + '\\app\\login_system_app\\temp'

        # extra windows (login, register)
        # They wil both remain hidden (withdraw) unless they are called
        self.login = LoginApp(parent=self)
        self.login.withdraw()
        self.reg = RegisterApp(parent=self)
        self.reg.withdraw()

        self._frame = None

        # starting frame
        frame = StartWindow(self)
        frame.pack()


class StartWindow(Frame):
    def __init__(self, master):
        """Start window for app"""

        Frame.__init__(self, master)
        self.master = master

        # container
        self.scene = ttk.Frame(self)
        self.scene.pack()

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
        self.master.withdraw()
        self.master.login.deiconify()

    def register(self):
        """Displays registration window"""

        # We hide the start_app (withdraw),
        # and deiconify (unhide) the register system which was hidden
        self.master.withdraw()
        self.master.reg.deiconify()
