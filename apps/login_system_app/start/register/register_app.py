from tkinter import *
from .register_page import RegisterSystem


class RegisterApp(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self)
        self._frame = None
        self.database = parent.database

        # sets current frame to 'RegisterSystem', a class(Frame) from the 'register_page' file
        self.switch_frame(RegisterSystem)
        self.parent = parent

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()