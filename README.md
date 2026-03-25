# GameHub

We plan to build a secure, multi-user game hub which uses Bash scripting for authentication and Python and Pygame for gameplay. In this project, two players will enter their usernames and passwords to authenticate themselves, then select a game from a menu, play via a graphical interface and have their results recorded on a persistent leaderboard.

As mentioned in the project specification, we will make a file main.sh to handle user authentication, which allows the users to securely login via username and password(which will be hashed with SHA-256), after which game.py will be called.

The game engine game.py will have an interactive, robust user interface with a menu to choose various games from(like Tic-Tac-Toe, Othello, Connect 4 and more) and play. There will be a feature for users to request hints as well during gameplay.

We will display a leaderboard after every game and there will be an option to choose which metric it is sorted by. We will also implement displaying of various statistics through graphs and charts using matplotlib.
