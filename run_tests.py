import tkinter

import tests.loginTest as Login
import tests.mainTest as Files
import tests.databaseTest as Database
import tests.boardTest as Chess

import unittest

# test some login system functions
suite = unittest.TestLoader().loadTestsFromModule(Login)
unittest.TextTestRunner(verbosity=2).run(suite)

# test all files needed are in the program
suite = unittest.TestLoader().loadTestsFromModule(Files)
unittest.TextTestRunner(verbosity=2).run(suite)

# test database browsing commands
suite = unittest.TestLoader().loadTestsFromModule(Database)
unittest.TextTestRunner(verbosity=2).run(suite)

# test board obj
suite = unittest.TestLoader().loadTestsFromModule(Chess)
unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()