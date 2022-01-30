import unittest
from database.database import DatabaseBrowser
from app.login_system_app.register import RegisterSystem


class MyTestCase(unittest.TestCase):

    def test_00_user_in_db(self):
        exists = DatabaseBrowser.username_in_database('user_test_account')

        if not exists:
            DatabaseBrowser.create_new_user('user_test_account',
                                            RegisterSystem.hash_pass('TTtt@@@00'),
                                            'minilobezno@gmail.com')

            exists = DatabaseBrowser.username_in_database('user_test_account')

        self.assertTrue(exists)

    def test_01_create_new_user(self):
        DatabaseBrowser.create_new_user('test_create_new_user', 'test_unhashed_password', 'test@gmail.com')

        exists = DatabaseBrowser.username_in_database('test_create_new_user')

        DatabaseBrowser.delete_user('test_create_new_user')

        self.assertTrue(exists)

    def test_02_delete_user(self):
        DatabaseBrowser.create_new_user('test_delete_user', 'test_unhashed_password', 'test@gmail.com')

        DatabaseBrowser.delete_user('test_delete_user')

        exists = DatabaseBrowser.username_in_database('test_delete_user')

        self.assertFalse(exists)

    def test_03_load_settings(self):
        data = DatabaseBrowser.load(load='settings', username='user_test_account')

        self.assertEqual(len(data), 8)

    def test_04_load_statistics(self):
        data = DatabaseBrowser.load(load='statistics', username='user_test_account')

        self.assertEqual(len(data), 6)

    def test_05_load_general(self):
        data = DatabaseBrowser.load(load='general', username='user_test_account')

        self.assertEqual(len(data), 3)

    def test_06_save_settings(self):
        # would be actual user data
        data = ['user_test_account', 'test', 'test', 'test', 'test', 'test', 'test', 'test']
        DatabaseBrowser.save(save='settings', username='user_test_account', data=data)

        loaded_data = DatabaseBrowser.load(load='settings', username='user_test_account')

        is_equal = data == loaded_data

        self.assertTrue(is_equal)

    def test_07_save_statistics(self):
        # would be actual user data
        data = ['user_test_account', 'test', 'test', 'test', 'test', 'test']
        DatabaseBrowser.save(save='statistics', username='user_test_account', data=data)

        loaded_data = DatabaseBrowser.load(load='statistics', username='user_test_account')

        is_equal = data == loaded_data

        self.assertTrue(is_equal)

    def test_08_save_general(self):
        data = ['user_test_account', 'test', 'test']
        DatabaseBrowser.save(save='general', username='user_test_account', data=data)

        loaded_data = DatabaseBrowser.load(load='general', username='user_test_account')

        is_equal = data == loaded_data

        self.assertTrue(is_equal, f'{data},\n {loaded_data}')
