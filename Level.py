import random, Object

class Cell:

	def __init__(self,xNum,yNum):
	
		self.xNum = xNum
		self.yNum = yNum
		
		self.objects = []

def Load(id,cellSize,player):

	cells = []
	
	# Default Player Loc #
	if player[1] != None : player[1].rect.left = 200
	if player[2] != None : player[2].rect.left = 300
	
	for xNum in range(250):
		cells.append([])
		for yNum in range(50):
			cell = Cell(xNum,yNum)
			cells[-1].append(cell)
	
	if id == 'wave':
	
		y = 500 ; dir = 'up' ; stepSize = 10
		for x in range(len(cells)):
			
			if random.randrange(0,4) == 0:
				if dir == 'up' : dir = 'down'
				elif dir == 'down' : dir = 'up'
			if dir == 'down' and y > len(cells) * cellSize : dir = 'up'
			elif dir == 'up' and y < 0 : dir = 'down'
			
			if dir == 'up' : y -= stepSize
			else : y += stepSize
			
			#if random.randrange(0,7) != 0:
			LoadObject('object','square',[10+(x*cellSize)-(x*10),y],cells,cellSize)
				
	elif id == 'debug level':
	
		# Floors #
		LoadObject('object','floor',[0,800],cells,cellSize)
		LoadObject('object','floor',[1000,800],cells,cellSize)
		LoadObject('object','floor',[2000,800],cells,cellSize)
		LoadObject('object','floor',[3000,800],cells,cellSize)
		LoadObject('object','floor',[4000,800],cells,cellSize)
		
		# First Area #
		LoadObject('object','circle',[150,170],cells,cellSize)
		LoadObject('object','small right 45',[50,750],cells,cellSize)
		LoadObject('object','small left 45',[105,750],cells,cellSize)
		LoadObject('object','mountain ramp right',[270,300],cells,cellSize)
		LoadObject('object','mountain ramp left',[421,300],cells,cellSize)
		LoadObject('object','wall',[1000,300],cells,cellSize)
		LoadObject('object','small right 45',[950,750],cells,cellSize)
		LoadObject('object','mountain ramp left',[1050,300],cells,cellSize)
		
		# Bumps #
		LoadObject('object','small right 45',[1200,750],cells,cellSize)
		LoadObject('object','floor 2',[1250,750],cells,cellSize)
		LoadObject('object','small left 45',[1450,750],cells,cellSize)	
		LoadObject('object','small right 45',[1600,750],cells,cellSize)
		LoadObject('object','floor 2',[1650,755],cells,cellSize)
		LoadObject('object','small left 45',[1850,750],cells,cellSize)
		
		# Big Ramps #
		LoadObject('object','circle',[1900,470],cells,cellSize)
		LoadObject('object','long ramp right',[2000,600],cells,cellSize)
		LoadObject('object','test ramp left',[3300,600],cells,cellSize)
		
		for x in range(5) : LoadObject('object','test moveable square',[3000+x*100,300],cells,cellSize)
		for x in range(10) : LoadObject('object','test collectable item',[3000+x*50,200],cells,cellSize)
		
		LoadObject('mob','samus',[2700,200],cells,cellSize)
		
	elif id == 'combat debug':
		
		if player[1] != None : player[1].rect.left = 450
		if player[2] != None : player[2].rect.left = 850 ; player[2].facingDir = 'left'
		
		LoadObject('object','floor',[150,800],cells,cellSize)
		LoadObject('object','floor 2',[300,600],cells,cellSize)
		LoadObject('object','floor 2',[800,600],cells,cellSize)
		
	elif id == 'random test':
	
		x = 100
	
		for platformNum in range(50):
			
			y = random.randrange(1000,1500)
			
			# Start Wall
			o = LoadObject('object','small right 45',[x,y],cells,cellSize) ; x += o.rect.width
			LoadObject('object','long wall',[x-o.rect.width-1,y+o.rect.height],cells,cellSize)
			o = LoadObject('object','floor 3',[x,y],cells,cellSize) ; x += o.rect.width
			
			for num in range(random.randrange(2,10)):

				# Step Up #
				if random.randrange(0,2) == 1:
					y -= 50
					o = LoadObject('object','small right 45',[x,y],cells,cellSize)
					x += o.rect.width
					o = LoadObject('object',random.choice(['floor 3','floor 4','floor 5']),[x,y],cells,cellSize) ; x += o.rect.width
				
				# Step Down #
				else:
					o = LoadObject('object','small left 45',[x,y],cells,cellSize)
					x += o.rect.width ; y += o.rect.height
					o = LoadObject('object',random.choice(['floor 3','floor 4','floor 5']),[x,y],cells,cellSize) ; x += o.rect.width
			
			# End Wall
			o = LoadObject('object','small left 45',[x,y],cells,cellSize) ; x += o.rect.width
			LoadObject('object','long wall',[x-o.rect.width+1,y+o.rect.height],cells,cellSize)
			
			x += random.randrange(150,600)
		
	return cells

def LoadObject(type,id,loc,cells,cellSize):

	o = Object.Load(type,id)
	
	o.rect.left = loc[0]
	o.rect.top = loc[1]
	
	if o.collideShape == 'ramp':
		o.points = [[o.rect.left,o.rect.bottom],[o.rect.right,o.rect.bottom]]
		if o.flags['ramp direction'] == 'left' : o.points.append([o.rect.left,o.rect.top])
		elif o.flags['ramp direction'] == 'right' : o.points.append([o.rect.right,o.rect.top])

	w = 1
	h = 1
	if o.rect.width > cellSize : w += (o.rect.width / cellSize)
	if o.rect.height > cellSize : h += (o.rect.height / cellSize)
	if (o.rect.width % cellSize) + (o.rect.left % cellSize) > cellSize : w += 1
	if (o.rect.height % cellSize) + (o.rect.top % cellSize) > cellSize : h += 1
	
	xLoc = o.rect.left / cellSize
	yLoc = o.rect.top / cellSize
	cellList = []
	
	if xLoc < len(cells) and yLoc < len(cells[0]) and xLoc > -1 and yLoc > -1:
		startLoc = [xLoc,yLoc]
		for xNum in range(w):
			x = xLoc + xNum
			for yNum in range(h):
				y = yLoc + yNum
				if x < len(cells) and y < len(cells[0]):
					cellList.append([x,y])
	
	if len(cellList) > 0:
	
		o.cellList = cellList
		objectPart = Object.Part(id,o.idNum,cellList)
	
		for cellLoc in cellList:
			
			x = cellLoc[0]
			y = cellLoc[1]
			
			if x == startLoc[0] and y == startLoc[1] : newObject = o
			else : newObject = objectPart
			
			cells[x][y].objects.append(newObject)
			
	return o
	