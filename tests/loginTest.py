import unittest
from app.login_system_app.login import LoginSystem, ForgotPassword
from app.login_system_app.register import RegisterSystem
from app.login_system_app.start import StartApp


class MyTestCase(unittest.TestCase):
    def est_login_check(self):
        """Takes too long"""

        obj_1 = StartApp()
        obj_2 = LoginSystem(obj_1)

        h_password = '7d1e03376e60d97da300f95cfb47bf55936c3c7c05fb51bbe5d36b88ad2f7' \
                     '98ceb860cf0d27eb8e8145e41c482e56377174f01a9b1de04a93a5b0d8588a29b8d'

        exists = obj_2.check_data('theoden', h_password)
        exists_2 = obj_2.check_data('opkjihu', 'joihuj')

        self.assertTrue(exists, 'User should exist')  # existing user
        self.assertFalse(exists_2, 'User should not exist')  # user doesn't exist

    def test_validate_email(self):
        result = ForgotPassword.validate('minilobezno@gmail.com')
        result_2 = ForgotPassword.validate('hghvhbjbmgnv')

        self.assertTrue(result)
        self.assertFalse(result_2)

    def test_validate_email_2(self):
        result = RegisterSystem.validate_email('minilobezno@gmail.com')
        result_2 = RegisterSystem.validate_email('hghvhbjbmgnv')

        self.assertTrue(result)
        self.assertFalse(result_2)

    def est_check_email(self):
        """Takes too long"""
        exists = RegisterSystem.check_email('minilobezno@gmail.com')
        exists_2 = RegisterSystem.validate_email('hghvhbjbmgnv')

        self.assertTrue(exists)
        self.assertFalse(exists_2)

    def test_calculate_age(self):
        age = RegisterSystem.calculate_age('05/02/2004', this_year=2021)

        self.assertEqual(age, 16)

    def test_hash_pass(self):
        password = RegisterSystem.hash_pass('lolol')

        self.assertEqual(len(password), 128, msg='Length of h pass should 128')

    def test_check_pass(self):
        valid = RegisterSystem.check_pass('TTtt@@00')
        invalid = RegisterSystem.check_pass('nvs')

        self.assertTrue(valid)
        self.assertFalse(invalid)
