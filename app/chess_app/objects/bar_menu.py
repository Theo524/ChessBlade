from tkinter import *
import os

from database.database import DatabaseBrowser
from app.chess_app.objects.settings import Settings
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import date, datetime


class BarMenu(Menu):
    def __init__(self, root):
        Menu.__init__(self, root)

        # GAME MODE
        self.root = root
        self.mode = self.root.mode
        # Create a menu
        self.game_menu = Menu(self, tearoff=0)
        # Add the game menu options
        self.game_menu.add_command(label='Open existing game', command=self.open_file)
        self.game_menu.add_command(label='Save', command=self.save_game)
        self.game_menu.add_command(label='New game', command=self.new_game)
        if self.mode == 'user':
            self.game_menu.add_command(label='Player stats', command=self.show_player_stats)
        self.game_menu.add_command(label='Exit', command=self.exit)
        # Name the game menu
        self.add_cascade(label='Game', menu=self.game_menu)

        # Create another menu
        self.help_menu = Menu(self, tearoff=0)
        # Add menu options
        self.help_menu.add_command(label='Settings', command=self.open_settings)
        self.help_menu.add_command(label='Help and chess rules')
        # Name teh menu
        self.add_cascade(label='Help', menu=self.help_menu)

        # Create another menu
        self.about_menu = Menu(self, tearoff=0)
        # Add menu options
        # self.about_menu.add_command(label='Contact us')
        self.about_menu.add_command(label='Author', command=self.show_my_details)
        # Name the menu
        self.add_cascade(label='About', menu=self.about_menu)

    def save_game(self):
        """Save a game fen string into txt file"""

        board_obj = self.root.main_chess_board
        fen = board_obj.ai_board.fen().split(' ')[0]

        with open(os.getcwd()+'\\app\\login_system_app\\temp\\current_user.txt', 'r') as f:
            name = f.read() if self.mode == 'user' else 'Guest'

        # new file name
        f_name = f'{name} - Saved Game.txt'

        today = date.today()
        date_str = today.strftime("%A %B %d, %Y")

        time = datetime.now()
        h = f'0{str(time.hour)}' if len(str(time.hour)) == 0 else time.hour
        m = f'0{str(time.minute)}' if len(str(time.minute)) == 0 else time.minute
        s = f'0{str(time.second)}' if len(str(time.second)) == 0 else time.second
        time_str = f'{h}:{m}:{s}'

        with open(os.getcwd() + f'\\app\\chess_app\\all_saved_games\\{f_name}', 'w') as f:
            f.write(f'Owner: {name}\n')
            f.write(f'Date saved: {date_str}\n')
            f.write(f'Time saved: {time_str}\n')
            f.write('\n')
            f.write(f'GAME FEN:{fen}')

        messagebox.showinfo('Saved', 'Game successfully Saved')

    def open_file(self):
        """Open file"""

        board_obj = self.root.main_chess_board

        res = messagebox.askyesno('Open', 'Open text file for saved game?')
        g_path = os.getcwd() + '\\app\\chess_app\\all_saved_games'
        if res:
            filename = filedialog.askopenfilename(initialdir=g_path, title="Select file", filetypes=(("text files","*.txt"), ("all files","*.*")))

            with open(filename, 'r') as f:
                # end of file
                file = list(f.readlines())
                fen = file[-1].split(':')[1]

            # write fen to temp file
            with open(os.getcwd() + '\\app\\chess_app\\all_saved_games\\temp\\temp_file.txt', 'w') as f:
                # end of file
                f.write(fen)

            with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
                f.write('new_game:yes\n')
                f.write('saved_game:yes')

            # close win
            self.master.destroy()

    def open_settings(self):
        """Open game settings"""
        s = Settings(self.mode)
        s.mainloop()

    def new_game(self):
        # os.path.normpath(os.getcwd() + os.sep + os.pardir)
        # Set new game file to 'yes' and destroy window, so a new ChessAPp is run
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:yes\n')
            f.write('saved_game:no')

        self.master.destroy()

    def exit(self):
        # Set new game file to 'no' and destroy window so the looping chess app stops
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
            f.write('new_game:no\n')
            f.write('saved_game:no')

        self.master.destroy()

    @staticmethod
    def show_player_stats():
        """Shows player data"""

        # We get the name for this current user
        with open(os.getcwd() + '//app//login_system_app//temp//current_user.txt', 'r') as f:
            username = f.read()

        # Get required data
        data = DatabaseBrowser.load(load='statistics', username=username)

        # load unto files
        with open(os.getcwd() + '\\app\\chess_app\\all_settings\\user\\user_stats.csv', 'w') as f:
            f.write('number_of_games_played-wins-loses-draws-ranking\n')
            f.write(f'{data[1]}-{data[2]}-{data[3]}-{data[4]}-{data[5]}')

        with open(os.getcwd() + '//app//chess_app//all_settings//user//user_stats.csv') as f:
            reader = csv.reader(f, delimiter='-')  # file separated by '-' rather than comas
            next(reader)  # skip header
            for row in reader:
                # the row is a list containing the data
                number_of_games_played = row[0]
                wins = row[1]
                loses = row[2]
                draws = row[3]
                ranking = row[4]

        new_window = Toplevel()

        # Create the frame
        player_stats_frame = Frame(new_window,  width=320, height=180)
        player_stats_frame.pack(pady=5)

        # Place the username as a title at the top of the box frame
        Label(player_stats_frame, text=username, font='verdana 15 bold') \
            .grid(row=0, columnspan=5, padx=20, pady=5)
        ttk.Separator(player_stats_frame, orient='horizontal').grid(row=1, column=0, columnspan=5, sticky='we')

        # - DATA
        # number of games played
        Label(player_stats_frame, text='Number_of_games_played: ', font='calibri 10') \
            .grid(column=0, row=2)
        Label(player_stats_frame, text=number_of_games_played, font='verdana 10 bold') \
            .grid(column=1, row=2, padx=(0, 28))

        # wins
        Label(player_stats_frame, text='Wins: ', font='calibri 10') \
            .grid(column=2, row=2, padx=(15, 0))
        Label(player_stats_frame, text=wins, font='verdana 10 bold') \
            .grid(column=3, row=2, padx=(0, 25))

        # loses
        Label(player_stats_frame, text='Loses: ', font='calibri 10') \
            .grid(column=0, row=3)
        Label(player_stats_frame, text=loses, font='verdana 10 bold') \
            .grid(column=1, row=3, padx=(0, 28))

        # draws
        Label(player_stats_frame, text='Draws: ', font='calibri 10') \
            .grid(column=2, row=3, padx=(15, 0))
        Label(player_stats_frame, text=draws, font='verdana 10 bold') \
            .grid(column=3, row=3, padx=(0, 25))

    @staticmethod
    def show_my_details():
        """My credentials"""

        win = Toplevel()
        github_frame = Frame(win)
        github_frame.pack()

        first_row = Frame(github_frame)
        github_user_intro = Label(first_row, text='Github user:', font='Helvetica 11 bold')
        github_user_text = Label(first_row, text='Theo524', font='Helvetica 11')
        first_row.pack()
        github_user_intro.pack(side=LEFT)
        github_user_text.pack()

        second_row = Frame(github_frame)
        github_user_intro_2 = Label(second_row, text='Github site for this project:', font='Helvetica 11 bold')
        github_user_text_2 = Label(second_row, text='https://github.com/Theo524/Chess-game.git', font='Helvetica 11')
        second_row.pack()
        github_user_intro_2.pack(side=LEFT)
        github_user_text_2.pack()

    def show_help(self):
        """Help window"""

        pass
