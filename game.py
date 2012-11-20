import curses, random
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
class A():
	pass

def robomake():
	box=A()
	box.d=5    				# No of diffuse codes
	box.begin_x = 10 ; box.begin_y = 0	# Starting coordinates of the window
	box.height = 36 ; box.width = 130	# Height and Width of the window
	box.y=(box.height)/2			#initial coordinates of the robot
	box.x=(box.width)/2 			
#	blink=curses.A_BLINK
	box.s=5						#points for the first game

	def addscreen():			# initialises the screen and makes a box around it
		screen= curses.initscr()
		curses.noecho()				# No character is echoed to the terminal
		curses.curs_set(0)			# set the cursor to invisible
		win = curses.newwin(box.height, box.width, box.begin_y, box.begin_x)	#constructing a new window
		win.box()				#Construct a box around the window.
		win.keypad(1)				#Escape sequences by some keys will be interpreted by curses
		return win

	def definecolors():
		curses.start_color()
		curses.use_default_colors()
		curses.init_pair(4, curses.COLOR_BLUE, -1)	 #blue
		curses.init_pair(3, curses.COLOR_RED, -1)	 #red
		curses.init_pair(2, curses.COLOR_GREEN, -1)	 #green

	def addelements(win, level):			#adds bomb, diffusecodes, robot and enemy robot in the game at random positions
		x1=range(6, box.x)
		x1.extend(range(box.x+1, box.width-8))
		random.shuffle(x1)			#creats a list with random(distinct) numbers excluding x
#		y1=range(1, box.y-2)
#		y1.extend(range(box.y+2, box.height-2))
#		random.shuffle(y1)		#creats a list with random(distinct) numbers excluding y
	
		y1=range(1, box.height/3-2)
		y1.extend(range(box.height/3+1, 2*box.height/3-2))
		y1.extend(range(2*box.height/3+1, box.height-2))
#	del y1[box.height/3-1]; del y1[2*box.height/3-1]
		random.shuffle(y1)
		
		win.addstr(y1[box.d], x1[box.d], "B", curses.color_pair(3))			#adding the bomb
		win.refresh()
		drawrobot(win, box.y-2, box.x-2)
		win.refresh()
		drawenemy(win, level, box.height/3, 1)
		drawenemy(win, level, 2*box.height/3, box.width-6)
		win.refresh()
		for i in range(box.d):
			win.addch(int(y1[i]), int(x1[i]), 'D', curses.color_pair(2))		#adding the diffuse kits(ensures that they are placed on unique coordinates)
			win.refresh()
		if(level>1):									
			for i in range(box.d+2, box.d+1+level*3):	#mines increase if the level increases
				win.addch(int(y1[i]), int(x1[i]), '*', curses.color_pair(3))	#adding the mines(ensures that they are placed on unique coordinates)
				win.refresh()
	
	def drawenemy(win, level, y, x):		#draws the enemy robot onwards level 2
		if(level>=2):
			win.addstr(y-2, x, "  V  ")
			win.addstr(y-1, x, "<~0~>")
			win.addstr(y, x ,  " /_\ ")
			win.addstr(y+1, x, "d   b")
	
	def drawrobot(win, y, x):		#draws the main robot
		win.addstr(y  , x, " |^| ", curses.color_pair(4))
		win.addstr(y+1, x, "<*|*>", curses.color_pair(4))
		win.addstr(y+2, x, "/_~_\\", curses.color_pair(4))
		win.addstr(y+3, x, "J   L", curses.color_pair(4))
	
	def check(count, ch):
		if(ch==580):			
			curses.beep()
			return count+1			#Found a diffuse code	
		elif(ch==834):
			return -1			#collided with bomb
		elif(ch==810 or ch==ord("-")):			
			return -2			#collided with mine or bullet
		elif(ch==ord(" ")):
			return count				#found nothing
		return -2

	def bkgcolor(win):				# Changes the background color (not called in main)
		i=1
		while (i < box.height-1) :
			j=1
			while(j< box.width-1):
				win.addstr(i, j, " ", curses.color_pair(2))
				j+=1
			i+=1
		win.refresh()

	def main(speed, level):
		flag=0		#To see if game is paused or not
		lost=0		#To see if the user loses or not
		count=0		#count of the diffuse kits obtained
		ret=-2
#		global x ; global y		
		xnew=box.x; ynew=box.y		#Make safe copies of x, y
		win=addscreen()		#adds the window
		definecolors()				#colors initialised
		bullet=0				#bullet position
	#	bkgcolor(win)
		addelements(win, level)			#adds robot(s),mines, diffuse codes, bomb 
		event=ord("q")
		while(event != 27):
			win.addstr(0, 2,' Diffuse Codes: '+str(count)+' ')
			win.addstr(box.height-1, box.x-4, 'Level: '+str(level)+' ')
			win.timeout(speed- 15*count ) 			#As robot takes diffuse codes, its speed increases
			key= win.getch()
			if(key==27):
				break;
			if(flag==0):
				if(key==ord("p") or key==ord("P")):		#If paused
					flag=1
					win.addstr(0, box.x, ' Paused!')
					resume=event
				else:
					if(key ==-1 or (key!=KEY_RIGHT and key !=KEY_LEFT and key !=KEY_UP and key!=KEY_DOWN)):
						event=event
					else:
						event=key
			elif(flag==1):
				if(key==ord("p") or key==ord("P")):	#Resume the previous state after p is pressed again
					flag=0
					event=resume
					win.box()
	
			if(event == KEY_RIGHT and flag==0):		#If robot moved right
				if(xnew +2 <box.width-2 and flag==0):	#If robot inside boundary
					
					for i in range(ynew-2,ynew+2):		#To check the neighbouring characteres
						ch=win.inch(i, xnew+3)
						ret=check(count, ch)
						if(ret >= count):
							count=ret
						elif(ret==-2):			#Hits the wall
							lost=1
							break
						elif(ret==-1):			#Hits the bomb
							break
					if(ret==-1 or ret ==-2):
						break
			
					xnew=xnew+1				#update new coordinates

					drawrobot(win, ynew-2, xnew-2)		#Draw the new robot

					win.addch(ynew-2, xnew-3, ' ')		#Delete the previous robot
					win.addch(ynew-1, xnew-3, ' ')
					win.addch(ynew, xnew-3, ' ')
					win.addch(ynew+1, xnew-3, ' ')
	
				elif(xnew+2==box.width-2):		#see if robo hits the wall
					lost=1			#user loses
					break
	
			if(event == KEY_LEFT and flag==0):
				if(xnew -2> 1):
					for i in range(ynew-2,ynew+2):
						ch=win.inch(i, xnew-3)
						ret=check(count, ch)
						if(ret >= count):
							count=ret
						elif(ret==-2):
							lost=1
							break
						elif(ret==-1):
							break
					if(ret==-1 or ret ==-2):
						break
				
					xnew=xnew-1
					
					drawrobot(win, ynew-2, xnew-2)
					win.addch(ynew-2, xnew+3, ' ')
					win.addch(ynew-1, xnew+3, ' ')
					win.addch(ynew, xnew+3, ' ')
					win.addch(ynew+1, xnew+3, ' ')

				elif(xnew-2==1):
					lost=1
					break
	
			if(event == KEY_UP and flag==0):
				if(ynew-2>1):
					for i in range(xnew-2, xnew+3):
						ch=win.inch(ynew-3, i) 
					
						ret=check(count, ch)
						if(ret >= count):
							count=ret
						elif(ret==-2):
							lost=1
							break
						elif(ret==-1):
							break
					if(ret==-1 or ret ==-2):
						break

					ynew=ynew-1

					drawrobot(win, ynew-2, xnew-2)
					win.addch(ynew+2, xnew-2, ' ')
					win.addch(ynew+2, xnew-1, ' ')
					win.addch(ynew+2, xnew, ' ')
					win.addch(ynew+2, xnew+1, ' ')
					win.addch(ynew+2, xnew+2, ' ')

				elif(ynew-2==1):
					lost=1
					break
	
			if(event == KEY_DOWN and flag==0):
				if(ynew+1 < box.height -2 and flag==0):
					for i in range(xnew-2, xnew+3):
						ch=win.inch(ynew+2, i)
						ret=check(count, ch)
						if(ret >= count):
							count=ret
						elif(ret==-2):
							lost=1
							break
						elif(ret==-1):
							break
					if(ret==-1 or ret ==-2):
						break
	
					ynew=ynew+1
	
					drawrobot(win, ynew-2, xnew-2)
					win.addch(ynew-3, xnew-2, ' ')
					win.addch(ynew-3, xnew-1, ' ')
					win.addch(ynew-3, xnew, ' ')
					win.addch(ynew-3, xnew+1, ' ')
					win.addch(ynew-3, xnew+2, ' ')

				elif(ynew+1==box.height -2):
					lost=1
					break
	
			if(level>=2 and flag==0):			#move the bullet forward and see if it hits the bullet
				win.addch(box.height/3-1, 7+(bullet), ' ') 		#1
				win.addch(2*box.height/3-1, box.width-(7+(bullet)), ' ')
				bullet=(bullet+1)%(box.width-8)				#2
				ch=win.inch(box.height/3-1, 7+bullet)			#3
				if(ch!=ord(" ")):					#4
					lost=1						#5
					break						#6
				win.addch(box.height/3-1, 7+(bullet), '-')		#7

				ch=win.inch(2*box.height/3-1, box.width-(7+bullet))
				if(ch!=ord(" ")):
					lost=1
					break
				win.addch(2*box.height/3-1, box.width-(7+(bullet)), '-')
				
		curses.endwin()
		if(count!=box.d):
			lost=1
		return lost
	def result(lost):
		win=addscreen()
		definecolors()
		if(lost==0):
			win.addstr(box.y-2, box.x-14, "Congrats, you won this level",curses.color_pair(2) )
			win.addstr(box.y+1, box.x-16, "Do you want to play next level?(y/n)", curses.color_pair(2))
			while(1):
				nxt=win.getch()
				if(nxt==ord("y") or nxt==ord("n")):
					break
		if(nxt==ord("y")):
			return 'y'
		else:
			curses.endwin()			
			return 'n'
		
		

	def run():
		score=0
		level=1
		levels=10
		lost=main(100, level)
		while(level<levels):
			if lost ==0 :
				score=score+box.s
				box.s+=5
				nxt=result(lost)
				if(nxt=='y'):
					level+=1
					lost=main(180-20*level, level)
				elif(nxt=='n'):
					win=addscreen()
					definecolors()
					win.addstr(box.y-1, box.x-10, 'Your final score : '+str(score)+' ', curses.color_pair(3))
					win.addstr(box.y+2, box.x-10, 'Press ESC to exit', curses.color_pair(3))
					while(1):
						key=win.getch()
						if(key==27):
							break
					curses.endwin()	
					break
			elif(lost==1):
				win=addscreen()
				definecolors()
				win.addstr(box.y-2, box.x-5, "You LOST!", curses.color_pair(3))
				win.addstr(box.y, box.x-10, 'Your final score is ' +str(score)+' ', curses.color_pair(3))
				win.addstr(box.y+2, box.x-8, 'Press ESC to exit', curses.color_pair(3))
				while(1):
					key=win.getch()
					if(key==27):
						break
				
				curses.endwin()
				break

		if(level==levels and lost==0):
			win=addscreen()
			definecolors()
			win.addstr(box.y-2, box.x-10, "You completed all levels!!!", curses.color_pair(2))
			win.addstr(box.y, box.x-10, 'Your final score is ' +str(score)+' ', curses.color_pair(2))
			win.addstr(box.y+2, box.x-10, 'Thanks for playing!', curses.color_pair(2))
			win.addstr(box.y+4, box.x-10, 'Press ESC to exit', curses.color_pair(2))
			while(1):
				key=win.getch()
				if(key==27):
					break
			curses.endwin()
		if(level==levels and lost==1):
			win=addscreen()
			definecolors()
			win.addstr(box.y-2, box.x-5, "You LOST!", curses.color_pair(3))
			win.addstr(box.y, box.x-10, 'Your final score is ' +str(score)+' ', curses.color_pair(3))
			while(1):
				key=win.getch()
				if(key==27):
					break
			curses.endwin()
				
	

	ab=A()
	ab.addscreen=addscreen
	ab.definecolors=definecolors
	ab.addelements=addelements
	ab.drawenemy=drawenemy
	ab.drawrobot=drawrobot
	ab.check=check
	ab.bkgcolor=bkgcolor
	ab.main=main
	ab.run=run
#	ab.width=width
#	ab.height=height
	return ab
