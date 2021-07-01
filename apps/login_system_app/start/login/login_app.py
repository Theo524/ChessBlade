from tkinter import *
from .login_page import LoginSystem


class LoginApp(Toplevel):
    def __init__(self, parent):
        """Login Application container"""

        Toplevel.__init__(self)
        self._frame = None
        self.parent = parent

        # Attributes
        self.resizable(0, 0)
        self.title('Login')

        # database and temporal files paths
        self.database = self.parent.database
        self.temp_files = self.parent.temp_files

        # place 'LoginSystem' frame
        self.switch_frame(LoginSystem)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
