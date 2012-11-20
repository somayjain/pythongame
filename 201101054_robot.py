import game, instructions
status=instructions.inst()
if(status!=-1):
	robot=game.robomake()
	robot.run()
