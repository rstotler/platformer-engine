import pygame, os, copy, glob, math, random, PygTools, Object, Level, Sprite
from pygame import *

class Load:

	def __init__(self,id,window):
	
		self.cellSize = 128
		self.xMod = 0
		self.yMod = 0
		self.gravity = 80
		
		self.drawObjects = []
		
		# Load Players #
		self.player = {}
		self.player[1] = Object.Load('player','shinobi',{'player num':1})
		self.player[2] = Object.Load('player','alucard',{'player num':2})
		
		self.cell = Level.Load(id,self.cellSize,self.player)
		self.image = self.LoadImages()
		
		self.smallScreen = pygame.Surface((640,360))
		self.mapScreen = pygame.Surface((1280,720))
		self.bgColor = [0,0,0]
		self.bgColor[random.choice([0,1,2])] = random.randrange(20,100)
		self.toggleKeys = {'f1':True, 'f2':True, 'f3':False}
		
	def Display(self,window):
	
		self.mapScreen.fill(self.bgColor)
	
		playerList = []
		mobList = []
		
		displayFlags = []
		if self.toggleKeys['f2'] : displayFlags.append('collide box')
		
		for o in self.drawObjects:
			if o.type == 'player' : playerList.append(o)
			elif o.type == 'mob' : mobList.append(o)
			else : o.Display(self.mapScreen,(self.xMod,self.yMod),[],self.image['object sheet'])
				
		# Mobs #
		for m in mobList:
			spriteSheet = None
			if m.sprite.loaded : spriteSheet = self.image['character'][m.sprite.id]
			m.Display(self.mapScreen,(self.xMod,self.yMod),displayFlags,spriteSheet)
				
		# Player #
		for p in playerList:
			spriteSheet = None
			if p.sprite.loaded : spriteSheet = self.image['character'][p.sprite.id]
			p.Display(self.mapScreen,(self.xMod,self.yMod),displayFlags,spriteSheet)
		
		if self.toggleKeys['f3']:
			self.smallScreen.blit(self.mapScreen,[0,0],[320,180,640,360])
			self.mapScreen = pygame.transform.scale(self.smallScreen,(1280,720))
		
		window.blit(self.mapScreen,(0,0))
		
	def Update(self,window,dt,keyboard):
	
		self.drawObjects = []
		idList = []
		
		for pNum in self.player:
			if self.player[pNum] != None:
				p = self.player[pNum]
				p.ProcessInput(dt,pNum,keyboard)
				p.Update(self.gravity,dt)
				if not p.static : self.UpdateMovingObject(window,dt,p)
				self.UpdateObjectAttacks(dt,p)
				self.drawObjects.append(p)
				idList.append(p.idNum)
		
		for xNum in range(-1,(window.get_width()/self.cellSize)+2):
			for yNum in range(-1,(window.get_height()/self.cellSize)+2):
				x = xNum - (self.xMod/self.cellSize)
				y = yNum - (self.yMod/self.cellSize)
				
				if x > -1 and y > -1 and x < len(self.cell) and y < len(self.cell[0]):
				
					c = self.cell[x][y]
					
					if len(c.objects) > 0:
						for o in c.objects:
							
							if o.type != 'part':
								if o.idNum not in idList:
									o.Update(self.gravity,dt)
									if not o.static : self.UpdateMovingObject(window,dt,o)
									self.UpdateObjectAttacks(dt,o)
									self.drawObjects.append(o)
									idList.append(o.idNum)
									
							elif o.idNum not in idList:
								targetCell = self.cell[o.cellList[0][0]][o.cellList[0][1]]
								for o2 in targetCell.objects:
									if o2.type != 'part' and o2.idNum == o.idNum:
										o2.Update(self.gravity,dt)
										if not o2.static : self.UpdateMovingObject(window,dt,o2)
										self.UpdateObjectAttacks(dt,o2)
										self.drawObjects.append(o2)
										idList.append(o2.idNum)
							
		# Center Camera - Can Make More Efficient?
		targetPlayer = self.player[1]
		if targetPlayer == None : targetPlayer = self.player[2]
		if targetPlayer != None:
			self.CenterCamera(window,targetPlayer)
							
	def UpdateMovingObject(self,window,dt,o):
		
		# Falling #
		o.yVel += self.gravity * dt
		if o.yVel > 80 : o.yVel = 80
		
		# Collision Detection #
		itemDelList = []
		newXVel = int(o.xVel*o.speedMod)
		if o.xVel != 0 and newXVel == 0:
			if o.xVel < 0 : newXVel = -1
			else : newXVel = 1
		oVel = [newXVel,int(o.yVel)]
		moveRange = int(abs(oVel[0]))
		if int(abs(o.yVel)) > moveRange : moveRange = int(abs(o.yVel))
		oSize = o.rect.width
		if o.rect.height < oSize : oSize = o.rect.height
		
		for moveIncrement in range(1+(moveRange/oSize)):
						
			originalY = o.rect.top
						
			# Left/Right #
			if oVel[0] != 0:
			
				velStep = oVel[0]
				if velStep > oSize : velStep = oSize
				elif velStep < -oSize : velStep = -oSize
				
				o.rect.left += velStep
				oVel[0] -= velStep
				collideList = self.CollideCheckList(o)
				for collideObject in collideList:
				
					if o.type == 'player' and 'item' in collideObject.flags and collideObject.flags['item']:
						# Add Collect Item here and for Up/Down Movement
						itemDelList.append(collideObject)
					
					elif collideObject.collideShape == 'ramp':
						
						if collideObject.flags['ramp direction'] == 'left':
							
							# Moving Right #
							if velStep > 0 and o.rect.left+o.rect.width >= collideObject.rect.left:
								
								ignoreCheck = False
								#for newCollideObject in collideList:
								#	if newCollideObject.idNum != collideObject.idNum:
								#		if 'ignore ramps' in newCollideObject.flags and newCollideObject.flags['ignore ramps'] == True:
								#			ignoreCheck = True ; break
											
								if ignoreCheck == False:
								
									stepSizeMod = 0
									if o.grounded : stepSizeMod = o.stepSize
									
									newY = collideObject.rect.bottom - int((((collideObject.rect.left+collideObject.rect.width) - (o.rect.left+(o.rect.width/2))) / (collideObject.rect.width+0.)) * collideObject.rect.height)
									if newY < collideObject.rect.top : newY = collideObject.rect.top
									elif newY > collideObject.rect.bottom : newY = collideObject.rect.bottom
									
									# Go Down Ramp #
									if o.rect.bottom - stepSizeMod <= newY or o.rect.left > collideObject.rect.left:
										if o.grounded and o.rect.bottom < newY:
											o.rect.bottom = newY
											
											#if o.rect.bottom > collideObject.rect.top:
											#	if o.speedMod < 1 : o.speedMod = 1
											#	o.speedMod += dt * (.75 * (collideObject.angle / 90.0))
											#	if o.speedMod > 3 : o.speedMod = 3
											
									# Hit Wall #
									elif o.rect.bottom - stepSizeMod > collideObject.rect.top:
										o.rect.left = collideObject.rect.left - o.rect.width - 1
										o.rect.top = originalY
										oVel[0] = 0
										o.xVel = 0
										
									# Step Up #
									else:
										oldX = o.rect.left
										oldY = o.rect.bottom
										o.rect.bottom = collideObject.rect.top
										newCollideList = self.CollideCheckList(o)
										
										if len(newCollideList) > len(collideList):
											o.rect.left = oldX
											o.rect.bottom = oldY
											oVel[0] = 0
											o.xVel = 0
										
							# Moving Left #
							elif velStep < 0:
							
								stepSizeMod = 0
								if o.grounded : stepSizeMod = o.stepSize
								
								# Hit Wall #
								if o.rect.left <= collideObject.rect.left+collideObject.rect.width and collideObject.rect.bottom < o.rect.bottom - stepSizeMod:
									o.rect.left = collideObject.rect.left + collideObject.rect.width + 1
									oVel[0] = 0
									o.xVel = 0
								
								# Go Up Ramp #
								elif o.rect.left+(o.rect.width/2) < collideObject.rect.left+collideObject.rect.width:
									newY = collideObject.rect.bottom - int((((collideObject.rect.left+collideObject.rect.width) - (o.rect.left+(o.rect.width/2))) / (collideObject.rect.width+0.)) * collideObject.rect.height)
									if newY < collideObject.rect.top : newY = collideObject.rect.top
									if o.rect.bottom > newY:
										oldY = o.rect.top
										o.rect.bottom = newY
										
										#if o.rect.bottom > collideObject.rect.top:
										#	o.speedMod -= dt * (18 * (collideObject.angle / 90.0))
										#	if o.speedMod < 1-(collideObject.angle / 90.0) : o.speedMod = 1-(collideObject.angle / 90.0)
											
										# Rect Check #
										for newCollideObject in self.CollideCheckList(o):
											if newCollideObject.idNum != collideObject.idNum:
												if newCollideObject.collideShape in ['rect'] and 'ignore on ramps' not in newCollideObject.flags:
													o.xVel = 0
													while o.rect.top < newCollideObject.rect.bottom:
														o.rect.left += 1
														newNewY = collideObject.rect.bottom - int((((collideObject.rect.left+collideObject.rect.width) - (o.rect.left+(o.rect.width/2))) / (collideObject.rect.width+0.)) * collideObject.rect.height)
														if newNewY < collideObject.rect.top : newNewY = collideObject.rect.top
														o.rect.bottom = newNewY
														if o.rect.left > collideObject.rect.right : break
													
						elif collideObject.flags['ramp direction'] == 'right':
						
							# Moving Left #
							if velStep < 0:
								
								ignoreCheck = False
								#for newCollideObject in collideList:
								#	if newCollideObject.idNum != collideObject.idNum:
								#		if 'ignore ramps' in newCollideObject.flags and newCollideObject.flags['ignore ramps'] == True:
								#			ignoreCheck = True ; break
											
								if ignoreCheck == False:
										
									stepSizeMod = 0
									if o.grounded : stepSizeMod = o.stepSize
									
									newY = collideObject.rect.bottom - int((((o.rect.left+(o.rect.width/2)) - collideObject.rect.left) / (collideObject.rect.width+0.)) * collideObject.rect.height)
									if newY < collideObject.rect.top : newY = collideObject.rect.top
									elif newY > collideObject.rect.bottom : newY = collideObject.rect.bottom									
								
									# Go Down Ramp #
									if o.rect.bottom - stepSizeMod <= newY or o.rect.right < collideObject.rect.right:
										if o.grounded and o.rect.bottom < newY:
											o.rect.bottom = newY
											
											#if o.rect.bottom > collideObject.rect.top:
											#	if o.speedMod < 1 : o.speedMod = 1
											#	o.speedMod += dt * (.75 * (collideObject.angle / 90.0))
											#	if o.speedMod > 3 : o.speedMod = 3
								
									# Hit Wall #
									elif o.rect.bottom - stepSizeMod > collideObject.rect.top:
										o.rect.left = collideObject.rect.right + 1
										oVel[0] = 0
										o.xVel = 0
										
									# Step Up #
									else:
										oldX = o.rect.left
										oldY = o.rect.bottom
										o.rect.bottom = collideObject.rect.top
										newCollideList = self.CollideCheckList(o)
										
										if len(newCollideList) > len(collideList):
											o.rect.left -= oldX
											o.rect.bottom = oldY
											oVel[0] = 0
											o.xVel = 0
										
							# Moving Right #
							elif velStep > 0:
							
								stepSizeMod = 0
								if o.grounded : stepSizeMod = o.stepSize
							
								 # Hit Wall #
								if o.rect.left+o.rect.width >= collideObject.rect.left and collideObject.rect.bottom < o.rect.bottom - stepSizeMod:
									o.rect.left = collideObject.rect.left - o.rect.width - 1
									oVel[0] = 0
									o.xVel = 0
									
								# Go Up Ramp #
								elif o.rect.left+(o.rect.width/2) > collideObject.rect.left:
									newY = collideObject.rect.bottom - int((((o.rect.left+(o.rect.width/2)) - collideObject.rect.left) / (collideObject.rect.width+0.)) * collideObject.rect.height)
									if newY < collideObject.rect.top : newY = collideObject.rect.top
									if o.rect.bottom > newY:
										oldY = o.rect.top
										o.rect.bottom = newY
										
										#if o.rect.bottom > collideObject.rect.top:
										#	o.speedMod -= dt * (18 * (collideObject.angle / 90.0))
										#	if o.speedMod < 1-(collideObject.angle / 90.0) : o.speedMod = 1-(collideObject.angle / 90.0)
										
										# Rect Check #
										for newCollideObject in self.CollideCheckList(o):
											if newCollideObject.idNum != collideObject.idNum:
												if newCollideObject.collideShape in ['rect'] and 'ignore on ramps' not in newCollideObject.flags:
													o.xVel = 0
													while o.rect.top < newCollideObject.rect.bottom:
														o.rect.left -= 1
														newNewY = collideObject.rect.bottom - int((((o.rect.left+(o.rect.width/2)) - collideObject.rect.left) / (collideObject.rect.width+0.)) * collideObject.rect.height)
														if newNewY < collideObject.rect.top : newNewY = collideObject.rect.top
														o.rect.bottom = newNewY
														if o.rect.left < collideObject.rect.right : break
												
					elif collideObject.collideShape == 'circle':
					
						stepSizeMod = 0
						if o.grounded : stepSizeMod = o.stepSize
						
						if collideObject.rect.top+(collideObject.rect.width/2) >= o.rect.bottom - stepSizeMod:
							for yNum in range(collideObject.rect.height/2):
								o.rect.top -= 1
								if len(self.CollideCheckList(o)) < len(collideList):
									break
									
						else:
							o.rect.left -= velStep
							o.xVel = 0
							oVel[0] = 0
							
					elif collideObject.collideShape == 'rect':
						
						ignoreCheck = False
						if 'moveable' not in collideObject.flags or collideObject.flags['moveable'] == False:
							if 'ignore on ramps' in collideObject.flags and collideObject.flags['ignore on ramps']:
								for newCollideObject in collideList:
									if newCollideObject.collideShape == 'ramp':
										if 'ignore rects' in newCollideObject.flags and newCollideObject.flags['ignore rects'] == True:
											ignoreCheck = True ; break
									
						if ignoreCheck == False:
						
							# Move #
							if 'moveable' in collideObject.flags and collideObject.flags['moveable']:
								if velStep > 0 : o.rect.left = collideObject.rect.left - o.rect.width
								elif velStep < 0 : o.rect.left = collideObject.rect.right 
								collideObject.xVel += (o.xVel * o.speedMod)
								oVel[0] = 0
								o.xVel = 0
							
							# Step Up #
							elif o.grounded and collideObject.rect.top >= o.rect.bottom - o.stepSize:
								oldX = o.rect.left
								oldY = o.rect.bottom
								o.rect.bottom = collideObject.rect.top
								newCollideList = self.CollideCheckList(o)
								
								collideCheck = False
								for newCollideObject in newCollideList:
									if newCollideObject.collideShape != 'ramp' : collideCheck = True
								
								if collideCheck:
									o.rect.left = oldX
									o.rect.bottom = oldY
									oVel[0] = 0
									o.xVel = 0
									
							else:
								if velStep > 0 : o.rect.left = collideObject.rect.left - o.rect.width
								elif velStep < 0 : o.rect.left = collideObject.rect.right
								oVel[0] = 0
								o.xVel = 0
								
			# Up/Down #
			if oVel[1] != 0:
				
				velStep = oVel[1]
				if velStep > oSize : velStep = oSize
				elif velStep < -oSize : velStep = -oSize
				
				o.rect.top += velStep
				oVel[1] -= velStep
				collideList = self.CollideCheckList(o)
				
				groundedCheck = False
				for collideObject in collideList:
					if collideObject.collideShape != 'ramp' : groundedCheck = True
				if len(collideList) == 0 or not groundedCheck:
					o.grounded = False
					if o.type in ['player','mob'] and o.jumpCount == 0 : o.jumpCount = 1
				
				for collideObject in collideList:
				
					if o.type == 'player' and 'item' in collideObject.flags and collideObject.flags['item']:
						# Add Collect Item here and for Left/Right Movement
						itemDelList.append(collideObject)
						
					elif collideObject.collideShape == 'ramp':
						
						# Up #
						if velStep < 0:
						
							if o.rect.bottom > collideObject.rect.bottom and o.rect.top <= collideObject.rect.bottom:
								o.rect.top = collideObject.rect.bottom + 1
								oVel[1] = 0
								o.yVel = 0
								o.jumpTime = o.maxJumpTime
								
						# Down #
						elif velStep > 0:
							
							if collideObject.flags['ramp direction'] == 'left':
								
								newY = collideObject.rect.bottom - int((((collideObject.rect.left+collideObject.rect.width) - (o.rect.left+(o.rect.width/2))) / (collideObject.rect.width+0.)) * collideObject.rect.height)
								if newY < collideObject.rect.top : newY = collideObject.rect.top
								elif newY > collideObject.rect.bottom : newY = collideObject.rect.bottom
								
								if o.rect.left <= collideObject.rect.right and o.rect.bottom > newY:
									o.rect.bottom = newY
									oVel[1] = 0
									o.LandOnGround()
									
							elif collideObject.flags['ramp direction'] == 'right':
								
								newY = collideObject.rect.bottom - int((((o.rect.left+(o.rect.width/2)) - collideObject.rect.left) / (collideObject.rect.width+0.)) * collideObject.rect.height)
								if newY < collideObject.rect.top : newY = collideObject.rect.top
								elif newY > collideObject.rect.bottom : newY = collideObject.rect.bottom
								
								if o.rect.left+o.rect.width >= collideObject.rect.left and o.rect.bottom > newY:
									o.rect.bottom = newY
									oVel[1] = 0
									o.LandOnGround()
									
					else:
						
						# Up #
						if velStep < 0:
							
							ignoreCheck = False
							for newCollideObject in collideList:
								if newCollideObject.collideShape == 'ramp':
									if 'ignore rects' in newCollideObject.flags and newCollideObject.flags['ignore rects'] == True:
										ignoreCheck = True
						
							if ignoreCheck == False:
								if collideObject.collideShape == 'circle':
									while len(self.CollideCheckList(o)) == len(collideList):
										o.rect.top += 1
									oVel[1] = 0
									o.yVel = 0
									o.jumpTime = o.maxJumpTime
								else:
									o.rect.top = collideObject.rect.bottom
									oVel[1] = 0
									o.yVel = 0
									o.jumpTime = o.maxJumpTime
								
						# Down #
						elif velStep > 0:
							
							ignoreCheck = False
							for newCollideObject in collideList:
								if newCollideObject.collideShape == 'ramp':
									if 'ignore rects' in newCollideObject.flags:
										if newCollideObject.flags['ignore rects'] == True:											
											if (newCollideObject.flags['ramp direction'] == 'right' and collideObject.rect.left > newCollideObject.rect.left) or (newCollideObject.flags['ramp direction'] == 'left' and collideObject.rect.right < newCollideObject.rect.right): 
												ignoreCheck = True ; break
						
							if ignoreCheck == False:
								if collideObject.collideShape == 'circle':
									while len(self.CollideCheckList(o)) == len(collideList):
										o.rect.top -= 1
								else:
									if o.rect.bottom > collideObject.rect.top:
										o.rect.bottom = collideObject.rect.top
										
								oVel[1] = 0
								o.LandOnGround()
								
								#if o.speedMod < 1 : o.speedMod = 1
								#elif o.speedMod > 1:
								#	o.speedMod -= dt * .1
								#	if o.speedMod < 1 : o.speedMod = 1
									
			if oVel[0] == 0 and oVel[1] == 0 : break
			
		# Friction #
		if o.xVel < 0:
			o.xVel += 3 * dt
			if o.xVel > 0 : o.xVel = 0
		elif o.xVel > 0:
			o.xVel -= 3 * dt
			if o.xVel < 0 : o.xVel = 0
			
		if o.type != 'player':
			self.UpdateObjectCells(o)
		
		for object in itemDelList:
			self.DeleteObject(object)

		if o.type == 'player':
			if o.rect.top > len(self.cell[0]) * self.cellSize : o.rect.top = 0
			
	def UpdateObjectAttacks(self,dt,o):
	
		attackDelList = []
		for aNum, a in enumerate(o.currentAttacks):
			returnData = a.Update(dt,o.attackList[a.id],o.rect,o.facingDir)
			if returnData == 'attack finish' : attackDelList.append(aNum)
			else:
				for collideObject in self.CollideCheckList(a):
					if collideObject.type in ['player','mob']:
						if collideObject.idNum not in a.hitObjectsList:
							
							# Assign Collide Data To Attack #
							a.hitObjectsList[collideObject.idNum] = collideObject
							if 'repeater' in a.flags and 'time' in a.flags['repeater'] and 'idNumTime' in a.flags['repeater']:
								a.flags['repeater']['idNumTime'][collideObject.idNum] = a.flags['repeater']['time']
							
							hitData = collideObject.GetHit(dt,o.facingDir,a)
							if hitData == 'dead' : self.DeleteObject(collideObject)
							
					if 'destroy on collide' in a.flags and a.flags['destroy on collide']:
						attackDelList.append(aNum) ; break
							
		attackDelList.reverse()
		for aNum in attackDelList:
			del o.currentAttacks[aNum]
			
	def CollideCheckList(self,o):
	
		list = []
		surroundingObjects = self.GetSurroundingObjects(o)
		
		for sObject in surroundingObjects:
			if 'background' in sObject.flags and sObject.flags['background'] : pass
			elif o.type == 'attack' and sObject.type not in ['player','mob'] and 'collide with walls' not in o.flags : pass
			else:
				
				if o.collideShape == 'rect':
					if sObject.collideShape == 'rect' and pygame.sprite.collide_rect(o,sObject) : list.append(sObject)
					elif sObject.collideShape == 'ramp' and PygTools.RectTriangleCollide(o,sObject) : list.append(sObject)
					elif sObject.collideShape == 'circle' and PygTools.RectCircleCollide(o,sObject) : list.append(sObject)
					
				# Ramps Don't Move/Collide Yet
				elif o.collideShape == 'ramp':
					pass
					
				elif o.collideShape == 'circle':
					if sObject.collideShape == 'rect' and PygTools.RectCircleCollide(sObject,o) : list.append(sObject)
					elif sObject.collideShape == 'ramp' and PygTools.RectTriangleCollide(o,sObject) : list.append(sObject) # Fix This!
					elif sObject.collideShape == 'circle' and PygTools.CircleCircleCollide([o.rect.left,o.rect.top],[sObject.rect.left,sObject.rect.top],o.rect.width/2,sObject.rect.width/2) : list.append(sObject)
				
		return list
		
	def GetSurroundingObjects(self,o):
	
		objectList = [] ; idList = []
	
		w = 1
		h = 1
		if o.rect.width > self.cellSize : w += (o.rect.width / self.cellSize)
		if o.rect.height > self.cellSize : h += (o.rect.height / self.cellSize)
		if (o.rect.width % self.cellSize) + (o.rect.left % self.cellSize) > self.cellSize : w += 1
		if (o.rect.height % self.cellSize) + (o.rect.top % self.cellSize) > self.cellSize : h += 1
		
		xLoc = (o.rect.left / self.cellSize) - 1
		yLoc = (o.rect.top / self.cellSize) - 1
		for xNum in range(w+2):
			for yNum in range(h+2):
				x = xLoc + xNum
				y = yLoc + yNum
								
				if x > -1 and y > -1 and x < len(self.cell) and y < len(self.cell[0]):
					
					c = self.cell[x][y]
					for targetObject in c.objects:
						if targetObject.type != 'part':
							if targetObject.idNum != o.idNum:
								if targetObject.idNum not in idList:
									objectList.append(targetObject)
									idList.append(targetObject.idNum)
							
						elif targetObject.type == 'part':
							targetCell = self.cell[targetObject.cellList[0][0]][targetObject.cellList[0][1]]
							for o2 in targetCell.objects:
								if o2.type != 'part' and o2.idNum == targetObject.idNum:
									targetObject = o2
									if targetObject.idNum != o.idNum:
										if targetObject.idNum not in idList:
											objectList.append(targetObject)
											idList.append(targetObject.idNum)
		
		# Temp Player Add #
		for pNum in self.player:
			if self.player[pNum] != None and o.idNum != self.player[pNum].idNum:
				objectList.append(self.player[pNum])
		
		return objectList
	
	def UpdateObjectCells(self,o):
	
		w = 1
		h = 1
		if o.rect.width > self.cellSize : w += (o.rect.width / self.cellSize)
		if o.rect.height > self.cellSize : h += (o.rect.height / self.cellSize)
		if (o.rect.width % self.cellSize) + (o.rect.left % self.cellSize) > self.cellSize : w += 1
		if (o.rect.height % self.cellSize) + (o.rect.top % self.cellSize) > self.cellSize : h += 1
		
		xLoc = o.rect.left / self.cellSize
		yLoc = o.rect.top / self.cellSize
		
		# Remove Object From Map #
		if xLoc < 0 or yLoc < 0 or xLoc >= len(self.cell) or yLoc >= len(self.cell[0]):
			self.DeleteObject(o)
		
		# Update Cells #
		else:
			oldCellList = copy.deepcopy(o.cellList)
			newCellList = []
			updateCheck = False
			for xNum in range(w):
				x = xLoc + xNum
				for yNum in range(h):
					y = yLoc + yNum
					if x < len(self.cell) and y < len(self.cell[0]):
						newCellList.append([x,y])
					
			# New Cell #
			o.cellList = newCellList
			targetObject = o
			for cNum, cellLoc in enumerate(newCellList):
				targetCell = self.cell[cellLoc[0]][cellLoc[1]]
				if cNum != 0 : targetObject = Object.Part(o.id,o.idNum,newCellList)
				
				targetObjectNum = None
				for oNum, cellObject in enumerate(targetCell.objects):
					if cellObject.id == o.id and cellObject.idNum == o.idNum:
						targetObjectNum = oNum ; break
				
				if targetObjectNum != None : targetCell.objects[targetObjectNum] = targetObject
				else : targetCell.objects.append(targetObject)
					
			# Delete Old Cells #
			for cellLoc in oldCellList:
				if cellLoc not in newCellList:
					targetCell = self.cell[cellLoc[0]][cellLoc[1]]
					targetObjectNum = None
					for oNum, cellObject in enumerate(targetCell.objects):
						if cellObject.id == o.id and cellObject.idNum == o.idNum:
							targetObjectNum = oNum ; break
					
					if targetObjectNum != None:
						del targetCell.objects[targetObjectNum]
		
	def DeleteObject(self,o):

		# Player #
		if o.type == 'player':
			self.player[o.flags['player num']] = None
	
		# Object #
		else:
			for loc in o.cellList:
				delCheck = None
				targetCell = self.cell[loc[0]][loc[1]]
				for oNum, tempObject in enumerate(targetCell.objects):
					if tempObject.id == o.id and tempObject.idNum == o.idNum:
						delCheck = oNum ; break
				if delCheck != None : del targetCell.objects[delCheck]

	def MiddleClick(self,mouse):
	
		mx = mouse.x - self.xMod - 50
		my = mouse.y - self.yMod - 50
		
		#Level.LoadObject('object','moveable square',[mx,my],self.cell,self.cellSize)
		#Level.LoadObject('object','small right 45',[mx,my],self.cell,self.cellSize)
		#Level.LoadObject('object','ramp medium right 45',[mx,my],self.cell,self.cellSize)
		#Level.LoadObject('object','ramp medium left 45',[mx+150,my],self.cell,self.cellSize)
		#Level.LoadObject('object','circle 1',[mx,my],self.cell,self.cellSize)
		#Level.LoadObject('object','square',[mx,my],self.cell,self.cellSize)
		Level.LoadObject('mob','samus',[mx,my],self.cell,self.cellSize)
		pass
		
	def PlayerDash(self,key):
	
		if key == K_LSHIFT:
			self.player[1].Dash()
			
		elif key == K_RSHIFT:
			self.player[2].Dash()
			
	def MoveCamera(self,window,loc):
	
		self.xMod += loc[0]
		self.yMod += loc[1]
		
		self.AdjustCamera(window)
			
	def CenterCamera(self,window,object):
	
		self.xMod = -object.rect.left + (window.get_width()/2) - (object.rect.width/2)
		self.yMod = -object.rect.top + (window.get_height()/2) - (object.rect.height/2)
		self.AdjustCamera(window)
		
	def AdjustCamera(self,window):
		
		if self.xMod > 0 : self.xMod = 0
		elif self.xMod < (-len(self.cell) * self.cellSize) + window.get_width() : self.xMod = (-len(self.cell) * self.cellSize) + window.get_width()
		if self.yMod > 0 : self.yMod = 0
		elif self.yMod < (-len(self.cell[0]) * self.cellSize) + window.get_height() : self.yMod = (-len(self.cell[0]) * self.cellSize) + window.get_height()
		
	def LoadImages(self):
	
		image = {}
		
		# Character Sprite Sheets #
		image['character'] = {}
		for characterPath in glob.glob("Resources/Images/Characters/*"):
			charId = characterPath[28:].lower()
			image['character'][charId] = Sprite.LoadSheet('character',characterPath)
			
		# Object Sprite Sheets #
		image['object sheet'] = Sprite.LoadSheet('object',"Resources/Images/Objects")
			
		return image
		