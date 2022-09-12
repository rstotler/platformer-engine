import pygame, glob, cPickle, Sprite, PygTools
from pygame import *

SCREENSIZE = [400,400]

class Screen:

	def __init__(self):
	
		self.xMod = 100
		self.yMod = 100
		
		self.mouse = PygTools.Mouse()
		self.keyboard = PygTools.Keyboard()
		self.pauseSpeed = None
		
		self.displayMessage = ''
		self.displayMessageTimer = 0
		
		self.sheet = {}
		for characterPath in glob.glob("Resources/Images/Characters/*"):
			charId = characterPath[28:].lower()
			self.sheet[charId] = Sprite.LoadSheet('character',characterPath)
	
		self.c = Character('samus')
		self.LoadData()
		
		self.displayLines = True
		self.smallFont = pygame.font.Font("Resources/Fonts/PressStartK.ttf",10)
		self.medFont = pygame.font.Font("Resources/Fonts/PressStartK.ttf",12)
		
		
		#### TEST LIST #######
		#self.l = PygTools.ButtonList('test list',[32,32])#################
		#testB1 = PygTools.Button('test list button 1','rect',[100,100],[50,50],{'default color':[150,150,255], 'hover color':[50,50,150], 'label':{'string':'test 1', 'color':[255,255,255]}},window)#############
		#testB2 = PygTools.Button('test list button 2','rect',[100,100],[50,50],{'default color':[150,150,255], 'hover color':[50,50,150], 'label':{'string':'test 2', 'color':[255,255,255]}},window)#############
		#self.l.AddButton(testB1)
		#self.l.AddButton(testB2)
		
	def Update(self,window,clock,dt):

		if self.displayMessage != '':
			self.displayMessageTimer -= 1
			if self.displayMessageTimer <= 0:
				self.displayMessageTimer = 0
				self.displayMessage = ''
	
		self.ProcessInput()
		self.c.sprite.Update(self.c.facingDir,dt)
		self.Display(window,clock)
		
		#### SOME TESTS #########
		#self.l.Update()###############

	def ProcessInput(self):

		self.mouse.Update()
		#self.mouse.Update([{'buttonList':self.l.buttons}])
		
		for event in pygame.event.get():
			
			if event.type == QUIT : raise SystemExit
			
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE : raise SystemExit
				elif event.key in [K_LEFT,K_RIGHT]:
					if self.keyboard.shift and not self.keyboard.control : self.ChangeLevel(event.key)
					elif self.keyboard.control and not self.keyboard.shift : self.ModFrame(event.key)
					else : self.ChangeFrame(event.key)
				elif event.key in [K_UP,K_DOWN]:
					if self.keyboard.control : self.ModFrame(event.key)
					else : self.ChangeCharacter(event.key)
				elif event.key in [K_LSHIFT,K_RSHIFT] and not self.keyboard.shift : self.keyboard.shift = True
				elif event.key in [K_LCTRL,K_RCTRL] and not self.keyboard.control : self.keyboard.control = True
				elif event.key == K_SPACE : self.Pause()
				elif event.key == K_F1:
					if self.displayLines : self.displayLines = False
					else : self.displayLines = True
				elif pygame.key.name(event.key) == 's' and self.keyboard.control : self.SaveData()
				elif pygame.key.name(event.key) == 'l' and self.keyboard.control : self.LoadData()
				
			elif event.type == KEYUP:
				if event.key in [K_LSHIFT,K_RSHIFT] and self.keyboard.shift : self.keyboard.shift = False
				elif event.key in [K_LCTRL,K_RCTRL] and self.keyboard.control : self.keyboard.control = False
				
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and not self.mouse.leftClick : self.mouse.leftClick = True ; self.LeftClick()
				elif event.button in [4,5] : self.ChangeSpeed(event.button)
				
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1 and self.mouse.leftClick : self.mouse.leftClick = False
				
		if self.mouse.x != self.mouse.oldX or self.mouse.y != self.mouse.oldY:
			if self.mouse.leftClick:
				self.MoveScreen()
			
	def LeftClick(self):
	
		#print self.mouse.hoverTarget
		pass
			
	def Display(self,window,clock):

		f = self.c.sprite.frame[self.c.sprite.level+' '+self.c.facingDir][self.c.sprite.currentFrame]
		window.fill((0,0,0))
		
		if self.displayLines:
			pygame.draw.line(window,[255,0,0],[self.xMod,0],[self.xMod,SCREENSIZE[1]])
			pygame.draw.line(window,[255,0,0],[0,self.yMod],[SCREENSIZE[0],self.yMod])
		
		if self.displayLines:
			PygTools.Outline(window,[0,255,0],[self.xMod+f.xMod,self.yMod+f.yMod],[self.c.sprite.frame[self.c.sprite.level+' '+self.c.facingDir][self.c.sprite.currentFrame].w-1,self.c.sprite.frame[self.c.sprite.level+' '+self.c.facingDir][self.c.sprite.currentFrame].h-1])
		self.c.sprite.Display(window,[self.xMod,self.yMod],self.c.facingDir,self.sheet[self.c.id])

		debugLine1 = self.smallFont.render(self.c.sprite.level+' '+self.c.facingDir,False,(255,255,255)) ; window.blit(debugLine1,(SCREENSIZE[0]-len(self.c.sprite.level+' '+self.c.facingDir)*10,0))
		debugLine2 = self.smallFont.render('Speed: '+str(self.c.sprite.speed),False,(255,255,255)) ; window.blit(debugLine2,(SCREENSIZE[0]-70-(len(str(self.c.sprite.speed))*10),10))
		debugLine3 = self.smallFont.render('Frame: '+str(self.c.sprite.currentFrame),False,(255,255,255)) ; window.blit(debugLine3,(SCREENSIZE[0]-70-(len(str(self.c.sprite.currentFrame)))*10,20))
		debugLine4 = self.smallFont.render('X='+str(f.xMod)+' Y='+str(f.yMod),False,(255,255,255)) ; window.blit(debugLine4,(SCREENSIZE[0]-50-(len(str(f.xMod)+str(f.yMod)))*10,30))
		
		if self.displayMessage != '':
			m = self.medFont.render(self.displayMessage,False,(255,255,255))
			window.blit(m,[0,SCREENSIZE[1]-12])
		
		####### MORE TESTSINGS ####
		#self.l.Display(window,self.mouse)#################
		
	def Pause(self):
	
		if self.c.sprite.speed != 0:
			self.pauseSpeed = self.c.sprite.speed
			self.c.sprite.speed = 0
			
		else:
			if self.pauseSpeed != None : self.c.sprite.speed = self.pauseSpeed ; self.pauseSpeed = None
			else : self.c.sprite.speed = 50
		
	def ChangeLevel(self,key):

		levelList = []
		newLevel = None
		for l in self.c.sprite.frame : levelList.append(l)
		currentLevel = self.c.sprite.level + ' ' + self.c.facingDir
		
		if key == K_LEFT:
			if levelList.index(currentLevel) > 0 : newLevel = levelList[levelList.index(currentLevel)-1]
			else : newLevel = levelList[-1]
		
		elif key == K_RIGHT:
			if levelList.index(currentLevel) == len(levelList)-1 : newLevel = levelList[0]
			else : newLevel = levelList[levelList.index(currentLevel)+1]
			
		if newLevel != None:
			self.c.sprite.level = ' '.join(newLevel.split()[:-1])
			self.c.facingDir = newLevel.split()[-1]
			
	def ChangeFrame(self,key):
	
		currentLevel = self.c.sprite.level + ' ' + self.c.facingDir
		frameList = self.c.sprite.frame[currentLevel]
		
		if key == K_LEFT:
			if self.c.sprite.currentFrame == 0 : self.c.sprite.currentFrame = len(frameList)-1
			else : self.c.sprite.currentFrame -= 1
			
		elif key == K_RIGHT:
			if self.c.sprite.currentFrame == len(frameList)-1 : self.c.sprite.currentFrame = 0
			else : self.c.sprite.currentFrame += 1
			
	def ModFrame(self,key):
	
		f = self.c.sprite.frame[self.c.sprite.level+' '+self.c.facingDir][self.c.sprite.currentFrame]
		newXMod = 0
		newYMod = 0
	
		if key == K_UP : newYMod = -1
		elif key == K_DOWN : newYMod = 1
		elif key == K_LEFT : newXMod = -1
		elif key == K_RIGHT : newXMod = 1
		
		if newXMod != 0 : f.xMod += newXMod
		if newYMod != 0 : f.yMod += newYMod
			
	def ChangeCharacter(self,key):
	
		charList = []
		newChar = None
		for characterPath in glob.glob("Resources/Images/Characters/*"):
			charId = characterPath[28:].lower()
			charList.append(charId)
	
		if key == K_UP:
			if charList.index(self.c.id) > 0 : newChar = charList[charList.index(self.c.id)-1]
			else : newChar = charList[-1]
			
		elif key == K_DOWN:
			if charList.index(self.c.id) < len(charList)-1 : newChar = charList[charList.index(self.c.id)+1]
			else : newChar = charList[0]
			
		if newChar != None:
			oldSpeed = self.c.sprite.speed
			self.c = Character(newChar)
			if oldSpeed == 0 : self.c.sprite.speed = 0
			
	def MoveScreen(self):
	
		self.xMod += self.mouse.x - self.mouse.oldX
		self.yMod += self.mouse.y - self.mouse.oldY
			
	def ChangeSpeed(self,key):
	
		# Up #
		if key == 4:
			if self.c.sprite.speed < 200:
				self.c.sprite.speed += 2
			
		# Down #
		elif key == 5:
			if self.c.sprite.speed > 0:
				self.c.sprite.speed -= 2
			
	def SaveData(self):
	
		spriteData = self.c.sprite
		cPickle.dump(spriteData,open('Resources/Sprite Data/' + self.c.id + '.txt','w'))
		self.displayMessage = 'Saved sprite data - ' + self.c.id + '.txt'
		self.displayMessageTimer = 300
		
	def LoadData(self):
	
		dataList = {}
		for characterPath in glob.glob("Resources/Sprite Data/*.txt"):
			charId = characterPath[22:-4].lower()
			dataList[charId] = characterPath
			
		if self.c.id not in dataList:
			self.displayMessage = "Can't find sprite file - " + self.c.id
			self.displayMessageTimer = 300
			
		else:
			dataFile = open(dataList[self.c.id],'r')
			spriteData = cPickle.load(dataFile)
			dataFile.close()
			
			self.c.sprite = spriteData
			#self.c.sprite.level = 'stand'
			#self.c.facingDir = 'right'
			
			self.displayMessage = "Loaded sprite file - " + self.c.id
			self.displayMessageTimer = 300
			
class Character:

	def __init__(self,id):
	
		self.id = id
		self.sprite = Sprite.LoadAnimated(id)
		self.facingDir = 'right'
		
		self.sprite.speed = 50
		
pygame.init()
window = pygame.display.set_mode(SCREENSIZE,0,32)
pygame.display.set_caption("Sprite Rigger 0.11")
clock = pygame.time.Clock()
screen = Screen()

while True:

	dt = clock.tick(60)
	screen.Update(window,clock,dt/1000.)
	pygame.display.flip()
	