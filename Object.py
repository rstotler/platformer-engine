import pygame, random, math, PygTools, Sprite, CharacterData
from pygame import *

class Load:

	def __init__(self,type,id=None,loadFlags={}):
	
		self.type = type
		self.collideShape = None
		self.idNum = random.randrange(100000000,999999999)
		self.id = id
		self.flags = {}
		self.static = True
		self.cellList = []
		self.attackList = {}
		self.currentAttacks = []
		self.currentCharging = None
		self.attackKeyBinding = None
		
		self.sprite = None
		self.facingDir = 'right'
		
		self.hitEffect = {}
		self.hp = None
		
		self.rect = None
		self.points = None
		self.angle = None
		self.color = [255,0,255]
		
		self.xVel = 0
		self.yVel = 0
		
		self.speedMod = 1
		
		self.moveCheck = False
		self.hitFlashTimer = 0
		
		self.grounded = False
		self.moveSpeed = 30
		self.maxSpeed = 0
		self.stepSize = 0
		
		self.jumpCount = 0
		self.jumpTime = 0
		self.maxJumps = 1
		self.maxJumpTime = 10
		self.jumpKey = False
		self.jumpKeyReset = True
		
		self.autoMove = False
		self.autoMoveDir = None
		
		# Process Load Flags #
		if 'player num' in loadFlags:
			self.flags['player num'] = loadFlags['player num']
		
		self.LoadData()
		
	def Display(self,window,loc,flags,spriteSheet=None):
	
		ox = self.rect.left + loc[0]
		oy = self.rect.top + loc[1]
	
		if 'collide box' not in flags and self.sprite == None:
			if self.collideShape == 'rect':
				pygame.draw.rect(window,self.color,(ox,oy,self.rect.width,self.rect.height))
			
			elif self.collideShape == 'ramp':
				if self.flags['ramp direction'] == 'right' : pygame.draw.polygon(window,self.color,[[ox,oy+self.rect.height],[ox+self.rect.width,oy],[ox+self.rect.width,oy+self.rect.height]])
				elif self.flags['ramp direction'] == 'left' : pygame.draw.polygon(window,self.color,[[ox,oy],[ox,oy+self.rect.height],[ox+self.rect.width,oy+self.rect.height]])
			
			elif self.collideShape == 'circle':
				pygame.draw.circle(window,self.color,[ox+(self.rect.width/2),oy+(self.rect.width/2)],self.rect.width/2)
		
		# Sprite #
		if self.sprite != None and self.sprite.loaded and spriteSheet != None:
			if self.sprite.type == 'animated' : self.sprite.Display(window,(ox,oy),self.facingDir,spriteSheet)
			elif self.sprite.type == 'still' : self.sprite.Display(window,(ox,oy),spriteSheet)
		
		# Hit Flash #
		if self.hitFlashTimer != 0:
			if self.collideShape == 'rect':
				pygame.draw.rect(window,[255,0,0],(ox,oy,self.rect.width,self.rect.height))
			elif self.collideShape == 'circle':
				pygame.draw.circle(window,[255,0,0],[ox+(self.rect.width/2),oy+(self.rect.width/2)],self.rect.width/2)
		
		if 'collide box' in flags:
			outlineColor = [255,0,0]
			if self.currentCharging != None:
				outlineColor = [0,0,255]
				if self.currentCharging['current time'] >= self.currentCharging['charge time'] : outlineColor = [0,255,0]
			PygTools.Outline(window,outlineColor,[ox,oy],[self.rect.width,self.rect.height])
		
		# Attacks #
		for a in self.currentAttacks:
			a.Display(window,loc)
			
	def LoadData(self):
	
		if self.type == 'player':
			self.collideShape = 'rect'
			self.rect = pygame.rect.Rect([0,0],[50,50])
			self.static = False
			self.color = [255,0,0]
			self.hp = 50
			self.attackKeyBinding = {1:'basic attack', 2:'bullet attack', 3:'charged circle attack'}
			
			CharacterData.LoadCharacter(self)
			
		elif self.type == 'object':
			self.LoadObjectData()
			
		elif self.type == 'mob':
			self.collideShape = 'rect'
			self.rect = pygame.rect.Rect([0,0],[50,50])
			self.static = False
			self.color = [150,0,255]
			self.hp = 50
			
			CharacterData.LoadCharacter(self)
			
	def LoadObjectData(self):
	
		if self.id == 'square':
			self.collideShape = 'rect'
			size = [100,100]
			self.color = [255,0,0]
			
		elif self.id == 'square 2':
			self.collideShape = 'rect'
			size = [80,80]
			self.color = [0,0,255]
		
		elif self.id == 'floor':
			self.collideShape = 'rect'
			size = [1000,30]
			self.color = [0,150,0]
			
		elif self.id == 'floor 2':
			self.collideShape = 'rect'
			size = [200,30]
			self.color = [0,0,150]
			self.flags['ignore on ramps'] = True
			
		elif self.id == 'floor 3':
			self.collideShape = 'rect'
			size = [400,30]
			self.color = [0,0,150]
			self.flags['ignore on ramps'] = True
			
		elif self.id == 'floor 4':
			self.collideShape = 'rect'
			size = [200,30]
			self.color = [0,0,150]
			self.flags['ignore on ramps'] = True
			
		elif self.id == 'floor 5':
			self.collideShape = 'rect'
			size = [100,30]
			self.color = [0,0,150]
			self.flags['ignore on ramps'] = True
			
		elif self.id == 'wall':
			self.collideShape = 'rect'
			size = [50,500]
			self.color = [150,150,250]
			
		elif self.id == 'wall 2':
			self.collideShape = 'rect'
			size = [50,650]
			self.color = [50,50,150]
			
		elif self.id == 'long wall':
			self.collideShape = 'rect'
			size = [50,2000]
			self.color = [50,50,150]
			
		elif self.id == 'small right 45':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'right'
			self.flags['ignore rects'] = True
			self.flags['ignore ramps'] = True
			size = [50,50]
			self.color = [200,50,0]
		
		elif self.id == 'small left 45':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'left'
			self.flags['ignore rects'] = True
			self.flags['ignore ramps'] = True
			size = [50,50]
			self.color = [200,0,50]
		
		elif self.id == 'mountain ramp left':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'left'
			self.flags['ignore ramps'] = True
			size = [100,500]
			self.color = [0,200,50]
		
		elif self.id == 'mountain ramp right':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'right'
			self.flags['ignore ramps'] = True
			size = [150,500]
			self.color = [50,200,0]
		
		elif self.id == 'long ramp right':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'right'
			size = [1000,200]
			self.color = [50,200,120]
		
		elif self.id == 'test ramp left':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'left'
			size = [200,200]
			self.color = [55,255,100]
		
		elif self.id == 'ramp medium left 45':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'left'
			size = [100,100]
			self.color = [0,200,0]
		
		elif self.id == 'ramp medium right 45':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'right'
			size = [100,100]
			self.color = [0,200,0]
		
		elif self.id == 'ramp medium right 45':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'right'
			size = [100,100]
			self.color = [0,200,0]
		
		elif self.id == 'ramp large left 45':
			self.collideShape = 'ramp'
			self.flags['ramp direction'] = 'left'
			size = [300,300]
			self.color = [0,200,0]
		
		elif self.id == 'circle':
			self.collideShape = 'circle'
			size = [100,100]
			self.color = [0,200,200]
		
		elif self.id == 'test bg square':
			self.collideShape = 'rect'
			size = [40,40]
			self.color = [255,255,255]
			self.flags['background'] = True
			
		elif self.id == 'test moveable square':
			self.collideShape = 'rect'
			size = [64,64]
			self.color = [255,255,0]
			self.static = False
			self.flags['moveable'] = True
			self.sprite = Sprite.LoadStill('medium stone block 1')
		
		elif self.id == 'test collectable item':
			self.collideShape = 'circle'
			size = [20,20]
			self.color = [255,0,0]
			self.flags['item'] = True
		
		else:
			self.id = 'error'
			self.collideShape = 'rect'
			size = [100,100]
			self.color = [255,0,255]
			self.flags['background'] = True
		
		self.rect = pygame.rect.Rect([0,0],size)
		if self.collideShape == 'ramp' : self.angle = self.LoadRampAngle(size)
		
		# Set Ramp Triangle Points #
		if self.collideShape == 'ramp':
			self.points = [[self.rect.left,self.rect.bottom],[self.rect.right,self.rect.bottom]]
			if self.flags['ramp direction'] == 'left' : self.points.append([self.rect.left,self.rect.top])
			elif self.flags['ramp direction'] == 'right' : self.points.append([self.rect.right,self.rect.top])
		
		# Random Colors #
		self.color = [random.randrange(0,256),random.randrange(0,256),random.randrange(0,256)]
				
	def LoadRampAngle(self,size):
		import math
	
		a = math.atan((size[1]+.0)/size[0])
		a = math.degrees(a)
		a = abs(int(a))
		
		return a
				
	def Update(self,gravity,dt):
	
		if self.hitFlashTimer > 0:
			self.hitFlashTimer -= 1 * dt
			if self.hitFlashTimer < 0 : self.hitFlashTimer = 0
	
		if 'disable' in self.hitEffect:
			self.hitEffect['disable'] -= dt * 1
			if self.hitEffect['disable'] <= 0:
				del self.hitEffect['disable']
				
		if self.currentCharging != None and self.currentCharging['current time'] < self.currentCharging['charge time']:
			self.currentCharging['current time'] += dt * 1
	
		if self.type == 'mob':
			self.UpdateMob(dt)
			
		# X Sprites #
		if self.sprite != None and self.sprite.type == 'animated' and self.xVel == 0 and self.grounded and self.sprite.level != 'stand':
			self.sprite.level = 'stand'
			self.sprite.currentFrame = 0
			self.sprite.currentTime = 0
			
		# Y Sprites #
		elif self.sprite != None and self.sprite.type == 'animated' and not self.grounded and self.yVel > 0:
			if ('fall left' in self.sprite.frame or 'fall right' in self.sprite.frame) and self.sprite.level != 'fall':
				self.sprite.level = 'fall'
				self.sprite.currentFrame = 0
				self.sprite.currentTime = 0
			elif ('fall left' not in self.sprite.frame and 'fall right' not in self.sprite.frame) and ('jump up left' in self.sprite.frame or 'jump up right' in self.sprite.frame) and self.sprite.level != 'jump up':
				self.sprite.level = 'jump up'
				self.sprite.currentFrame = 0
				self.sprite.currentTime = 0
			
		if self.sprite != None and self.sprite.type == 'animated' : self.sprite.Update(self.facingDir,dt)
		
	def ProcessInput(self,dt,pId,keyboard):

		canMoveCheck = True
		if 'disable' in self.hitEffect and self.hitEffect['disable'] > 0 : canMoveCheck = False
		elif self.currentCharging != None and 'disable movement while charging' in self.currentCharging['flags'] : canMoveCheck = False
	
		self.moveCheck = False
	
		for keyEvent in keyboard.events:
			keyboard.key[keyEvent] = keyboard.events[keyEvent]
			if pId == 1:
				if keyEvent == 'a' and keyboard.key[keyEvent] and self.facingDir != 'left' : self.facingDir = 'left'
				elif keyEvent == 'd' and keyboard.key[keyEvent] and self.facingDir != 'right' : self.facingDir = 'right'
				if keyEvent == 'a' and not keyboard.key[keyEvent] and not keyboard.key['d'] and self.xVel != 0 : self.xVel = 0
				if keyEvent == 'd' and not keyboard.key[keyEvent] and not keyboard.key['a'] and self.xVel != 0 : self.xVel = 0
			elif pId == 2:
				if keyEvent == 'left' and keyboard.key[keyEvent] and self.facingDir != 'left' : self.facingDir = 'left'
				elif keyEvent == 'right' and keyboard.key[keyEvent] and self.facingDir != 'right' : self.facingDir = 'right'
				if keyEvent == 'left' and not keyboard.key[keyEvent] and not keyboard.key['right'] and self.xVel != 0 : self.xVel = 0
				if keyEvent == 'right' and not keyboard.key[keyEvent] and not keyboard.key['left'] and self.xVel != 0 : self.xVel = 0
				
		# Up #
		if canMoveCheck:
			if (pId == 1 and keyboard.key['w']) or (pId == 2 and keyboard.key['up']):
			
				if not self.moveCheck : self.moveCheck = True
			
				if not self.jumpKey and (self.maxJumps == 'infinite' or self.jumpCount < self.maxJumps):
					self.Jump()
					
				elif self.jumpKey and self.jumpTime < self.maxJumpTime and self.jumpKeyReset:
					self.yVel -= 120 * dt
					self.jumpTime += 1
			
			else:
				self.jumpKey = False
				self.jumpKeyReset = True
			
		# Left / Right #
		if pId == 1:
			if keyboard.key['a'] != keyboard.key['d']:
				if canMoveCheck:
					if keyboard.key['a'] : self.Move(dt,-1)
					elif keyboard.key['d'] : self.Move(dt,1)
			
			#elif self.xVel != 0:
			#	self.xVel = 0
			#	if not self.grounded : self.speedMod = 1
			
		elif pId == 2:
			if keyboard.key['left'] != keyboard.key['right']:
				if canMoveCheck:
					if keyboard.key['left'] : self.Move(dt,-1)
					elif keyboard.key['right'] : self.Move(dt,1)
					
			#elif self.xVel != 0:
			#	self.xVel = 0
			#	if not self.grounded : self.speedMod = 1
			
	def AttackButton(self,button,pressed):
	
		if 'disable' not in self.hitEffect or self.hitEffect['disable'] == 0:
		
			attackId = self.attackKeyBinding[button]
		
			if attackId in self.attackList:
				aData = self.attackList[attackId]
				a = aData.GetAttack(self.rect,self.facingDir)
				
				if pressed:
					if 'charge attack' in a.flags and 'time' in a.flags['charge attack']:
						self.currentCharging = {}
						self.currentCharging['attackId'] = attackId
						self.currentCharging['charge time'] = a.flags['charge attack']['time']
						self.currentCharging['current time'] = 0
						self.currentCharging['flags'] = {}
						if 'disable movement while charging' in a.flags:
							self.currentCharging['flags']['disable movement while charging'] = True
							if self.grounded and self.xVel != 0 : self.xVel = 0
					else : self.currentAttacks.append(a)
					
				else:
					if self.currentCharging != None and attackId == self.currentCharging['attackId']:
						if self.currentCharging['current time'] >= self.currentCharging['charge time']:
							self.currentAttacks.append(a)
							self.currentCharging = None
						else:
							self.currentCharging = None
				
	def UpdateMob(self,dt):
	
		if random.randrange(0,25) == 0:
			if self.autoMove : self.autoMove = False
			else:
				self.autoMove = True
				self.autoMoveDir = random.choice([1,-1])
			
		if self.autoMove:
			if random.randrange(0,50) == 0:
				if self.autoMoveDir == -1 : self.autoMoveDir = 1
				else : self.autoMoveDir = -1
			self.Move(dt,self.autoMoveDir)
			if random.randrange(0,25) == 0:
				self.Jump()
	
	def Jump(self):
	
		self.jumpTime = 0
		self.jumpCount += 1
		self.jumpKey = True
		self.jumpKeyReset = True
		self.grounded = False
		self.yVel = -10
		
		if self.xVel == 0:
			self.sprite.level = 'jump up'
			#if self.speedMod != 1 : self.speedMod = 1
			
		else:
			if 'jump side left' in self.sprite.frame or 'jump side right' in self.sprite.frame : self.sprite.level = 'jump side'
			elif 'jump up left' in self.sprite.frame or 'jump up right' in self.sprite.frame : self.sprite.level = 'jump up'
		
	def LandOnGround(self):
		
		if self.type in ['player','mob'] and self.xVel != 0:
			if (not self.moveCheck or self.currentCharging != None and 'disable movement while charging' in self.currentCharging['flags']):
				self.xVel = 0
		
		self.yVel = 0
		self.grounded = True
		
		self.jumpCount = 0
		self.jumpTime = 0
		self.jumpKeyReset = False
		
	def Move(self,dt,moveDir):
	
		if not self.moveCheck : self.moveCheck = True
	
		if moveDir == -1:
			if self.xVel > 0 : self.xVel = 0
			# ; self.speedMod = 1
		elif moveDir == 1:
			if self.xVel < 0 : self.xVel = 0
			# ; self.speedMod = 1
	
		self.xVel += (moveDir*self.moveSpeed) * dt
		if self.xVel < -self.maxSpeed : self.xVel = -self.maxSpeed
		if self.xVel > self.maxSpeed : self.xVel = self.maxSpeed
		
		if self.grounded : self.sprite.level = 'walk'
		elif self.yVel < 0 and not self.grounded and self.sprite.level != 'jump side' and ('jump side left' in self.sprite.frame or 'jump side right' in self.sprite.frame):
			self.sprite.level = 'jump side'
			self.sprite.currentFrame = 0
			self.sprite.currentTime = 0
		
	def Dash(self):
	
		pass
	
		#if self.xVel != 0:
		#	self.speedMod = 2.0
		
	def GetHit(self,dt,attackDir,a):
		
		# Temp - Armor Skin? #
		if self.currentCharging != None : self.currentCharging = None
		
		self.hitFlashTimer = .1
		
		disableTime = .25
		if 'disable' in self.hitEffect and disableTime < self.hitEffect['disable'] : pass
		else : self.hitEffect['disable'] = disableTime
		
		if attackDir == 'right' : xMod = -1
		elif attackDir == 'left' : xMod = 1
		self.xVel -= 500 * xMod * dt
		self.yVel -= 500 * dt
		
		if self.sprite != None:
			if 'hurt left' in self.sprite.frame or 'hurt right' in self.sprite.frame:
				self.sprite.level = 'hurt'
	
		self.hp -= 5
		if self.hp <= 0:
			return 'dead'
		
class Part:

	def __init__(self,id,idNum,cellList):
	
		self.type = 'part'
		self.id = id
		self.idNum = idNum
		self.cellList = cellList
