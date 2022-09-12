import pygame, PygTools, Map
from pygame import *

class Load:

	def __init__(self,window):
	
		self.levelList = ['wave','debug level','combat debug','random test']
		self.targetLevel = 'combat debug'
	
		self.mouse = PygTools.Mouse()
		self.keyboard = PygTools.Keyboard()
		self.map = Map.Load(self.targetLevel,window)
		
		self.debugFont = PygTools.Font("Resources/Fonts/PressStartK.ttf",10)
		
	def Update(self,window,clock,dt):
	
		self.Display(window,clock)
		
		self.GetInput(window)
		self.map.Update(window,dt,self.keyboard)
		
	def Display(self,window,clock):
	
		self.map.Display(window)
		
		if self.map.toggleKeys['f1']:
			PygTools.Write(str(clock.get_fps())[0:5],'5w',[0,0],self.debugFont,window)
			if self.map.player[1] != None : PygTools.Write(str(self.map.player[1].hp)+' '+str(self.map.player[1].xVel*self.map.player[1].speedMod),'10w',[0,10],self.debugFont,window)
			if self.map.player[2] != None : PygTools.Write(str(self.map.player[2].hp)+' '+str(self.map.player[2].xVel*self.map.player[2].speedMod),'10w',[0,20],self.debugFont,window)
			PygTools.Write(self.targetLevel,'50w',[0,30],self.debugFont,window)
		
	def GetInput(self,window):
	
		self.mouse.Update()
		self.keyboard.Update()
		for event in pygame.event.get():
			
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 2 : self.map.MiddleClick(self.mouse)
				elif event.button == 3 : self.mouse.rightClick = True
				elif event.button in [4,5]:
					if event.button == 4:
						if self.levelList.index(self.targetLevel) == 0 : self.targetLevel = self.levelList[-1]
						else : self.targetLevel = self.levelList[self.levelList.index(self.targetLevel)-1]
					elif event.button == 5:
						if self.levelList.index(self.targetLevel) == len(self.levelList)-1 : self.targetLevel = self.levelList[0]
						else : self.targetLevel = self.levelList[self.levelList.index(self.targetLevel)+1]
					self.map = Map.Load(self.targetLevel,window)
				
			elif event.type == MOUSEBUTTONUP:
				if event.button == 3 : self.mouse.rightClick = False
				
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE : raise SystemExit
				elif event.key == K_RETURN : self.map = Map.Load(self.targetLevel,window)
				elif event.key in [K_LSHIFT,K_RSHIFT] and self.map.player[1] != None : self.map.PlayerDash(event.key) # Temp Controls #
				elif event.key in [K_F1,K_F2,K_F3]:
					if self.map.toggleKeys[pygame.key.name(event.key)] : self.map.toggleKeys[pygame.key.name(event.key)] = False
					else : self.map.toggleKeys[pygame.key.name(event.key)] = True
				
			elif event.type == QUIT : raise SystemExit
		
		if input == None and (self.mouse.x != self.mouse.oldX or self.mouse.y != self.mouse.oldY):
			if self.mouse.rightClick:
				self.map.MoveCamera(window,[self.mouse.x-self.mouse.oldX,self.mouse.y-self.mouse.oldY])
		
		key = pygame.key.get_pressed()
		if key[pygame.K_w] != self.keyboard.key['w'] : self.keyboard.events['w'] = key[pygame.K_w]
		if key[pygame.K_a] != self.keyboard.key['a'] : self.keyboard.events['a'] = key[pygame.K_a]
		if key[pygame.K_d] != self.keyboard.key['d'] : self.keyboard.events['d'] = key[pygame.K_d]
		if key[pygame.K_UP] != self.keyboard.key['up'] : self.keyboard.events['up'] = key[pygame.K_UP]
		if key[pygame.K_LEFT] != self.keyboard.key['left'] : self.keyboard.events['left'] = key[pygame.K_LEFT]
		if key[pygame.K_RIGHT] != self.keyboard.key['right'] : self.keyboard.events['right'] = key[pygame.K_RIGHT]
		
		if key[pygame.K_z] != self.keyboard.key['z']:
			self.keyboard.events['z'] = key[pygame.K_z]
			if self.map.player[1] != None : self.map.player[1].AttackButton(1,self.keyboard.events['z'])
		if key[pygame.K_x] != self.keyboard.key['x']:
			self.keyboard.events['x'] = key[pygame.K_x]
			if self.map.player[1] != None : self.map.player[1].AttackButton(2,self.keyboard.events['x'])
		if key[pygame.K_c] != self.keyboard.key['c']:
			self.keyboard.events['c'] = key[pygame.K_c]
			if self.map.player[1] != None : self.map.player[1].AttackButton(3,self.keyboard.events['c'])
		if key[pygame.K_COMMA] != self.keyboard.key[',']:
			self.keyboard.events[','] = key[pygame.K_COMMA]
			if self.map.player[2] != None : self.map.player[2].AttackButton(1,self.keyboard.events[','])
		if key[pygame.K_PERIOD] != self.keyboard.key['.']:
			self.keyboard.events['.'] = key[pygame.K_PERIOD]
			if self.map.player[2] != None : self.map.player[2].AttackButton(2,self.keyboard.events['.'])
		if key[pygame.K_SLASH] != self.keyboard.key['/']:
			self.keyboard.events['/'] = key[pygame.K_SLASH]
			if self.map.player[2] != None : self.map.player[2].AttackButton(3,self.keyboard.events['/'])
		