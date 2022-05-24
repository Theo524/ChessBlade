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
    def load(load='', user_id=None):
        """Get data from user database

        :param str load: Data to be loaded. Must be either 'statistics', 'settings' or 'general'
        :param int user_id: the id of the user who's data will be modified

        :return: structure containing data for that user including id
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
        """For login into app, verify the user exists"""
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
                results = str(cursor.fetchall()[0][0])
                # write id to files
                with open(os.getcwd() + '\\app\\login_system_app\\temp\\current_user_id.txt', 'w') as f:
                    f.write(results)
                return True  # id for that user

            except IndexError:
                return False

    @staticmethod
    def save(save='', user_id=None, data=None):
        """Saves data to db

        :param str save: must be either 'statistics', 'settings' or 'general'
        :param int user_id: User to be deleted
        :param list data: The data to be stored, takes full record as list excluding the user id
        """

        # Open the sql database and retrieve all the data this user has
        # All usernames in the sql file are unique so there won't be any problems
        connection = db.connect(host="localhost", user="TheoAdmin", passwd="524BrownJacobTheophilus",
                                database='chess_data')

        stats_query = f"""UPDATE user_statistics SET games_played={data[0]}, wins={data[1]}, loses={data[2]}, 
        draws={data[3]}, ranking={data[4]} WHERE id={user_id}"""

        settings_query = f"""UPDATE user_settings SET difficulty="{data[0]}", game_mode="{data[1]}", player_piece_color="{data[2]}", 
        border_color="{data[3]}", board_color="{data[4]}" WHERE id={user_id}"""

        user_data_query = f"""UPDATE user_data SET username="{data[0]}", "password={data[1]}", email="{data[2]}", 
        dob="{data[3]}" WHERE id={user_id}"""

        with connection.cursor(buffered=True) as cursor:

            if save.lower() == 'statistics':
                cursor.execute(stats_query)

            if save.lower() == 'settings':
                cursor.execute(settings_query)

            if save.lower() == 'general':
                cursor.execute(user_data_query)

            connection.commit()

    @staticmethod
    def username_in_database(username):
        """Check if the username is in the database"""

        # Store data into database
        connection = db.connect(host="localhost", user="TheoAdmin", passwd="524BrownJacobTheophilus",
                                database='chess_data')
        with connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT * FROM user_data")
            results = cursor.fetchall()
            for result in results:
                # select that result
                if result[1] == username:
                    return True

        # Means all ids were checked and None equal was found
        return False




#DatabaseBrowser.create_new_user('TestUser', 'dfgddsgfsdfg', 'someone@gmail.com', '08-07-2017')
#print(DatabaseBrowser.load(14216, load='statistics'))
#print(DatabaseBrowser.load(14216, load='general'))
#print(DatabaseBrowser.load(14216, load='settings'))

#DatabaseBrowser.verify_user('TestUser', hashed_password='dfgddsgfsdfg')