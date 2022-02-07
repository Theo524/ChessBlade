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

        self.closed = False
        self.mode = None
        # command button made for close window
        self.protocol("WM_DELETE_WINDOW", self.close_win)

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
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill='both')

    def close_win(self):
        """Close Window"""
        # win state
        self.closed = True

        # Set start_new_game to false
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no\n')
            f.write('saved_game:no')

        # close win
        self.destroy()


class StartWindow(ttk.Frame):
    def __init__(self, master, **kwargs):
        """Start window for app"""

        ttk.Frame.__init__(self, master, **kwargs)
        self.master = master

        # container
        self.scene = ttk.Frame(self)
        self.scene.pack()

        # themes
        self.master.style.configure('start_page.TButton', font=('Arial', 20))
        self.master.style.configure("Placeholder.TEntry", foreground='grey')

        # Title
        ttk.Label(self.scene, text="ChessBlade", font=('Arial', 50)).pack(side="top", padx=30, pady=50)

        # Login Button
        ttk.Button(self.scene, text="Login", command=lambda: master.switch_frame(master.frames['login']),
                   style='start_page.TButton', cursor='hand2').pack(pady=20, ipady=5, ipadx=10)

        # Registration button
        ttk.Button(self.scene, text="Register", command=lambda: master.switch_frame(master.frames['register']),
                   style='start_page.TButton', cursor='hand2').pack(pady=20, ipady=5, ipadx=10)

        # Guest mode button
        ttk.Button(self.scene, text="Enter as guest", command=self.set_mode_guest, style='start_page.TButton',
                   cursor='hand2').pack(pady=20, ipady=5, ipadx=10)

        # Just my name at the bottom
        Label(self.scene, text="Developed by Theo Brown",
              font=('Calibri', 10))\
            .pack()

    def set_mode_guest(self):
        """Sets the game mode"""

        # set the game mode 'guest' because user clicked 'enter as guest' button
        self.master.mode = 'guest'

        # Set start_new_game to true
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:yes\n')
            f.write('saved_game:no')

        # We quit the start_page and start_app to start the chess app in guest mode
        self.master.quit()
