from tkinter import *
from ttkthemes import ThemedStyle

from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from app.resources.custom_widgets.placeholder_entry import PlaceholderEntry

import hashlib
import string
import smtplib
import sqlite3


class RegisterSystem(ttk.Frame):
    def __init__(self, master, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        self.database = self.master.database

        self.master.style.configure('error_label.TLabel', foreground='red', font=('Arial', 7))
        # container
        self.scene = ttk.Frame(self)
        self.scene.pack(pady=100)

        # ----------------------App layout/upper frame----------------------
        self.upper_window = ttk.Frame(self.scene, height=50, width=350)
        self.upper_window.pack()
        # Button to return to start page
        ttk.Button(self.upper_window, text='<--',
               command=self.return_to_start, cursor='hand2').place(x=0, y=0)

        # ----------------------App layout/middle frame----------------------

        # All the widgets are placed here
        # This frame will consist of more frames
        # Every frame will have a label an entry and an error frame (highlighted in red)
        self.main_window = ttk.Frame(self.scene)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = ttk.Frame(self.main_window)
        self.title_frame.pack(pady=(0, 20))
        ttk.Label(self.title_frame, text='CREATE ACCOUNT', font='arial 20').pack(expand=True)

        # New username (MIDDLE FRAME)
        self.new_user_frame = ttk.Frame(self.main_window)
        self.new_user_frame.pack(pady=10)

        # Username
        self.new_user_name_var = StringVar()
        self.new_username_entry = PlaceholderEntry(self.new_user_frame, 'New Username',
                                                   textvariable=self.new_user_name_var)

        self.new_username_entry.pack(expand=True, ipadx=15)

        self.new_user_name_error_frame = ttk.Frame(self.main_window, height=1)
        self.new_user_name_error_frame.pack()
        self.new_user_name_error_var = StringVar()
        self.new_user_name_error = ttk.Label(self.new_user_name_error_frame, textvariable=self.new_user_name_error_var,
                                             style='error_label.TLabel')

        # New password (MIDDLE FRAME)
        self.new_password_frame = ttk.Frame(self.main_window)
        self.new_password_frame.pack(pady=10)

        #Label(self.new_password_frame, text='New password\t ').pack(expand=True, side=LEFT)
        self.new_password = StringVar()
        self.new_password_entry = PlaceholderEntry(self.new_password_frame, 'New Password', textvariable=self.new_password)
        self.new_password_entry.pack(expand=True, ipadx=15)

        self.password_error_frame = ttk.Frame(self.main_window, height=1)
        self.password_error_frame.pack()
        self.password_error_var = StringVar()
        self.password_error = ttk.Label(self.password_error_frame, textvariable=self.password_error_var,
                                        style='error_label.TLabel')

        # Confirm new password (MIDDLE FRAME)
        self.confirm_password_frame = ttk.Frame(self.main_window)
        self.confirm_password_frame.pack(pady=10)

        self.confirmed_password = StringVar()
        self.confirmed_password_entry = PlaceholderEntry(self.confirm_password_frame, 'Confirm password',
                                                         textvariable=self.confirmed_password)
        self.confirmed_password_entry.pack(expand=True, ipadx=15)

        self.confirmed_password_error_frame = ttk.Frame(self.main_window, height=1)
        self.confirmed_password_error_frame.pack()
        self.confirmed_password_error_var = StringVar()
        self.confirmed_password_error = ttk.Label(self.confirmed_password_error_frame,
                                                  textvariable=self.confirmed_password_error_var,
                                                  style='error_label.TLabel')

        # Email (MIDDLE FRAME)
        self.email_frame = ttk.Frame(self.main_window)
        self.email_frame.pack(pady=10)

        self.email_var = StringVar()
        self.email_address_entry = PlaceholderEntry(self.email_frame, 'Email address (@gmail.com)', textvariable=self.email_var)
        self.email_address_entry.pack(expand=True, ipadx=15)

        self.email_error_frame = ttk.Frame(self.main_window, height=1)
        self.email_error_frame.pack()
        self.email_error_var = StringVar()
        self.email_error = ttk.Label(self.email_error_frame, textvariable=self.email_error_var,
                                     style='error_label.TLabel')

        # Date of birth (MIDDLE FRAME)
        self.dob_frame = ttk.Frame(self.main_window)
        self.dob_frame.pack(pady=10)

        self.dob_entry = DateEntry(self.dob_frame, date_pattern='dd/MM/yyyy', width=17, bg="darkblue")
        self.dob_entry.pack(expand=True)

        self.dob_error_frame = ttk.Frame(self.main_window, height=1)
        self.dob_error_frame.pack()
        self.dob_error_var = StringVar()
        self.dob_error = ttk.Label(self.dob_error_frame, textvariable=self.dob_error_var,
                                   style='error_label.TLabel')

        # Register all details (MIDDLE FRAME)
        self.save_data_frame = ttk.Frame(self.main_window)
        self.save_data_frame.pack(pady=10)

        self.save_button = ttk.Button(self.save_data_frame, text='Save', command=self.store_data, cursor='hand2')
        self.save_button.pack()

        # ----------------------App layout/lower frame----------------------
        self.lower_frame = ttk.Frame(self.scene, height=50)
        self.lower_frame.pack()

    def return_to_start(self):
        """Returns to the start page"""

        # Withdraw current 'LoginApp' and deiconify 'StartApp'
        self.master.switch_frame(self.master.frames['start'])

    @staticmethod
    def check_email(email):
        """Checks whether the email account user entered exists"""
        print(email)

        try:
            # Receiver email address
            receiver_address = email

            # Our message
            subject = "Welcome"
            body = f"Greetings from ChessMaster\n\nYour account has been successfully registered!" \
                   f"\nWe look forward to working with you," \
                   f"\n\nChessMaster,"

            # Combine the subject and the body onto a single message
            message = f"Subject: {subject}\n\n{body}"

            # Endpoint for the SMTP Gmail server
            smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

            # Login with a dummy email account I created
            smtp_server.login("pruebadelogin524@gmail.com", "logintest1234")

            # Message sent in the above format (Subject:...\n\nBody) from my dummy email account
            smtp_server.sendmail("pruebadelogin524@gmail.com", receiver_address, message)

            # Close our endpoint
            smtp_server.close()

            # if nothing went wrong it means the email account exists
            exists = True

        except smtplib.SMTPRecipientsRefused:
            # if an exception occurs, the account doesn't exist
            # The name of the exception is unclear and I do not know how to write it, hence I just use 'except'
            exists = False

        # We return whether the email account exists
        return exists

    @staticmethod
    def calculate_age(dob):
        """Calculate the user age"""

        # get today's date
        today = date.today()

        # convert the age string into a list
        born = dob.split('/')
        date_of_birth = date(int(born[2]), int(born[1]), int(born[0]))

        # operation that calculates the difference between today and the birthdate (age)
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    @staticmethod
    def hash_pass(password):
        """Hash the password for better security"""

        # password hashing
        message = password.encode()
        hashed_password = hashlib.blake2b(message).hexdigest()

        # Return result
        return hashed_password

    @staticmethod
    def check_pass(password):
        """Check if the password meets the requirements"""

        # Characters the password must contain
        # Upper case letters, lower case letters, symbols and numbers are a requirement
        alpha = list(string.ascii_uppercase)
        lower = list(string.ascii_lowercase)
        numbers = [str(number) for number in range(11)]
        symbols = list('`¦¬!\"£$€%^&*()_+=-[]#\',./{}~@<>?|\\:')

        # variables for the check
        is_len = False
        is_alpha = 0
        is_lower = 0
        is_num = 0
        is_special = 0

        # Check the length is appropriate (between 8 and 20 chars)
        if 8 <= len(password) <= 20:
            is_len = True

        # for loop checks each character in the password to find a match
        for letter in password:
            if letter in alpha:
                is_alpha += 1

            if letter in lower:
                is_lower += 1

            if letter in numbers:
                is_num += 1

            if letter in symbols:
                is_special += 1

        # if all requirements are met return true, else give false
        if is_len and is_alpha >= 2 and is_lower >= 2 and is_num >= 2 and is_special >= 2:
            # password is valid
            return True

        else:
            # password is invalid
            return False

    def username_in_database(self, username):
        """Ensure only unique usernames are stored in databse"""

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        with conn:
            c.execute("SELECT * FROM users")

            data = c.fetchall()

            # if username is in database return True, else False
            for val in data:
                if username == val[0]:
                    return True
                else:
                    continue

            return False

    def store_data(self):
        """Store the data in the database after checking it all"""

        requirements_met = 0

        # Check if username is valid
        username = self.new_user_name_var.get().lower()
        if 3 > len(username) or len(username) > 20:
            # if invalid, display error frame
            self.new_user_name_error_var.set('Username must be between 3-20 characters')
            self.new_user_name_error.pack(expand=True)
        else:
            # If the username has appropriate length, check if it is in the database
            if self.username_in_database(username):
                self.new_user_name_error_var.set('Username already exists')
                self.new_user_name_error.pack(expand=True)

            else:
                # if valid increase requirements met count and delete error frame
                requirements_met += 1
                self.new_user_name_error.pack_forget()

        # Check if password is valid
        password = self.new_password.get()
        confirmed_password = self.confirmed_password.get()
        if not self.check_pass(password):
            # if invalid, display error frame
            self.password_error_var.set('Password requisites: 8-20 characters, 2 - symbols, numbers, upper, lower')
            self.password_error.pack(expand=True)
        else:
            # if valid increase requirements met count and delete error frame
            requirements_met += 1
            self.password_error.pack_forget()

            # After checking if the password is valid, check if passwords match
            if password != confirmed_password:
                # if they do not match , display alert message
                self.confirmed_password_error_var.set('Passwords do not match')
                self.confirmed_password_error.pack(expand=True)
            else:
                # if they match increase requirement count and delete error frame
                requirements_met += 1
                self.confirmed_password_error.pack_forget()

        # Check if email is valid
        email = self.email_var.get()
        if not self.check_email(email):
            # if invalid, display error frame
            self.email_error_var.set("Invalid email address")
            self.email_error.pack(expand=True)
        else:
            # if valid increase requirements met and delete error frame
            requirements_met += 1
            self.email_error.pack_forget()

        # Check date of birth is valid (age between 14-70)
        date_of_birth = self.dob_entry.get()
        age = self.calculate_age(date_of_birth)
        if age < 14 or age > 100:
            # if invalid, display error frame
            self.dob_error_var.set('You must be between 14-100 years of age')
            self.dob_error.pack()
        else:
            # if valid increase requirements met and delete error frame
            requirements_met += 1
            self.dob_error.pack_forget()

        # Verify that all 5 requirements were met
        if requirements_met == 5:
            # Store data into database
            conn = sqlite3.connect(self.database)
            c = conn.cursor()

            with conn:
                # Insert values into the database (general)
                c.execute("INSERT INTO users VALUES (:username, :password, :email)",
                          {'username': username.lower(),
                           'password': self.hash_pass(password),
                           'email': email})

                # Insert values into the database (settings)
                c.execute("INSERT INTO user_settings VALUES (:user, :difficulty, :time, :game_type, "
                          ":player_piece_color, :opponent_piece_color, :border_color, :board_color)",
                          {'user': username.lower(), 'difficulty': 'medium', 'time': '02:30:00',
                           'game_type': 'two_player', 'player_piece_color': 'black', 'opponent_piece_color': 'white',
                           'border_color': 'black', 'board_color': 'brown'})

                # Insert values into the database (statistics)
                c.execute("INSERT INTO user_stats VALUES (:user, :number_of_games_played, :wins, :loses, "
                          ":draws, :ranking)",
                          {'user': username.lower(), 'number_of_games_played': 0, 'wins': 0,
                           'loses': 0, 'draws': 0, 'ranking': 0})

                # output database to console
                c.execute("SELECT * FROM users")
                print(f'User data: {c.fetchall()}')
                c.execute("SELECT * FROM user_settings")
                print(f'User settings: {c.fetchall()}')
                c.execute("SELECT * FROM user_stats")
                print(f'User stats: {c.fetchall()}')


            # ask user to leave or stay
            answer = messagebox.askyesno('Success', 'Your data has successfully been saved. Do you want to leave?')

            if answer:
                # switch if user wants to leave
                self.return_to_start()
            else:
                # reset all entries blank if user wants to stay
                self.reset()
        else:
            messagebox.showerror('Error', 'Incomplete or invalid data has been entered')

    def reset(self):
        """Reset all register entries"""

        self.new_user_name_var.set('')
        self.new_password.set('')
        self.confirmed_password.set('')
        self.email_var.set('')

    def reset_wrong_entries(self):
        """Resets entire page if user enters incorrect data"""

        self.new_user_name_var.set('')
        self.new_password.set('')
        self.confirmed_password.set('')
        self.email_var.set('')

        self.new_user_name_error_frame.pack_forget()
        self.password_error_frame.pack_forget()
        self.email_error_frame.pack_forget()
        self.confirmed_password_error_frame.pack_forget()
        self.email_error_frame.pack_forget()
