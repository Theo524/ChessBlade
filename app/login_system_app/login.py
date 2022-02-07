import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
from app.login_system_app.register import RegisterSystem
from app.resources.custom_widgets.placeholder_entry import PlaceholderEntry
import hashlib
import smtplib
import random
import sqlite3
import requests
from database.database import DatabaseBrowser


class LoginSystem(ttk.Frame):
    """Login to account"""

    def __init__(self, master, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        # themes
        self.master.style.configure('login_page.TButton', font=('Calibri', 13,))
        self.master.style.configure('login_page.TCheckbutton', font=('Calibri', 10))

        # window attributes
        self.master.title('Login')

        # container
        self.scene = ttk.Frame(self)
        self.scene.pack(pady=100)

        # files needed
        self.database = self.master.database
        self.temp_files = self.master.temp_files

        # ----------------------app layout/upper frame----------------------
        self.upper_window = ttk.Frame(self.scene, height=50, width=300)
        self.upper_window.pack()
        # button to return to start page
        ttk.Button(self.upper_window, text='<--', cursor="hand2",
                   command=self.return_to_start).place(x=0, y=0)

        # ----------------------app layout/middle frame(main data)----------------------
        # every item is placed inside this frame
        self.main_window = ttk.Frame(self.scene)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        pic = PhotoImage(file=os.getcwd() + '\\app\\resources\\img\\login_icon.png')
        self.title_frame = ttk.Frame(self.main_window)
        self.title_frame.pack(pady=10)
        image_title = Label(self.title_frame, image=pic)
        image_title.pack()
        image_title.image = pic

        # Username (MIDDLE FRAME)
        self.username_frame = ttk.Frame(self.main_window)
        self.username_frame.pack(pady=20)

        self.user_name_var = StringVar()
        self.username_entry = PlaceholderEntry(self.username_frame, 'Username',textvariable=self.user_name_var)
        self.username_entry.pack(expand=True, side=LEFT, padx=10, ipadx=10)

        # Password (MIDDLE FRAME)
        self.password_frame = ttk.Frame(self.main_window)
        self.password_frame.pack(pady=10)

        self.password_var = StringVar()
        self.password_entry = PlaceholderEntry(self.password_frame, 'Password',
                                               textvariable=self.password_var, show="")
        self.password_entry.pack(expand=True, side=LEFT, padx=10, ipadx=10)

        # Extra/additional settings - 'forgotten password', 'show password' (MIDDLE FRAME)
        self.extra = ttk.Frame(self.main_window)
        self.extra.pack()
        # Show/hide password
        self.show_password_var = IntVar()
        self.show_password = ttk.Checkbutton(self.extra, text='Show password', style='login_page.TCheckbutton',
                                         variable=self.show_password_var, onvalue=1, offvalue=0,
                                         command=self.show, cursor="hand2")
        self.show_password.pack(side=LEFT, padx=30)
        # Forgot password
        self.forgot_password = Label(self.extra, text='Forgot your password?', fg='blue', bg='#dadada',
                                      font=('Calibri', 9, 'italic'), cursor="hand2")

        self.forgot_password.bind("<Button-1>", lambda e: self.master.switch_frame(ForgotPassword))
        self.forgot_password.pack(side=LEFT)

        # Login button (MIDDLE FRAME)
        self.login_frame = ttk.Frame(self.main_window)
        self.login_frame.pack(pady=20)
        self.login_button = ttk.Button(self.login_frame, text='Login', command=self.verify_credentials,
                                       style='login_page.TButton', cursor="hand2")
        self.login_button.pack(ipady=3, ipadx=15)

        # ----------------------app layout/lower frame----------------------
        self.lower_window = ttk.Frame(self.scene, height=20)
        self.lower_window.pack()

    def return_to_start(self):
        """Return to start app"""

        # Hide current app(LoginSystem), deiconify (unhide) 'StartApp'
        self.master.title('Welcome')
        self.master.switch_frame(self.master.frames['start'])

    def show(self):
        """Show or hide password entry"""

        # if the checkbutton is activated, reveal password
        if self.show_password_var.get() == 1:
            self.password_entry.config(show='')

        # if the checkbutton is deactivated, hide password with asterisks '*'
        else:
            self.password_entry.config(show='*')

    def verify_credentials(self):
        """Check password and username are valid"""

        # Get username and password
        username = self.user_name_var.get().lower()
        password = self.password_var.get()

        # Hash password
        message = password.encode()
        user_hashed_password = hashlib.blake2b(message).hexdigest()

        # search for hashed password and username in database
        found = self.check_data(username, user_hashed_password)

        # Check whether the account was found
        if found:
            # feedback
            messagebox.showinfo('Success', 'Successful login')

            user_file = self.temp_files + '//current_user.txt'

            # save username to temp files
            with open(user_file, 'w') as f:
                f.write(username)

            # Set start_new_game to true
            with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
                f.write('new_game:yes\n')
                f.write('saved_game:no')

            # set game mode as user
            self.master.mode = 'user'
            # quit the login system
            self.master.close_win()

        else:
            # feedback for invalid data
            messagebox.showerror('Error', 'Invalid credentials')

    def check_data(self, username, h_password):
        """Check credentials are in db"""

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        with conn:
            # sql query to get all usernames and passwords that match the function parameters
            c.execute("SELECT * FROM users WHERE username=:username AND password=:password",
                      {'username': username, 'password': h_password})

            # the data, should only be one tuple containing 2 items
            data = c.fetchall()

            # If there are any values in 'data' it means there is a match with the execute statement from c
            if data:
                return True

            else:
                return False


class ForgotPassword(ttk.Frame):
    """Start for password recovery"""

    def __init__(self, master, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        self.database = self.master.database
        self.temp_files = self.master.temp_files

        self.master.style.configure('error_label.TLabel', foreground='red', font=('Arial', 7))

        # container
        self.scene = ttk.Frame(self)
        self.scene.pack(pady=100)

        # ---------------------App layout/upper frame---------------------
        self.upper_window = ttk.Frame(self.scene, height=50, width=300)
        self.upper_window.pack()
        ttk.Button(self.upper_window, text='<--',
               command=lambda: self.master.switch_frame(LoginSystem), cursor='hand2').place(x=0, y=0)

        # ---------------------App layout/middle frame---------------------
        self.main_window = ttk.Frame(self.scene)
        self.main_window.pack()

        # change title
        self.master.title('Recover password')

        # Title (MIDDLE FRAME)
        self.title_frame = ttk.Frame(self.main_window)
        self.title_frame.pack()
        ttk.Label(self.title_frame, text='Recover password', font='arial 20').pack(expand=True)

        # Info
        self.info_frame = ttk.Frame(self.main_window)
        self.info_frame.pack(pady=10)
        ttk.Label(self.info_frame, text='To recover your password,', font='arial 10').pack(expand=True)
        ttk.Label(self.info_frame, text='Enter your username and the email address', font='arial 10').pack(expand=True)
        ttk.Label(self.info_frame, text='You registered with.',  font='arial 10').pack(expand=True)
        ttk.Label(self.info_frame, text='A passcode will be sent to this account', font='arial 10').pack(expand=True)

        # Recover password (MIDDLE FRAME)
        # All data is placed on this frame
        self.recover_password_frame = ttk.Frame(self.main_window)
        self.recover_password_frame.pack(pady=10)

        # Username
        self.user_frame = ttk.Frame(self.recover_password_frame)
        self.user_frame.pack(pady=3)

        self.user_recover_password_var = StringVar()
        self.user_recover_password_entry = PlaceholderEntry(self.user_frame, 'Username', textvariable=self.user_recover_password_var)
        self.user_recover_password_entry.pack(expand=True)

        # Email
        self.email_frame = ttk.Frame(self.recover_password_frame)
        self.email_frame.pack()

        self.email_recover_password_var = StringVar()
        self.email_recover_password_entry = PlaceholderEntry(self.email_frame, 'Email address',
                                                  textvariable=self.email_recover_password_var)
        self.email_recover_password_entry.pack(expand=True)

        # error display frame
        self.recover_password_error_frame = ttk.Frame(self.main_window)
        self.recover_password_error_frame.pack()
        self.recover_password_error_var = StringVar()
        self.recover_password_error = ttk.Label(self.recover_password_error_frame,
                                                textvariable=self.recover_password_error_var,
                                                style='error_label.TLabel')

        # Verification button (MIDDLE FRAME)
        ttk.Button(self.main_window, text='Continue', cursor='hand2', command=self.get_email).pack()

        # ---------------------App layout/lower frame---------------------
        self.lower_frame = ttk.Frame(self.scene, height=50)
        self.lower_frame.pack()

    def check_email_in_db(self):
        """Check whether the email entered is in database"""

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        with conn:

            # our data
            email = self.email_recover_password_var.get()
            user = self.user_recover_password_var.get()

            # collect email and username matches from db
            # data should be a tuple of 3 values, if there is a match
            c.execute("SELECT * FROM users WHERE username=:user AND email=:email", {'user': user, 'email': email})
            data = c.fetchall()

            # If there are any values in 'data' it means there is a match with the execute statement from c
            if data:
                in_database = True
            else:
                in_database = False

        # if the data is in the database, we send the email verification
        if in_database:
            # Generate 4 digit random number
            code = [str(random.randint(0, 10)) for _ in range(4)]
            passcode = ''.join(code)

            # Send passcode to user email
            successfully_sent_email = self.send_email(passcode, email, user)

            if successfully_sent_email:
                # if email exists, we store passcode in temporal file
                passcode_file = self.temp_files + '\\password_recovery\\passcode.txt'
                with open(passcode_file, 'w') as f:
                    f.write(passcode)

                # write username to temp_file
                user_file = self.temp_files + '\\password_recovery\\username.txt'
                with open(user_file, 'w') as f:
                    f.write(user.lower())

                # get password for that user
                conn = sqlite3.connect(self.database)
                c = conn.cursor()

                with conn:
                    c.execute('SELECT * FROM users WHERE username=:username',
                              {'username': user.lower(),})

                    data = c.fetchall()
                    # format of data is [(username, password, email)] so 'my_list[0][1]' represents the password
                    password = data[0][1]

                # write password to temp files
                password_file = self.temp_files + '//password.txt'
                with open(password_file, 'w') as f:
                    f.write(password)

                # if nothing went wrong, the message has been sent
                return True

            else:
                return False

    def send_email(self, passcode, email, user):
        """Send email message to an account"""

        valid = self.validate(email)
        if valid:
            try:
                # Send passcode to user email
                receiver_address = email
                subject = "Passcode verification"
                body = f"Hello {user}!\nHere is your passcode\n{passcode}\nWith regards,\n\nChessMaster"

                # Endpoint for the SMTP Gmail server
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.ehlo()
                smtp_server.starttls()

                # Login with dummy Gmail account I created using SMTP
                smtp_server.login("chessblade.info@gmail.com", "chessblade1234")

                # Let's combine the subject and the body onto a single message
                message = f"Subject: {subject}\n\n{body}"

                # We'll be sending this message in the above format (Subject:...\n\nBody)
                smtp_server.sendmail("pruebadelogin524@gmail.com", [receiver_address], message)

                # Close our endpoint
                smtp_server.close()

            except smtplib.SMTPAuthenticationError:
                # if the email does not work return false
                return False

            else:
                return True
        else:
            return False

    @staticmethod
    def validate(email):
        """Check whether a email account exists"""

        email_address = email

        # get response from website api
        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
            params={'email': email_address})

        # actual response
        status = response.json()['status']

        if status == 'valid':
            return True

        else:
            return False

    def get_email(self):
        """Retrieve email input from user"""

        # Check if it valid
        valid = self.check_email_in_db()

        # If it is valid, we move to the next window
        if valid:
            self.master.switch_frame(VerifyPasscode)

        else:
            # if the email is invalid we add a warning message
            self.recover_password_error_frame.pack()
            self.recover_password_error.pack(pady=(0, 10))
            self.recover_password_error_var.set("Invalid data (Make sure you have created an account previously)")
            messagebox.showerror('Error', 'The data you entered is invalid')


class VerifyPasscode(ttk.Frame):
    """Receive sent passcode and verify"""

    def __init__(self, master, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        self.temp_files = self.master.temp_files

        # window attributes
        self.master.title('Recover password')

        # ---------------------App layout/upper frame---------------------
        self.upper_window = ttk.Frame(self, height=50, width=350)
        self.upper_window.pack()
        ttk.Button(self.upper_window, text='<--', cursor='hand2',
               command=self.return_to_login).place(x=0, y=0)

        # ---------------------App layout/middle frame---------------------
        self.main_window = ttk.Frame(self)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = Frame(self.main_window)
        self.title_frame.pack()

        ttk.Label(self.title_frame, text='Passcode sent', font='arial 20').pack(expand=True)

        # Passcode (MIDDLE FRAME)
        ttk.Label(self.main_window, text='Check your email,',font='arial 9').pack(pady=(10, 0))
        ttk.Label(self.main_window, text='A passcode has been sent.',font='arial 9').pack()
        ttk.Label(self.main_window, text='Enter the passcode below', font='arial 9').pack()

        self.passcode_var = StringVar()
        self.passcode_entry = ttk.Entry(self.main_window, textvariable=self.passcode_var)
        self.passcode_entry.pack(expand=True, pady=10)
        ttk.Button(self.main_window, text='Continue', cursor='hand2',
                   command=self.check_passcode).pack(expand=True)

        # ----------------------app layout/lower frame----------------------
        self.lower_window = ttk.Frame(self)
        self.lower_window.pack(ipady=10)

    def return_to_login(self):
        """Return to Login page"""

        self.master.switch_frame(LoginSystem)

    def check_passcode(self):
        """Check if the passcode is correct"""

        # Get passcode from file
        passcode_file = self.temp_files + '\\password_recovery\\passcode.txt'
        with open(passcode_file, 'r') as f:
            stored_passcode = f.read()

        # check if the passcode is correct
        if self.passcode_var.get() == stored_passcode:
            messagebox.showinfo('Valid', 'Correct passcode has been entered')
            # if it is switch to the next frame
            self.master.switch_frame(NewPassword)
        else:
            messagebox.showerror('Error', 'Incorrect passcode')


class NewPassword(ttk.Frame):
    """Create new password"""

    def __init__(self, master):
        ttk.Frame.__init__(self, master)


        # files
        self.database = self.master.database
        self.temp_files = self.master.temp_files

        # ---------------------App layout/upper frame---------------------
        self.upper_window = ttk.Frame(self, height=50, width=350)
        self.upper_window.pack()
        ttk.Button(self.upper_window, text='<--', cursor='hand2',
                   command=self.start).place(x=0, y=0)

        # ---------------------App layout/middle frame---------------------
        self.main_window = ttk.Frame(self)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = ttk.Frame(self.main_window)
        self.title_frame.pack()

        ttk.Label(self.title_frame, text='Success!', font='arial 20').pack(expand=True)

        # Passcode (MIDDLE FRAME)
        ttk.Label(self.main_window, text='Enter your new password here.',
              font='arial 7 bold italic').pack(pady=10)

        self.new_pass_var = StringVar()
        self.new_pass_entry = PlaceholderEntry(self.main_window, 'New password', textvariable=self.new_pass_var, show='')
        self.new_pass_entry.pack(expand=True, pady=10)

        self.show_pass_var = IntVar()
        self.show_password = ttk.Checkbutton(self.main_window, text='Show Password',
                                             variable=self.show_pass_var, command=self.show, onvalue=1, offvalue=0,
                                             cursor='hand2')
        self.show_password.pack(side=LEFT, padx=30)

        ttk.Button(self.main_window, text='continue', cursor='hand2', command=self.set_new_pass).pack(expand=True)

        # ----------------------app layout/lower frame----------------------
        self.lower_window = ttk.Frame(self, height=20)
        self.lower_window.pack()

    def show(self):
        """Show or hide password entry"""

        # if the checkbutton is activated, reveal password
        if self.show_pass_var.get() == 1:
            self.new_pass_entry.config(show='')

        else:
            self.new_pass_entry.config(show='*')

    def set_new_pass(self):
        """set new password"""

        password = self.new_pass_var.get()

        valid = RegisterSystem.check_pass(password)

        if valid:
            # convert password
            new_pass = RegisterSystem.hash_pass(password)

            user_file = self.temp_files + '\\password_recovery\\username.txt'
            with open(user_file, 'r') as f:
                username = f.read()

            password_file = self.temp_files + '\\password_recovery\\password.txt'
            with open(password_file, 'r') as f:
                old_pass = f.read()

            # get old data to get email
            data = DatabaseBrowser.load(load='general', username=username)

            # make new data
            all_data = [username, new_pass, data[2]]

            # save new data
            DatabaseBrowser.save(save='general', username=username, data=all_data)

            messagebox.showinfo('Success', 'Your new password has been set')
            # Return to login
            self.master.switch_frame(LoginSystem)

        else:
            messagebox.showerror('Error', 'The password should contain 2 of each:\n- Upper case leters'
                                 '\n- Lower case letters\n- Numbers\n- Symbols')

    def start(self):
        """Return to Login page"""
        self.master.title('Login')
        self.master.switch_frame(LoginSystem)
