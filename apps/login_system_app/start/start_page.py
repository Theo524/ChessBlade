from tkinter import *


class StartWindow(Frame):
    def __init__(self, master):
        """Start window for app"""

        Frame.__init__(self, master)
        self.master = master

        # Title
        Label(self, text="CHESS GAME", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5, padx=20)

        # Login Button
        Button(self, text="Login", font=('Helvetica', 15), command=self.login)\
            .pack(pady=15)

        # Registration button
        Button(self, text="Register", font=('Helvetica', 15), command=self.register)\
            .pack(pady=15)

        # Guest mode button
        Button(self, text="Enter as guest", font=('Helvetica', 15), command=self.set_mode_guest)\
            .pack(pady=15, padx=30)

        # Just my name at the bottom
        Label(self, text="Developed by Theo Brown", font=('Calibri', 7))\
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
