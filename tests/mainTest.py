import unittest
import os
from main import load_settings


class MyTestCase(unittest.TestCase):

    def test_database_exists(self):
        path = os.getcwd() + '\\database\\users.db'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_load_settings_user(self):

        load_settings('user')

        user_path = os.getcwd() + '\\app\\chess_app\\all_settings\\user\\user_game_settings.csv'

        exists = os.path.exists(user_path)

        self.assertTrue(exists)

    def test_load_settings_user_stats(self):
        load_settings('user')

        user_path = os.getcwd() + '\\app\\chess_app\\all_settings\\user\\user_stats.csv'

        exists = os.path.exists(user_path)

        self.assertTrue(exists)

    def test_load_settings_guest(self):
        load_settings('guest')

        guest_path = os.getcwd() + '\\app\\chess_app\\all_settings\\guest\\default_game_settings.csv'

        exists = os.path.exists(guest_path)

        self.assertTrue(exists)

    def test_current_user_f_exists(self):
        path = os.getcwd() + '\\app\\login_system_app\\temp\\current_user.txt'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_mode_f_exists(self):
        path = os.getcwd() + '\\app\\login_system_app\\temp\\mode.txt'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_password_f_exists(self):
        path = os.getcwd() + '\\app\\login_system_app\\temp\\password.txt'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_password_recovery_email_f_exists(self):
        path = os.getcwd() + '\\app\\login_system_app\\temp\\password_recovery\\email.txt'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_password_recovery_passcode_f_exists(self):
        path = os.getcwd() + '\\app\\login_system_app\\temp\\password_recovery\\passcode.txt'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_password_recovery_password_f_exists(self):
        path = os.getcwd() + '\\app\\login_system_app\\temp\\password_recovery\\password.txt'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_password_recovery_username_f_exists(self):
        path = os.getcwd() + '\\app\\login_system_app\\temp\\password_recovery\\username.txt'

        exists = os.path.exists(path)

        self.assertTrue(exists)

    def test_saved_games_f_exists(self):
        path = os.getcwd() + '\\app\\chess_app\\all_saved_games'

        exists = os.path.exists(path)

        self.assertTrue(exists)
