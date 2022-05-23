import sqlite3
import os
import mysql.connector as db
import random


class DatabaseBrowser:
    @staticmethod
    def delete_user(user_id):
        """Deletes user from database

        :param int user_id: User to be deleted
        """

        # Store data into database
        connection = db.connect(host="localhost", user="TheoAdmin", passwd="524BrownJacobTheophilus",
                                database='chess_data')

        # deletes
        user_dlt = f"""
DELETE FROM user_data WHERE id = "{user_id}"
"""
        settings_dlt = f"""
DELETE FROM user_settings WHERE id = "{user_id}"
"""

        statistics_dlt = f"""
DELETE FROM user_statistics WHERE id = "{user_id}"
"""

        with connection.cursor(buffered=True) as cursor:
            cursor.execute(user_dlt)
            cursor.execute(settings_dlt)
            cursor.execute(statistics_dlt)
            connection.commit()

    @staticmethod
    def id_exists(user_id):
        """Ensure an id doesnt exists alreday in the database

        :param int user_id: 5 digit id for the user
        """

        # Store data into database
        connection = db.connect(host="localhost", user="TheoAdmin", passwd="524BrownJacobTheophilus",
                                database='chess_data')
        with connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT * FROM user_data")
            results = cursor.fetchall()
            for result in results:
                # select that result
                if result[0] == user_id:
                    return True

        # Means all ids were checked and None equal was found
        return False

    @staticmethod
    def generate_id():
        """Create a unique id"""
        # generate 5 digit id and ensure it doesn't already exists
        user_id = int(''.join([random.choice([str(i) for i in range(0, 10)]) for i in range(5)]))
        while True:
            if DatabaseBrowser.id_exists(user_id):
                user_id = int(''.join([random.choice([str(i) for i in range(0, 10)]) for i in range(5)]))
                continue

            else:
                return user_id

    @staticmethod
    def create_new_user(username, hashed_password, email, dob):
        """Creates new user

        :param str username: username
        :param str hashed_password: Hashed version of password to be used (blake2b)
        :param str email: email account that will be used
        """

        # Store data into database
        connection = db.connect(host="localhost", user="TheoAdmin", passwd="524BrownJacobTheophilus",
                                database='chess_data')

        # get unique id
        user_id = DatabaseBrowser.generate_id()

        with connection.cursor(buffered=True) as cursor:

            # queries
            user = f"""
            INSERT INTO user_data (id, username, password, email, dob) VALUES ({user_id}, "{username}", "{hashed_password}", "{email}", "{dob}")
            """

            settings = f"""
            INSERT INTO user_settings (id, difficulty, game_mode, player_piece_color, border_color, board_color) VALUES 
            ({user_id}, "Novice", "two_player", "black", "black", "brown")
            """

            statistics = f"""
            INSERT INTO user_statistics (id, games_played, wins, loses, draws, ranking) VALUES 
            ({user_id}, 0, 0, 0, 0, 0)
            """

            # Insert values into the database (general)
            cursor.execute(user)

            # Insert values into the database (settings)
            cursor.execute(settings)

            # Insert values into the database (statistics)
            cursor.execute(statistics)

            connection.commit()

    @staticmethod
    def load(user_id, load=''):
        """Get data from user database

        :param str load: Data to be loaded. Must be either 'statistics', 'settings' or 'general'
        :param str user_id: the id of the user who's data will be modified

        :return: structure containing data for that user
        """

        connection = db.connect(host="localhost", user="TheoAdmin", passwd="524BrownJacobTheophilus",
                                database='chess_data')

        # Open the sql database and retrieve all the data this user has
        # All usernames in the sql file are unique so there won't be any problems
        with connection.cursor(buffered=True) as cursor:

            if load.lower() == 'statistics':
                cursor.execute(f"SELECT * FROM user_statistics WHERE id = {user_id}")

                results = list(cursor.fetchall()[0])

                return results

            elif load.lower() == 'settings':
                cursor.execute(f"SELECT * FROM user_settings WHERE id = {user_id}")

                results = list(cursor.fetchall()[0])

                return results

            elif load.lower() == 'general':
                cursor.execute(f"SELECT * FROM user_data WHERE id = {user_id}")

                results = list(cursor.fetchall()[0])

                return results

    @staticmethod
    def verify_user(username, hashed_password):
        # Store data into database
        connection = db.connect(host="localhost", user="TheoAdmin", passwd="524BrownJacobTheophilus",
                                database='chess_data')

        query = f"""
        SELECT id FROM user_data WHERE username="{username}" AND password="{hashed_password}"
"""
        # find the id for that user
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            try:
                results = cursor.fetchall()[0][0]
                # write id to files
                with open(os.getcwd() + '\\app\\login_system_app\\temp\\current_user_id.txt', 'w') as f:
                    f.write(results)
                return True  # id for that user

            except IndexError:
                return False

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
                    c.execute("UPDATE users SET "
                              " password=:password,"
                              " email=:email "
                              "WHERE username=:username",
                              {'username': data[0],
                               'password': data[1],
                               'email': data[2]})


#DatabaseBrowser.create_new_user('TestUser', 'dfgddsgfsdfg', 'someone@gmail.com', '08-07-2017')
#print(DatabaseBrowser.load(14216, load='statistics'))
#print(DatabaseBrowser.load(14216, load='general'))
#print(DatabaseBrowser.load(14216, load='settings'))

DatabaseBrowser.verify_user('TestUser', hashed_password='dfgddsgfsdfg')