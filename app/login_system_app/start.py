import os
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle

from app.login_system_app.login import LoginSystem
from app.login_system_app.register import RegisterSystem


class StartApp(Tk):
    def __init__(self):
        """Starting application"""

        Tk.__init__(self)

        self.mode = None
        self.user_entered_game = False
        self.user_id = None

        # command button for window closing
        self.protocol("WM_DELETE_WINDOW", self.close_win)
        # center
        #self.eval('tk::PlaceWindow . center')  # center splash window

        # Attributes
        #self.geometry('500x600')
        self.title('Welcome')
        self.center()

        # themes
        self.style = ThemedStyle(self)
        self.style.theme_use('scidsand')

        # set paths for file handling
        self.database = os.getcwd() + '\\database\\users.db'
        self.temp_files = os.getcwd() + '\\app\\login_system_app\\temp'

        # frame
        self._frame = None
        self.frames = {'start': StartWindow, 'login': LoginSystem, 'register': RegisterSystem}

        # starting frame
        self._frame = StartWindow(self)
        self._frame.pack(expand=True, fill='both')

        # window icon
        self.tk.call('wm', 'iconphoto', self._w,
                     PhotoImage(file=os.getcwd() + '\\app\\resources\\img\\StartMenuIcon.png'))

        # automatically start application
        self.mainloop()

    def switch_frame(self, frame_class):
        """Change application display"""

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill='both')

    def go_to_start_page(self):
        """Set start menu page"""

        self.switch_frame(StartWindow)
        self.title('Welcome')

    def go_to_login(self):
        """Set login page"""

        self.switch_frame(LoginSystem)
        self.title('Login')

    def go_to_registration(self):
        """Set registration page"""

        self.switch_frame(RegisterSystem)
        self.title('Register')

    def close_win(self):
        """Close Window"""

        # user did not enter game
        self.user_entered_game = False

        # Set start_new_game to false
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no\n')
            f.write('saved_game:no')

        # close win
        self.destroy()

    def center(self):
        window_width = 800
        window_height = 500
        # get the screen size of your computer [width and height using the root object as foolows]
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Get the window position from the top dynamically as well as position from left or right as follows
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        # this is the line that will center your window
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')


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
        ttk.Button(self.scene, text="Login", command=self.master.go_to_login,
                   style='start_page.TButton', cursor='hand2').pack(pady=20, ipady=5, ipadx=10)

        # Registration button
        ttk.Button(self.scene, text="Register", command=self.master.go_to_registration,
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
        self.master.user_entered_game = True

        # Set start_new_game to true
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:yes\n')
            f.write('saved_game:no')

        # We quit the start_page and start_app to start the chess app in guest mode
        self.master.destroy()