from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle


class StartWindow(Frame):
    def __init__(self, master):
        """Start window for app"""

        Frame.__init__(self, master)
        self.master = master

        # themes
        self.master.style.configure('start_page.TButton', font=('Arial', 15))

        # Title
        ttk.Label(self, text="CHESS GAME", font=('Arial', 30)).pack(side="top", padx=30, pady=15)

        # Login Button
        ttk.Button(self, text="Login", command=self.login, style='start_page.TButton').pack(pady=20, ipady=5, ipadx=10)

        # Registration button
        ttk.Button(self, text="Register", command=self.register, style='start_page.TButton')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Guest mode button
        ttk.Button(self, text="Enter as guest", command=self.set_mode_guest, style='start_page.TButton')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Just my name at the bottom
        Label(self, text="Developed by Theo Brown", font=('Calibri', 10))\
            .pack()

    def set_mode_guest(self):
        """Sets the game mode"""

        mode_file = self.master.temp_files + '//mode.txt'
        # Write the game mode 'guest' because user clicked 'enter as guest' button
        with open(mode_file, 'w') as f:
            f.write('guest')

        # We quit the start_page and start_app to start the chess app in guest mode
        self.master.my_state = False
        self.master.quit()

    def login(self):
        """Displays login window"""

        # We hide the start_app (withdraw), and deiconify (unhide) the login system which was hidden
        self.master.withdraw()
        self.master.login.deiconify()

    def register(self):
        """Displays registration window"""

        # We hide the start_app (withdraw), and deiconify (unhide) the register system which was hidden
        self.master.withdraw()
        self.master.reg.deiconify()
