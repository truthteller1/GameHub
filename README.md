# GameHub

Our project is a secure, multi-user game hub which uses Bash scripting for authentication and Python and Pygame for gameplay. In this project, two players enter their usernames and passwords to authenticate themselves, then select a game from a menu, play via a graphical interface and have their results recorded on a persistent leaderboard. The project includes the games Tic-Tac-Toe, Othello, Connect4, Chain Reaction and Checkers.

For details about installing prerequisites and setup refer to report.pdf.

**This project should only be run on Linux for complete functionality. If not, there may be issues with the sound, the avatar system and/or the matplotlib functionality. Do not resize the window, this will cause issues with the background and will also skew the positioning of the elements.**

The project can be run by bash main.sh in the directory hub upon which both players will be prompted to sign in using their usernames and passwords, and to create a new username if this is their first time. After this, the python script game.py will be called, opening a landing screen which is displayed in the screenshot below. As seen in Fig. 1, there
are three buttons on this screen: Options, Quit and Play. There is also a back button in the top right corner. Pressing Quit or the back button quits the program and halts the running of the python file. Pressing Options or Play opens other sub-menus detailed below.

Upon pressing Options, you are presented with the options menu which has 3 choices- Sound, Avatar and Analytics, and there is also a Back button. Pressing any of these(other than back of course) will open the respective submenu of each option.

Sound has options to change the track currently playing and to change the volume of the song. Avatar has options to change various features of each player’s respective avatar. 

Analytics has options to choose which metric the leaderboard will be sorted by when it is displayed, and a button named Show. If you click show, the command bash leaderboard.sh will be called and the leaderboard for each game will be printed out in the terminal. After this, the matplotlib plot of various game-related statistics will be displayed.

Also, upon pressing Play, you are presented with the play menu which has choices of all the 5 games in the project. Upon pressing any of the game buttons, the corresponding game will open and it can be played between the two players. When the game is completed, a win screen will be displayed with the winner’s name and avatar for a few seconds, after which the user will be redirected to the Analytics menu.
