import pygame, glob
from pygame import *

class LoadAnimated:

	def __init__(self,id):
	
		self.loaded = False
		self.type = 'animated'
		self.id = id.lower()
		self.currentFrame = 0
		self.currentTime = 0
		self.frame = {}
		self.speed = 100
		self.level = 'stand'
	
		# Load Check #
		for characterPath in glob.glob("Resources/Images/Characters/*"):
			tempName = characterPath[28:].lower()
			if tempName == self.id:
				self.loaded = True
				break
				
		if self.loaded:
			
			xLoc = 0
			yLoc = 0
			for moveTypePath in glob.glob("Resources/Images/Characters/"+self.id+"/*/"):
				
				moveType = moveTypePath[29+len(self.id):-1].lower()
				self.frame[moveType] = []
				tempHeight = 0
				
				for imagePath in glob.glob(moveTypePath+"/*.png"):
					tempImage = pygame.image.load(imagePath)
					f = Frame(xLoc,yLoc,tempImage.get_width(),tempImage.get_height())
					self.frame[moveType].append(f)
					xLoc += tempImage.get_width()
					if tempImage.get_height() > tempHeight : tempHeight = tempImage.get_height()
					
				xLoc = 0
				yLoc += tempHeight
				
	def Display(self,window,loc,facingDir,spriteSheet):
	
		targetLevel = self.level + ' ' + facingDir
		
		if targetLevel in self.frame:
			f = self.frame[targetLevel][self.currentFrame]
			window.blit(spriteSheet,[loc[0]+f.xMod,loc[1]+f.yMod],[f.sheetX,f.sheetY,f.w,f.h])
			
	def Update(self,facingDir,dt):
	
		targetLevel = self.level + ' ' + facingDir
		if targetLevel in self.frame:
			
			frameList = self.frame[targetLevel]
			if self.currentFrame >= len(frameList):
				self.currentFrame = 0
				self.currentTime = 0
				
			targetFrame = frameList[self.currentFrame]
			if targetFrame.timeLength != None:
				self.currentTime += dt * self.speed
				if self.currentTime >= targetFrame.timeLength:
					self.currentTime = 0
					self.currentFrame += 1
					if self.currentFrame >= len(frameList):
						self.currentFrame = 0
		
class LoadStill:

	def __init__(self,id):
	
		self.loaded = False
		self.type = 'still'
		self.id = None
		self.sheetX = None
		self.sheetY = None
		self.w = None
		self.h = None
		self.xMod = 0
		self.yMod = 0
		
		# Load Check #
		for imagePath in glob.glob("Resources/Images/Objects/*.png"):
			tempId = imagePath[25:-4].lower()
			if tempId == id:
				self.loaded = True
				self.id = id
				break
				
		if self.loaded:
			
			xLoc = 0
			yLoc = 0
			for imagePath in glob.glob("Resources/Images/Objects/*.png"):
				tempImage = pygame.image.load(imagePath)
				tempId = imagePath[25:-4].lower()
				
				if tempId == id:
					self.sheetX = xLoc
					self.sheetY = yLoc
					self.w = tempImage.get_width()
					self.h = tempImage.get_height()
					break
					
				xLoc += tempImage.get_width()
				
	def Display(self,window,loc,spriteSheet):
	
		window.blit(spriteSheet,[loc[0]+self.xMod,loc[1]+self.yMod],[self.sheetX,self.sheetY,self.w,self.h])
	
class Frame:

	def __init__(self,sheetX,sheetY,w,h):
	
		self.sheetX = sheetX
		self.sheetY = sheetY
		self.w = w
		self.h = h
		self.xMod = 0
		self.yMod = 0
		
		self.timeLength = 5
		
def LoadSheet(type,path):

	# Get Sheet Size #
	totalWidth = 0
	totalHeight = 0
	
	if type == 'character':
		for moveTypePath in glob.glob(path+"/*/"):
			tempWidth = 0
			tempHeight = 0
			for imagePath in glob.glob(moveTypePath+"/*.png"):
				tempImage = pygame.image.load(imagePath)
				tempWidth += tempImage.get_width()
				if tempImage.get_height() > tempHeight : tempHeight = tempImage.get_height()
			if tempWidth > totalWidth : totalWidth = tempWidth
			totalHeight += tempHeight
	
	elif type == 'object':
		for imagePath in glob.glob(path+"/*.png"):
			tempImage = pygame.image.load(imagePath)
			totalWidth += tempImage.get_width()
			if tempImage.get_height() > totalHeight : totalHeight = tempImage.get_height()
			
	# Create Sheet #
	sheet = pygame.Surface((totalWidth,totalHeight),flags=pygame.SRCALPHA)
	x = 0
	y = 0
	
	if type == 'character':
		for moveTypePath in glob.glob(path+"/*/"):
			tempHeight = 0
			for imagePath in glob.glob(moveTypePath+"/*.png"):
				tempImage = pygame.image.load(imagePath).convert_alpha()
				sheet.blit(tempImage,(x,y))
				x += tempImage.get_width()
				if tempImage.get_height() > tempHeight : tempHeight = tempImage.get_height()
			
			x = 0
			y += tempHeight
			
	elif type == 'object':
		for imagePath in glob.glob(path+"/*.png"):
			tempImage = pygame.image.load(imagePath).convert_alpha()
			sheet.blit(tempImage,(x,y))
			x += tempImage.get_width()
		
	return sheet.convert_alpha()
		