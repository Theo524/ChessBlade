from app.login_system_app.start import StartApp
from app.chess_app.chess_app import ChessApp

import os
import sqlite3

# Working directory for the current script
main_path = os.getcwd()

# set files to be used
# login system paths
database = main_path + '\\database\\users.db'
temp_files = main_path + '\\app\\login_system_app\\temp'
# chess paths
game_settings_path = main_path + '\\app\\chess_app\\all_settings'


def load_settings(game_mode):
    """Load settings from db to files, depending on gamemode"""

    if game_mode == 'guest':
        # if the mode is 'guest'
        # Apply default settings, to default_settings.csv

        # load default game settings
        default_game_settings = game_settings_path + '\\guest\\default_game_settings.csv'
        with open(default_game_settings, 'w') as file:
            # Apply default game settings
            file.write('Game_difficulty-time-game_mode-player_piece_color-opponent_piece_color-border_color-'
                       'board_color\n')
            file.write("medium-02:30:00-two_player-black-white-black-brown")

    if game_mode == 'user':
        # if the game mode is 'user'

        # Retrieve this user name
        with open(temp_files + '//current_user.txt', 'r') as f:
            user_name = f.read()

        # Open the sql database and retrieve all the data this user has, where the username is the id
        # All usernames in the sql file are unique so there won't be any problems such as duplicates
        conn = sqlite3.connect(database)
        c = conn.cursor()

        with conn:
            # get user statistics from db
            c.execute("SELECT * FROM user_stats WHERE user=:user",
                      {'user': user_name})
            # save the stats in a variable
            stats = c.fetchall()

            # get that user settings
            c.execute("SELECT * FROM user_settings WHERE user=:user",
                      {'user': user_name})
            # save the settings in a variable
            settings = c.fetchall()

        # write all the data to user files
        user_game_settings = game_settings_path + '\\user\\user_game_settings.csv'
        with open(user_game_settings, 'w') as my_file:
            # write the settings to user_settings.csv
            my_file.write('Game_difficulty-time-game_mode-player_piece_color-opponent_piece_color-border_color-'
                          'board_color\n')
            my_file.write(f"{settings[0][1]}-{settings[0][2]}-{settings[0][3]}-{settings[0][4]}-{settings[0][5]}-"
                          f"{settings[0][6]}-{settings[0][7]}")

        # write stats to user_stats.csv file
        user_stats = game_settings_path + '\\user\\user_stats.csv'
        with open(user_stats, 'w') as f:
            # These are user statistics such as loses, wins, draws and ranking
            f.write('number_of_games_played-wins-loses-draws-ranking\n')
            f.write(f"{stats[0][1]}-{stats[0][2]}-{stats[0][3]}-{stats[0][4]}-{stats[0][5]}")


if __name__ == '__main__':
    # Start the application
    start = StartApp()

    start.mainloop()
    # Once logged in or entered in guest mode, destroy the startapp
    start.destroy()

    # Retrieve the game mode the game should be in (guest or user, set by the startapp)
    with open(main_path + '\\app\\login_system_app\\temp\\mode.txt') as f:
        mode = f.read()

    # load settings into files
    load_settings(mode)

    # Set start_new_game to true
    with open(main_path + '\\app\\chess_app\\all_settings\\data.txt', 'w') as f:
        f.write('new_game:yes')

    # read the data from that file
    with open(main_path + '\\app\\chess_app\\all_settings\\data.txt', 'r') as f:
        response = f.read().split(':')[1]

    # while the response remains as 'yes'
    while str(response) == 'yes':
        # Start new chess game
        ChessApp(mode).mainloop()

        # Get new response once the chess app has been closed
        # Response on whether to start a new app
        with open(main_path + '\\app\\chess_app\\all_settings\\data.txt', 'r') as f:
            response = f.read().split(':')[1]
