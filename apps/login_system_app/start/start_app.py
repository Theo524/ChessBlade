from tkinter import *
from .start_page import StartWindow
from .login.login_app import LoginApp
from .register.register_app import RegisterApp
import os
from tkinter import ttk
from ttkthemes import ThemedStyle



class StartApp(Tk):
    def __init__(self):
        """Start of application"""

        Tk.__init__(self)
        self.my_state = True

        #themes
        self.style = ThemedStyle(self)
        #themes = style.get_themes()
        #themes.sort()
        #my_theme = themes[-1]
        self.style.set_theme('breeze')
        # ('breeze', 'arc', 'adapta', 'radiance', 'yaru')

        # set paths for file handling
        self.database = os.getcwd() + '\\database\\users.db'
        self.temp_files = os.getcwd() + '\\apps\\login_system_app\\temp'

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

    def switch_frame(self, frame_class):
        """Change the current frame"""

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def run(self):
        self.mainloop()
