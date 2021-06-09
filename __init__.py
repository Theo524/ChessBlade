"""By Theophilus Brown"""

# A chess game that consists of a login system and a chess game itself (not online)

"""
# DATABASE

// sql file called: 'users.db'
// sql tables names used:
// - users (name, password, email)
// - user_settings
// - user_stats
To directly view database download db browser at: https://sqlitebrowser.org/dl/ and open with db file


# CLASSES

- StartApp
// Contains the Window object for the starting application
// Allows the user to change frames

- StartPage
// Login, user can login
// Register, user can register
// Enter as guest, user can enter game with no account

- LoginApp
// Contains Window object for starting Login process
// Allows to change frames

- LoginPage
// Username, username can be entered
// Password, password can be entered, hidden with asterisks
// ForgotPassword, password recovery process
// ShowPassword, hides or shows password with '*'
// Login, Verify data and start game

- ForgotPassword
// Entry for username and email account
// Continue, check if valid
// if valid send email with passcode

- VerifyPasscode
// Entry requesting passcode
// Continue, check if passcode is valid

- NewPassword
// Allow creation of new password

- RegisterApp
// Contains Window object for starting Registration process
// Allows to change frames

- RegisterPage
// 5 entries requesting data
// save data to database if valid

- ChessApp
// Contains Window object for chess game

- BarMenu
// Menu at top of ChessApp
// Options: New game, Help, About

- Board
// Generates both virtual and visual chess board
// Game of chess

- Settings
// Customization: board color, piece color
// General: difficulty, time, game mode
"""