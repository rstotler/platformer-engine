import pygame, random, Sprite
from pygame import *

def LoadCharacter(o):

	# Attacks #
	o.attackList['basic attack'] = AttackData('basic attack')
	o.attackList['dual attack'] = AttackData('dual attack')
	o.attackList['circle attack'] = AttackData('circle attack')
	o.attackList['charged circle attack'] = AttackData('charged circle attack')
	o.attackList['bullet attack'] = AttackData('bullet attack')
	o.attackList['charged strike'] = AttackData('charged strike')
	
	o.sprite = Sprite.LoadAnimated(o.id)
	
	# Character Data #
	if o.id == 'alucard':
		o.rect = pygame.rect.Rect([0,0],[20,46])
		o.maxSpeed = 5
		o.stepSize = 10
		o.maxJumps = 'infinite'
		
	elif o.id == 'samus':
		o.rect = pygame.rect.Rect([0,0],[26,43])
		o.maxSpeed = 6
		o.stepSize = 10
		o.maxJumps = 'infinite'
		o.sprite.speed = 80
	
	elif o.id == 'shinobi':
		o.rect = pygame.rect.Rect([0,0],[20,34])
		o.maxSpeed = 8
		o.stepSize = 10
		o.maxJumps = 'infinite'
		o.sprite.speed = 80
		o.attackKeyBinding[2] = 'charged strike'
		
	# Sprite Mods #
	if o.sprite.loaded:
		
		# Frame Capping #
		if 'jump up left' in o.sprite.frame : o.sprite.frame['jump up left'][-1].timeLength = None
		if 'jump up right' in o.sprite.frame : o.sprite.frame['jump up right'][-1].timeLength = None
		if 'jump side left' in o.sprite.frame : o.sprite.frame['jump side left'][-1].timeLength = None
		if 'jump side right' in o.sprite.frame : o.sprite.frame['jump side right'][-1].timeLength = None
		if 'fall left' in o.sprite.frame : o.sprite.frame['fall left'][-1].timeLength = None
		if 'fall right' in o.sprite.frame : o.sprite.frame['fall right'][-1].timeLength = None
		if 'hurt right' in o.sprite.frame : o.sprite.frame['hurt right'][-1].timeLength = None
		if 'hurt left' in o.sprite.frame : o.sprite.frame['hurt left'][-1].timeLength = None
		
		# X Aligning #
		for frameType in o.sprite.frame:
			if 'right' in frameType:
				for f in o.sprite.frame[frameType]:
					f.xMod = -f.w + o.rect.width
				
		# Character Mods Go Here, Not Above! #
		if o.id == 'alucard':
		
			o.sprite.frame['walk left'][14].xMod =- 3
			o.sprite.frame['walk right'][14].xMod += 3
		
			o.sprite.frame['walk left'][1].yMod = 1
			o.sprite.frame['walk left'][2].yMod = -2
			o.sprite.frame['walk left'][3].yMod = 2
			o.sprite.frame['walk left'][4].yMod = 4
			o.sprite.frame['walk left'][5].yMod = 5
			o.sprite.frame['walk left'][6].yMod = 5
			o.sprite.frame['walk left'][7].yMod = 2
			o.sprite.frame['walk left'][8].yMod = 1
			o.sprite.frame['walk left'][9].yMod = 1
			o.sprite.frame['walk left'][10].yMod = 1
			o.sprite.frame['walk left'][11].yMod = 2
			o.sprite.frame['walk left'][12].yMod = 3
			o.sprite.frame['walk left'][13].yMod = 3
			o.sprite.frame['walk left'][14].yMod = 4
			o.sprite.frame['walk left'][15].yMod = 2
			
			o.sprite.frame['walk right'][1].yMod = 1
			o.sprite.frame['walk right'][2].yMod = -2
			o.sprite.frame['walk right'][3].yMod = 2
			o.sprite.frame['walk right'][4].yMod = 4
			o.sprite.frame['walk right'][5].yMod = 5
			o.sprite.frame['walk right'][6].yMod = 5
			o.sprite.frame['walk right'][7].yMod = 2
			o.sprite.frame['walk right'][8].yMod = 1
			o.sprite.frame['walk right'][9].yMod = 1
			o.sprite.frame['walk right'][10].yMod = 1
			o.sprite.frame['walk right'][11].yMod = 2
			o.sprite.frame['walk right'][12].yMod = 3
			o.sprite.frame['walk right'][13].yMod = 3
			o.sprite.frame['walk right'][14].yMod = 4
			o.sprite.frame['walk right'][15].yMod = 2
		
		elif o.id == 'shinobi':
			
			o.sprite.frame['stand right'][1].xMod = 0
			o.sprite.frame['stand right'][2].xMod = 0
			o.sprite.frame['stand right'][3].xMod = 0
			o.sprite.frame['stand left'][1].xMod = -1
			o.sprite.frame['stand left'][2].xMod = -2
			o.sprite.frame['stand left'][3].xMod = -1
			
			o.sprite.frame['stand right'][1].yMod = 1
			o.sprite.frame['stand right'][2].yMod = 2
			o.sprite.frame['stand right'][3].yMod = 1
			o.sprite.frame['stand left'][1].yMod = 1
			o.sprite.frame['stand left'][2].yMod = 2
			o.sprite.frame['stand left'][3].yMod = 1
			
			o.sprite.frame['walk right'][0].xMod = 0
			o.sprite.frame['walk right'][0].yMod = 3
			o.sprite.frame['walk right'][1].xMod = -2
			o.sprite.frame['walk right'][1].yMod = 2
			o.sprite.frame['walk right'][2].xMod = -7
			o.sprite.frame['walk right'][2].yMod = 4
			o.sprite.frame['walk right'][3].xMod = -9
			o.sprite.frame['walk right'][3].yMod = 3
			o.sprite.frame['walk right'][4].xMod = -11
			o.sprite.frame['walk right'][4].yMod = 4
			o.sprite.frame['walk right'][5].xMod = -9
			o.sprite.frame['walk right'][5].yMod = 2
			o.sprite.frame['walk right'][6].xMod = -3
			o.sprite.frame['walk right'][6].yMod = 0
			o.sprite.frame['walk right'][7].xMod = 0
			o.sprite.frame['walk right'][7].yMod = 1
			o.sprite.frame['walk right'][8].xMod = 0
			o.sprite.frame['walk right'][8].yMod = 1
			o.sprite.frame['walk right'][9].xMod = 0
			o.sprite.frame['walk right'][9].yMod = 2
			
			o.sprite.frame['walk left'][0].xMod = 0
			o.sprite.frame['walk left'][0].yMod = 3
			o.sprite.frame['walk left'][1].xMod = -4
			o.sprite.frame['walk left'][1].yMod = 2
			o.sprite.frame['walk left'][2].xMod = -7
			o.sprite.frame['walk left'][2].yMod = 4
			o.sprite.frame['walk left'][3].xMod = -5
			o.sprite.frame['walk left'][3].yMod = 3
			o.sprite.frame['walk left'][4].xMod = -1
			o.sprite.frame['walk left'][4].yMod = 4
			o.sprite.frame['walk left'][5].xMod = 0
			o.sprite.frame['walk left'][5].yMod = 2
			o.sprite.frame['walk left'][6].xMod = 2
			o.sprite.frame['walk left'][6].yMod = 0
			o.sprite.frame['walk left'][7].xMod = 1
			o.sprite.frame['walk left'][7].yMod = 1
			o.sprite.frame['walk left'][8].xMod = 0
			o.sprite.frame['walk left'][8].yMod = 1
			o.sprite.frame['walk left'][9].xMod = 0
			o.sprite.frame['walk left'][9].yMod = 2
			
			o.sprite.frame['jump up left'][1].xMod = -3
			o.sprite.frame['jump up left'][1].yMod = -1
			o.sprite.frame['jump up left'][2].xMod = -4
			o.sprite.frame['jump up left'][2].yMod = -1
			
			o.sprite.frame['jump up right'][1].xMod = -2
			o.sprite.frame['jump up right'][1].yMod = -1
			o.sprite.frame['jump up right'][2].xMod = -4
			o.sprite.frame['jump up right'][2].yMod = -1
				
class AttackData:

	def __init__(self,id):
	
		self.id = id
		self.frameData = []
		self.collideShape = None
		self.attackType = 'parented'
		self.flags = {}
		
		if id == 'basic attack':
			self.collideShape = 'rect'
			f = AttackDataFrame(20,5,60,20)
			self.frameData = [f]
			
		elif id == 'dual attack':
			self.collideShape = 'rect'
			f1 = AttackDataFrame(20,5,60,20)
			f2 = AttackDataFrame(-60,10,40,10)
			self.frameData = [f1,f2]
			
		elif id == 'circle attack':
			self.collideShape = 'circle'
			size = 50
			f = AttackDataFrame(30,-10,size,size)
			f.timeLength = 2
			self.frameData = [f]
			self.attackType = 'projectile'
			self.flags['repeater'] = {'time':.2, 'idNumTime':{}}
			
		elif id == 'charged circle attack':
			self.collideShape = 'circle'
			size = 100
			f = AttackDataFrame(30,-20,size,size)
			f.timeLength = 2
			self.frameData = [f]
			self.attackType = 'projectile'
			self.flags['charge attack'] = {'time':.3}
			self.flags['repeater'] = {'time':.2, 'idNumTime':{}}
			self.flags['disable movement while charging'] = True
			
		elif id == 'bullet attack':
			self.collideShape = 'circle'
			size = 4
			f = AttackDataFrame(30,10,size,size)
			f.timeLength = 4
			self.frameData = [f]
			self.attackType = 'projectile'
			self.flags['speed'] = 1500
			self.flags['destroy on collide'] = True
			self.flags['collide with walls'] = True
			
		elif id == 'charged strike':
			self.collideShape = 'rect'
			f = AttackDataFrame(20,-5,65,35)
			self.frameData = [f]
			self.flags['charge attack'] = {'time':.3}
			
	def GetAttack(self,oRect,facingDir):
	
		f1 = self.frameData[0]
		
		a = Attack(self.id,self.attackType,self.collideShape,self.flags)
		a.rect.width = f1.w
		a.rect.height = f1.h
		a.rect.left = oRect.left + (oRect.width/2) + f1.xMod
		if facingDir == 'left' : a.rect.left = oRect.left + (oRect.width/2) - (a.rect.width + f1.xMod)
		a.rect.top = oRect.top + f1.yMod
		
		if a.attackType == 'projectile':
			if facingDir == 'left' : dirMod = -1
			else : dirMod = 1
			defaultVel = 500
			if 'speed' in self.flags : defaultVel = self.flags['speed']
			a.xVel = defaultVel * dirMod
		
		return a
	
class AttackDataFrame:

	def __init__(self,xMod,yMod,w,h):
	
		self.xMod = xMod
		self.yMod = yMod
		self.w = w
		self.h = h
		
		self.timeLength = .15
	
class Attack:
	
	def __init__(self,id,attackType,collideShape,flags):
	
		self.id = id
		self.idNum = random.randrange(100000000,999999999)
		self.type = 'attack'
		self.rect = pygame.rect.Rect([0,0],[1,1])
		self.collideShape = collideShape
		self.currentTime = 0
		self.currentFrame = 0
		self.attackType = attackType
		self.flags = flags
		self.xVel = 0
		self.yVel = 0
		self.hitObjectsList = {}
		
	def Update(self,dt,aData,oRect,facingDir):
		
		# Frame Updates #
		self.currentTime += 1 * dt
		f = aData.frameData[self.currentFrame]
		
		if self.currentTime >= f.timeLength:
			self.currentTime = 0
			self.currentFrame += 1
			
			if self.currentFrame >= len(aData.frameData) : return 'attack finish'
			else:
				newFrame = aData.frameData[self.currentFrame]
				self.rect.width = newFrame.w
				self.rect.height = newFrame.h
				self.rect.left = oRect.left + (oRect.width/2) + newFrame.xMod
				if facingDir == 'left' : self.rect.left = oRect.left + (oRect.width/2) - (self.rect.width + newFrame.xMod)
				self.rect.top = newFrame.yMod + oRect.top
				
		# Frame Update Data #
		if self.attackType == 'parented':
			f = aData.frameData[self.currentFrame]
			self.rect.left = oRect.left + (oRect.width/2) + f.xMod
			if facingDir == 'left' : self.rect.left = oRect.left + (oRect.width/2) - (self.rect.width + f.xMod)
			self.rect.top = f.yMod + oRect.top
			
		elif self.attackType == 'projectile':
			self.rect.left += dt * self.xVel
			
		if 'repeater' in self.flags and 'time' in self.flags['repeater'] and 'idNumTime' in self.flags['repeater']:
			repeaterDelList = []
			for idNum in self.flags['repeater']['idNumTime']:
				self.flags['repeater']['idNumTime'][idNum] -= 1 * dt
				if self.flags['repeater']['idNumTime'][idNum] <= 0:
					repeaterDelList.append(idNum)
			for idNum in repeaterDelList:
				del self.flags['repeater']['idNumTime'][idNum]
				if idNum in self.hitObjectsList : del self.hitObjectsList[idNum]
		
	def Display(self,window,loc):
	
		x = self.rect.left + loc[0]
		y = self.rect.top + loc[1]
		
		if self.collideShape == 'rect' : pygame.draw.rect(window,[255,0,0],[x,y,self.rect.w,self.rect.h])
		elif self.collideShape == 'circle' : pygame.draw.circle(window,[255,0,0],[x+(self.rect.width/2),y+(self.rect.height/2)],self.rect.width/2)
		