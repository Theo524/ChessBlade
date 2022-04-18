from app.login_system_app.start import StartApp
from app.chess_app.chess_app import ChessApp
from database.database import DatabaseBrowser

import os
import json

# Directory path for the current script
main_path = os.getcwd()

# File paths to be used
database = main_path + '\\database\\users.db'
temp_files = main_path + '\\app\\login_system_app\\temp'
game_settings_path = main_path + '\\app\\chess_app\\all_settings'


def load_settings(game_mode):
    """Load settings from db to files, depending on game mode"""

    if game_mode == 'guest':
        # Apply default settings, to default_settings.csv
        with open(game_settings_path + '\\guest\\default_game_settings.csv', 'w') as file:
            # Apply default game settings
            file.write('Game_difficulty-time-game_mode-player_piece_color-opponent_piece_color-border_color-'
                       'board_color\n')
            file.write("medium-02:30:00-two_player-black-white-black-brown")

    if game_mode == 'user':
        # Apply settings specific to that user

        # Retrieve the user name
        with open(temp_files + '//current_user.txt', 'r') as f:
            user_name = f.read()

        # get settings and statistics for this user
        settings = DatabaseBrowser.load(load='settings', username=user_name)
        stats = DatabaseBrowser.load(load='statistics', username=user_name)

        # write all retrieved data to user files
        with open(game_settings_path + '\\user\\user_game_settings.csv', 'w') as my_file:
            # write the settings to user_settings.csv
            my_file.write('Game_difficulty-time-game_mode-player_piece_color-opponent_piece_color-border_color-'
                          'board_color\n')
            my_file.write(f"{settings[1]}-{settings[2]}-{settings[3]}-{settings[4]}-{settings[5]}-"
                          f"{settings[6]}-{settings[7]}")

        # write stats to user_stats.csv file
        user_stats = game_settings_path + '\\user\\user_stats.csv'
        with open(user_stats, 'w') as f:
            # These are user statistics such as loses, wins, draws and ranking
            f.write('number_of_games_played-wins-loses-draws-ranking\n')
            f.write(f"{stats[1]}-{stats[2]}-{stats[3]}-{stats[4]}-{stats[5]}")


def main():

    # Start the initial menu application
    start = StartApp()

    # If the user just closes the window do not proceed
    if not start.user_entered_game:
        return

    # game mode (from Login system)
    mode = start.mode

    # load settings into files
    load_settings(mode)

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
    # game
    main()
