import sqlite3
import os


class DatabaseBrowser:
    def __init__(self):
        pass

    @staticmethod
    def delete_user(username):

        # Store data into database
        conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
        c = conn.cursor()

        with conn:
            # delete general
            c.execute('DELETE FROM users WHERE username=:username', {'username': username})

            # delete settings
            c.execute('DELETE FROM user_settings WHERE user=:user', {'user': username})

            # delete stats
            c.execute('DELETE FROM user_stats WHERE user=:user', {'user': username})

    @staticmethod
    def create_new_user(username, hashed_password, email):

        # Store data into database
        conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
        c = conn.cursor()

        with conn:
            # Insert values into the database (general)
            c.execute("INSERT INTO users VALUES (:username, :password, :email)",
                      {'username': username.lower(),
                       'password': hashed_password,
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
            #c.execute("SELECT * FROM users")
            #print(f'User data: {c.fetchall()}')
            #c.execute("SELECT * FROM user_settings")
            #print(f'User settings: {c.fetchall()}')
            #c.execute("SELECT * FROM user_stats")
            #print(f'User stats: {c.fetchall()}')

    @staticmethod
    def load(load='', username=None):
        """Get data from user database

        :param str load: Data to be loaded. Must be either 'statistics', 'settings' or 'general'
        :param str username: the name of the user who's data will be modified

        :return: structure containing data for that user

        """

        if username is not None:

            # Open the sql database and retrieve all the data this user has
            # All usernames in the sql file are unique so there won't be any problems
            conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
            c = conn.cursor()

            with conn:
                if load.lower() == 'statistics':
                    c.execute('''SELECT * FROM user_stats WHERE user=:username''',
                              {'username': username})

                    stats = c.fetchall()[0]

                    return list(stats)

                elif load.lower() == 'settings':
                    c.execute('''SELECT * FROM user_settings WHERE user=:username''',
                              {'username': username})

                    settings = c.fetchall()[0]

                    return list(settings)

                elif load.lower() == 'general':
                    c.execute('''SELECT * FROM users WHERE username=:username''',
                              {'username': username})

                    general = c.fetchall()[0]

                    return list(general)

    @staticmethod
    def save(save='', username=None, data=None):
        """Saves data to db

        :param str save: must be either 'statistics', 'settings' or 'general'
        :param str username: the name of the user who's data will be modified
        :param list data: The data to be stored. For 'statistics' len(6). For 'settings' len(8). For 'general' len(3)

        """

        if username is not None:

            # Open the sql database and retrieve all the data this user has
            # All usernames in the sql file are unique so there won't be any problems
            conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
            c = conn.cursor()

            if save.lower() == 'statistics':
                with conn:
                    # add new data
                    c.execute("""UPDATE user_stats SET 
                    number_of_games_played=:number_of_games_played, 
                    wins=:wins, loses=:losses, 
                    draws=:draws, 
                    ranking=:ranking 
                    WHERE user=:user""",
                              {'number_of_games_played': data[1],
                               'wins': data[2],
                               'losses': data[3],
                               'draws': data[4],
                               'ranking': data[5],
                               'user': data[0]})

            if save.lower() == 'settings':
                with conn:
                    # update all user stats
                    c.execute('''UPDATE user_settings SET 
                    difficulty=:game_difficulty, 
                    time=:time, 
                    game_type=:game_type,  
                    player_piece_color=:player_piece_color,  
                    opponent_piece_color=:opponent_piece_color,  
                    border_color=:border_color, 
                    board_color=:board_color 
                    WHERE user=:user''',
                              {'game_difficulty': data[1],
                               'time': data[2],
                               'game_type': data[3],
                               'player_piece_color': data[4],
                               'opponent_piece_color': data[5],
                               'border_color': data[6],
                               'board_color': data[7],
                               'user': data[0]})

            if save.lower() == 'general':
                with conn:
                    c.execute("UPDATE users SET username=:username,"
                              " password=:password,"
                              " email=:email",
                              {'username': data[0],
                               'password': data[1],
                               'email': data[2]})

    @staticmethod
    def username_in_database(username):
        """Ensure only unique usernames are stored in database"""

        conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
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

    @staticmethod
    def all_table_names(self):
        conn = sqlite3.connect(os.getcwd() + '\\database\\users.db')
        c = conn.cursor()
        with conn:
            c.execute('SELECT name from sqlite_master where type= "table"')

            return c.fetchall()
