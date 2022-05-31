from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from app.login_system_app.placeholder_entry import PlaceholderEntry
from app.resources.database.database import SQLite3DatabaseBrowser

import hashlib
import smtplib


class RegisterSystem(ttk.Frame):
    def __init__(self, master, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        self.master = master

        self.master.style.configure('error_label.TLabel', foreground='red', font=('Arial', 7))

        # container
        self.scene = ttk.Frame(self)
        self.scene.pack(pady=50)

        # ----------------------App layout/upper frame----------------------
        self.upper_window = ttk.Frame(self.scene, height=50, width=350)
        self.upper_window.pack(pady=15)
        self.inner_upper = ttk.Frame(self.upper_window)
        self.inner_upper.pack(side=LEFT)
        self.air = ttk.Frame(self.inner_upper, width=270)
        # Button to return to start page
        ttk.Button(self.inner_upper,
                   cursor='hand2', command=self.master.go_to_start_page, image=self.master.back_btn_photo).pack(side=LEFT, ipady=5, ipadx=5)

        self.air.pack(side=LEFT)

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
        self.new_user_name_error = ttk.Label(self.new_user_name_error_frame,
                                             textvariable=self.new_user_name_error_var,
                                             style='error_label.TLabel')

        # New password (MIDDLE FRAME)
        self.new_password_frame = ttk.Frame(self.main_window)
        self.new_password_frame.pack(pady=10)

        self.new_password = StringVar()
        self.new_password_entry = PlaceholderEntry(self.new_password_frame, 'New Password',
                                                   textvariable=self.new_password)
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
        self.email_address_entry = PlaceholderEntry(self.email_frame, 'Email address (@gmail.com)',
                                                    textvariable=self.email_var)
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

        self.save_button = ttk.Button(self.save_data_frame, text='Save', command=self.store_data,
                                      cursor='hand2')
        self.save_button.pack()

        # ----------------------App layout/lower frame----------------------
        self.lower_frame = ttk.Frame(self.scene, height=50)
        self.lower_frame.pack()

    @staticmethod
    def validate_email(email):
        """Validate email"""

        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@gmail.com')

        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def check_email(self, email):
        """Checks whether the email account user entered exists"""

        # first validate
        valid = RegisterSystem.validate_email(email)

        if valid:
            try:
                # Receiver email address
                receiver_address = email

                # Our message
                subject = "Welcome"
                body = f"Greetings from ChessBlade\n\nYour account has been successfully registered!" \
                       f"\nTime to play!" \
                       f"\n\nChessBLade,"

                # Combine the subject and the body onto a single message
                message = f"Subject: {subject}\n\n{body}"

                # Endpoint for the SMTP Gmail server
                smtp_server = smtplib.SMTP('smtp-mail.outlook.com', 587)
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.ehlo()

                # Login with a dummy email account I created
                smtp_server.login(self.master.v3948hf['E_USER'], self.master.v3948hf['E_PASS'])

                # Message sent in the above format (Subject:...\n\nBody) from my dummy email account
                smtp_server.sendmail(self.master.v3948hf['E_USER'], receiver_address, message)

                # Close our endpoint
                smtp_server.close()

                # if nothing went wrong it means the email account exists
                return True

            except smtplib.SMTPRecipientsRefused:
                # if an exception occurs, the account doesn't exist
                # The name of the exception is unclear and I do not know how to write it, hence I just use 'except'
                return False
        else:
            return False

    @staticmethod
    def calculate_age(dob, this_year):
        """Calculate the user age"""

        # get today's date
        today = date.today()

        # convert the age string into a list
        born = dob.split('/')
        date_of_birth = date(int(born[2]), int(born[1]), int(born[0]))

        # operation that calculates the difference between today and the birthdate (age)
        return this_year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

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
        # Should have at least one number.
        # Should have at least one uppercase and one lowercase character.
        # Should have at least one special symbol.
        # Should be between 8 to 20 characters long.
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        # compiling regex
        pat = re.compile(reg)
        # searching regex
        match = re.search(pat, password)
        # validating conditions
        if match:
            return True
        else:
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
            if SQLite3DatabaseBrowser.username_in_database(username):
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
            self.password_error_var.set('Password requisites: 8-20 characters,'
                                        ' at least - 1 symbols, 1 number, 1 upper, 1 lower')
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
        this_year = date.today().year
        age = self.calculate_age(date_of_birth, this_year)
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
            hashed_password = self.hash_pass(password)

            # create new user
            SQLite3DatabaseBrowser.create_new_user(username=username, hashed_password=hashed_password, email=email,
                                                   dob=date_of_birth)

            # ask user to leave or stay
            answer = messagebox.askyesno('Success', 'Your data has successfully been saved. Do you want to leave?')

            if answer:
                # switch if user wants to leave
                self.master.go_to_start_page()
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

        self.new_username_entry.reset()
        self.new_password_entry.reset()
        self.confirmed_password_entry.reset()
        self.email_address_entry.reset()
