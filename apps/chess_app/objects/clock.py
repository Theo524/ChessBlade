import time
from tkinter import *
from tkinter import messagebox
import os

"""Credits timer function https://pythonguides.com/create-countdown-timer-using-python-tkinter/"""


class Clock(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # The window itself
        self.root = master

        # Retrieve the default game settings, to get the time value
        with open(os.getcwd() + "//apps//chess_app//all_settings//guest//default_game_settings.csv", 'r') as f:
            # Reads both lines in the file (header and row) and grabs the list at index 1, (row)
            data = f.readlines()[1].split('-')
            # This value is in the format hh:mm:ss, so it split into a list containing all the times slices
            settings_time = str(data[1]).split(':')
            # List comprehension looping through 3 vales - hour, minute and second
            temp = [item for item in settings_time]
            new = []

            # format time from e.g. '2:4:30' to '02:04:30' with this loop
            for i in temp:
                if len(i) == 1:
                    b = i.replace(f'{i}', f'0{i}')
                    new.append(b)
                else:
                    new.append(i)

        # Time variables (str to int)
        self.hours = int(new[0])
        self.minutes = int(new[1])
        self.seconds = int(new[2])

        # Tk time variables
        self.hour = StringVar()
        self.minute = StringVar()
        self.second = StringVar()

        # Set the time to the one retrieved from file and formatted
        self.hour.set(self.hours)
        self.minute.set(self.minutes)
        self.second.set(self.seconds)

        # Font used
        f = ("Verddana", 35, 'bold')

        # Hour label
        hour_tf = Label(self, width=3, font=f, textvariable=self.hour)
        hour_tf.pack(side=LEFT)

        # colon
        Label(self, text=':', font=f).pack(side=LEFT)

        # Minutes label
        mins_tf = Label(self, width=3, font=f, textvariable=self.minute)
        mins_tf.pack(side=LEFT)

        # colon
        Label(self, text=':',font=f).pack(side=LEFT)

        # Seconds label
        sec_tf = Label(self, width=3, font=f, textvariable=self.second)
        sec_tf.pack(side=LEFT)

    def startCountdown(self):
        """Starts countdown"""
        try:
            # Convert everything to seconds
            # Multiply hours by 3600, minutes by 60 and seconds are kept the same
            userinput = (self.hours * 3600) + (self.minutes * 60) + self.seconds
        except:
            messagebox.showwarning('', 'Invalid Input!')
        while userinput > -1:
            mins, secs = divmod(userinput, 60)

            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)

            self.hour.set("{0:2d}".format(hours))
            self.minute.set("{0:2d}".format(mins))
            self.second.set("{0:2d}".format(secs))

            self.master.update()
            time.sleep(1)

            if (userinput == 0):
                 messagebox.showinfo("", "Time's Up")

            userinput -= 1
