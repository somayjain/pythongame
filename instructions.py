import curses
import game
a=game.robomake()
def inst():
	win=a.addscreen()
	a.definecolors()
	win.addstr(2,58 , "Robot Bomb Defuser", curses.color_pair(3))
	win.addstr(6,28 , "This game has one red colored bomb which is to be diffused by a blue colored robot.", curses.color_pair(2))
	win.addstr(7,31 , "The robot has to collect 'd' diffuse codes before diffusing the bomb.", curses.color_pair(2))
	win.addstr(8,30 , "The number of diffuse codes collected are displayed on the top left corner.", curses.color_pair(2))
	win.addstr(10,36 , "The player loses in the following situations:", curses.color_pair(2))
	win.addstr(11,36 , "1) Reaches the bomb before collecting all diffuse codes", curses.color_pair(2))
	win.addstr(12,36 , "2) Hits the wall", curses.color_pair(2))
	win.addstr(13,36 , "3) Hits the mine", curses.color_pair(2))
	win.addstr(14,36 , "4) Hits the enemy robot or the bullet thrown by enemy robot", curses.color_pair(2))
	win.addstr(16,27 , "As the robot gathers the diffuse codes, it's speed increases, increasing the difficulty level", curses.color_pair(2))
	win.addstr(18,54 , "The game has five levels.", curses.color_pair(2))
	win.addstr(19,48 , "Mines and enemy robot appear onwards level 1", curses.color_pair(2))
	win.addstr(20,43 , "As the levels progress, the number of mines increase.", curses.color_pair(2))
	win.addstr(22,45 , "The score given in each round is as follows:", curses.color_pair(2))
	win.addstr(23,60 , "Level 1: 5", curses.color_pair(2))
	win.addstr(24,60 , "Level 2: 10", curses.color_pair(2))
	win.addstr(25,60 , "Level 3: 15", curses.color_pair(2))
	win.addstr(26,60 , "Level 4: 20", curses.color_pair(2))
	win.addstr(27,60 , "Level 5: 25", curses.color_pair(2))
	win.addstr(29,52 , "Controls-", curses.color_pair(2))
	win.addstr(30,60 , "arrow keys to move", curses.color_pair(2))
	win.addstr(31,60 , "p or P to pause", curses.color_pair(2))
	win.addstr(32,60 , "ESC to exit the game", curses.color_pair(2))
	win.addstr(34,49 , "Press any key to PLAY or ESC to exit", curses.color_pair(4))
	nxt=win.getch()
	curses.endwin()
	if(nxt==27):
		return -1