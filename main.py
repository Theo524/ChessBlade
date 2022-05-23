from app.login_system_app.start import StartApp
from app.chess_app.chess_app import ChessApp
from database.database import DatabaseBrowser

import os
import json
from tkinter import *
import time
import traceback
def resource_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    os.chdir(base_path)  # change


def intro_splash():
    """Close startup splash"""
    try:
        import pyi_splash
        pyi_splash.close()
    except:
        return


# change script path for pyinstaller env

intro_splash()
resource_path()

# Directory path for the current script
main_path = os.getcwd()

# File paths to be used
database = main_path + '\\database\\users.db'
temp_files = main_path + '\\app\\login_system_app\\temp'
game_settings_path = main_path + '\\app\\chess_app\\all_settings'


def load_settings(game_mode, user_id):
    """Load settings from db to files, depending on game mode"""

    if game_mode == 'guest':
        # Apply default settings, to default_settings.csv
        with open(game_settings_path + '\\guest\\default_game_settings.csv', 'w') as file:
            # Apply default game settings
            file.write('Game_difficulty-game_mode-player_piece_color-border_color-'
                       'board_color\n')
            file.write("medium-two_player-black-black-brown")

    if game_mode == 'user':
        # Apply settings specific to that user

        # Retrieve the user name
        with open(temp_files + '//current_user.txt', 'r') as f:
            user_name = f.read()

        # get settings and statistics for this user
        settings = DatabaseBrowser.load(load='settings', user_id=user_id)
        stats = DatabaseBrowser.load(load='statistics', user_id=user_id)

        # write all retrieved data to user files
        with open(game_settings_path + '\\user\\user_game_settings.csv', 'w') as my_file:
            # write the settings to user_settings.csv
            my_file.write('Game_difficulty-game_mode-player_piece_color-border_color-'
                          'board_color\n')
            my_file.write(f"{settings[1]}-{settings[2]}-{settings[3]}-{settings[4]}-{settings[5]}")

        # write stats to user_stats.csv file
        user_stats = game_settings_path + '\\user\\user_stats.csv'
        with open(user_stats, 'w') as f:
            # These are user statistics such as loses, wins, draws and ranking
            f.write('number_of_games_played-wins-loses-draws-ranking\n')
            f.write(f"{stats[1]}-{stats[2]}-{stats[3]}-{stats[4]}-{stats[5]}")


def starting_menu():
    """Starting window for user to access game"""

    # Start the initial menu application
    start = StartApp()

    # If the user just closes the window do not proceed
    if not start.user_entered_game:
        return

    # game mode (from Login system)
    mode = start.mode
    user_id = start.user_id

    # load settings
    load_settings(mode, user_id)

    return mode


def chess_main(mode, splash):
    """Chess application initialization"""

    # remove splash screen
    splash.destroy()

    # Defines whether to run game or not
    response = 'yes\n'
    saved_game = 'no'

    # while the response remains as 'yes'
    while str(response) == 'yes\n':

        # Start new chess game
        if saved_game == 'yes':
            # get fen string for saved game to be opened
            with open(main_path + '\\app\\chess_app\\all_saved_games\\temp\\temp_file.json') as f:
                data = json.load(f)
                saved_data = (data['fen'], data['notation'], data['deleted_pieces'])

            # start actual game app
            ChessApp(mode, saved_data=saved_data).mainloop()
        if saved_game == 'no':
            # start actual game app
            ChessApp(mode).mainloop()

        # Get new data once the chess app has been closed response on whether to start a new chess game or not
        with open(main_path + '\\app\\chess_app\\all_settings\\data.txt', 'r') as f:
            txt = list(f.readlines())
            response = txt[0].split(':')[1]
            saved_game = txt[1].split(':')[1]


if __name__ == '__main__':
    # main code
    try:
        # starting menu
        game_mode = starting_menu()

        if game_mode:
            # splash screen
            splash_root = Tk()
            splash_root.geometry("578x459")  # Adjust size
            splash_root.resizable(False, False)
            photo_image = PhotoImage(file=os.getcwd() + "\\app\\resources\\img\\splash.png")
            splash_label = Label(splash_root, text="Splash Screen", image=photo_image)  # Set Label
            splash_label.pack()
            splash_root.eval('tk::PlaceWindow . center')  # center splash window
            splash_root.overrideredirect(1)
            # chess application after splash screen
            splash_root.after(3000, func=lambda: chess_main(game_mode, splash_root))

            # run splash screen
            mainloop()
    except Exception as e:
        # write error to file
        time = str(time.time())
        with open(os.getcwd() + "\\tests\\crash-logs\\CRASH-" + time + ".txt", "w") as crashLog:
            traceback.print_exc(file=crashLog)

