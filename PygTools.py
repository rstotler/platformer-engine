import pygame, math, glob, copy
from pygame import *

class FPS:

	def __init__(self,fontPath):
	
		self.font = Font(fontPath,10)
		
	def Display(self,window,clock,loc):
	
		fpsString = str(clock.get_fps())
		fpsCode = str(len(fpsString)) + 'w'
		Write(fpsString[0:5],fpsCode,loc,self.font,window)

class Font:

	def __init__(self,path,size,offset=0):
	
		self.size = size
		self.font = pygame.font.Font(path,size)
		self.offset = offset
		
class Mouse:

	def __init__(self):
	
		self.x = 0 ; self.oldX = 0
		self.y = 0 ; self.oldY = 0
		
		self.leftClick = False
		self.rightClick = False
		
		self.hoverObjects = {}
		
	def Update(self,objectList=[]):
	
		self.oldX = self.x
		self.oldY = self.y
		self.x, self.y = pygame.mouse.get_pos()
		
		self.SetHoverTarget(objectList)
		
	def SetHoverTarget(self,objectList):
	
		self.hoverObjects = {}
		
		for objectGroup in objectList:
			for o in objectGroup['buttonList']:
				x = o.rect.left
				y = o.rect.top
				if 'displayOffset' in objectGroup:
					x += objectGroup['displayOffset'][0]
					y += objectGroup['displayOffset'][1]
			
				if o.collideShape == 'rect':
					if self.HoverCheck(x,y,o.rect.width,o.rect.height):
						self.hoverObjects[o.id] = o
						
				elif o.collideShape == 'circle':
					if CircleCircleCollide([x+(o.rect.width/2),y+(o.rect.width/2)],[self.x,self.y],o.rect.width/2,0):
						self.hoverObjects[o.id] = o
		
	def HoverCheck(self,x,y,w,h):

		if self.x in range(x,x+w):
			if self.y in range(y,y+h):
				return True

		return False
		
class Keyboard:
	
	def __init__(self):
		
		self.shift = False
		self.lShift = False
		self.rShift = False
		self.control = False
		self.lControl = False
		self.rControl = False
		self.backspace = False
		self.backTick = 3
		self.events = {}
		
		self.key = {'w':False, 'a':False, 's':False, 'd':False,\
					'up':False, 'left':False, 'down':False, 'right':False,\
					'z':False, 'x':False, 'c':False,\
					',':False, '.':False, '/':False}
		
		self.letters = {'a':'a','b':'b','c':'c','d':'d','e':'e','f':'f','g':'g','h':'h','i':'i','j':'j',\
						'k':'k','l':'l','m':'m','n':'n','o':'o','p':'p','q':'q','r':'r','s':'s','t':'t',\
					    'u':'u','v':'v','w':'w','x':'x','y':'y','z':'z','0':'0','1':'1','2':'2','3':'3',\
					    '4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','-':'-','=':'=',']':']','[':'[',\
					    ';':';',"'":"'",'/':'/','.':'.',',':',','space':' '}
			
		self.shiftLetters = {'a':'A','b':'B','c':'C','d':'D','e':'E','f':'F','g':'G','h':'H','i':'I','j':'J',\
						     'k':'K','l':'L','m':'M','n':'N','o':'O','p':'P','q':'Q','r':'R','s':'S','t':'T',\
						     'u':'U','v':'V','w':'W','x':'X','y':'Y','z':'Z','0':')','1':'!','2':'@','3':'#',\
						     '4':'$','5':'%','6':'^','7':'&','8':'*','9':'(','-':'_','=':'+',']':'}','[':'{',\
						     ';':':',"'":'"','/':'?','.':'>',',':'<','space':' '}
			
	def Update(self):
	
		if self.events != {}:
			self.events = {}
			
	def BackspaceCheck(self):
		
		self.backTick += 1
		if self.backTick == 4 : self.backTick = 0
		
		if self.backTick == 0 : return True
		return False

class ButtonList:

	def __init__(self,id,loc):
	
		self.id = id
		self.type = 'button list'
		self.loc = loc
		
		self.buttons = []
		
		self.listFont = pygame.font.Font("Resources/Fonts/PressStartK.ttf",10)
		
	def Update(self):
	
		pass
		
	def Display(self,window,mouse):
	
		for b in self.buttons:
			b.Display(window,mouse,{'font':self.listFont})
		
	def AddButton(self,b):
	
		b.rect.left = self.loc[0]
		newY = self.loc[1]
		for tempB in self.buttons : newY += tempB.rect.height
		b.rect.top = newY
		
		self.buttons.append(b)
		
class Button:

	def __init__(self,id,collideShape,loc,size,flags,window):
	
		self.id = id
		self.type = 'button'
		self.collideShape = collideShape
		
		if size[0] == 'label':
			size[0] = 10
			if 'label' in flags and 'string' in flags['label'] and 'color' in flags['label'] and 'font path' in flags and 'font size' in flags:
				size[0] = flags['font size'] * len(flags['label']['string'])
		if size[1] == 'label':
			size[1] = 10
			if 'label' in flags and 'string' in flags['label'] and 'color' in flags['label'] and 'font path' in flags and 'font size' in flags:
				size[1] = flags['font size']
		
		if collideShape == 'circle' : size = [size,size]
		self.rect = pygame.rect.Rect(loc,size)
		self.flags = flags
		self.image = {}
		self.label = None
		self.font = None
		self.selected = False
		
		# Images #
		if not ('color' in flags and flags['color'] == None):
			c = [255,0,150]
			if 'default color' in flags : c = flags['default color']
			self.image['default'] = pygame.Surface(size) ; self.image['default'].fill(c)
		if 'hover color' in flags : self.image['hover'] = pygame.Surface(size) ; self.image['hover'].fill(flags['hover color'])
		if 'selected color' in flags : self.image['selected color'] = pygame.Surface(size) ; self.image['selected color'].fill(flags['selected color'])
		
		# Label #
		if 'label' in flags and 'string' in flags['label'] and 'color' in flags['label'] : self.label = flags['label']
		if 'font path' in flags:
			fontSize = 10
			if 'font size' in flags : fontSize = flags['font size']
			self.font = pygame.font.Font(flags['font path'],fontSize)
			
	def Update(self):
	
		pass
		
	def Display(self,window,mouse,flags={}):
	
		i = None
		if 'default' in self.image : i = self.image['default']
		if self.selected and 'selected color' in self.image : i = self.image['selected color']
		if self in mouse.hoverObjects and 'hover' in self.image : i = self.image['hover']
		
		# Surface #
		if i != None or self.collideShape == 'circle':
			if self.collideShape == 'rect' : window.blit(i,(self.rect.left,self.rect.top))
			elif self.collideShape == 'circle':
				c = [255,0,150]
				if 'default color' in self.flags : c = self.flags['default color']
				if self.id in mouse.hoverObjects and 'hover color' in self.flags : c = self.flags['hover color']
				pygame.draw.circle(window,c,[self.rect.left+(self.rect.width/2),self.rect.top+(self.rect.width/2)],self.rect.width/2)
			
		# Label #
		if self.label != None:
			f = self.font
			if 'font' in flags : f = flags['font']
			if f != None:
				c = self.label['color']
				if 'label color' in flags : c = flags['label color']
				if self.label != None and 'hover color' in self.label and self in mouse.hoverObjects : c = self.label['hover color']
				l = f.render(self.label['string'],False,c)
				window.blit(l,(self.rect.left,self.rect.top))
		
	def Toggle(self):
	
		if self.selected : self.selected = False
		else : self.selected = True
		
class InputBar:

	def __init__(self,id,loc,length,h,fontPath,fontSize,flags):
		
		self.type = 'input bar'
		self.selected = False
		
		self.id = id
		self.x = loc[0]
		self.y = loc[1]
		self.length = length
		self.flags = flags
		self.color = [0,0,0]
		self.alpha = None
		self.outline = None
		self.hoverColor = None
		
		self.input = ''
		self.tempInput = ''
		self.blinkerNum = 0
		self.history = []
		self.displayPage = None
		
		fontOffset = 0
		self.xOffset = 0
		self.yOffset = 0
		if 'x offset' in flags : self.xOffset = flags['x offset']
		if 'y offset' in flags : self.yOffset = flags['y offset']
		if 'font offset' in flags : fontOffset = flags['font offset']
		self.font = Font(fontPath,fontSize,fontOffset)
		
		if 'color' in flags : self.color = flags['color']
		if 'alpha' in flags : self.alpha = flags['alpha']
		self.hoverImage = None
		if 'hover color' in flags : self.hoverColor = flags['hover color']
		if 'outline' in flags : self.outline = flags['outline']
	
		self.w = (self.xOffset*2) + (length*(fontSize+fontOffset))
		self.h = h + (self.yOffset*2)
		self.image = pygame.Surface((self.w,self.h)) ; self.image.fill(self.color)
		if self.alpha != None : self.image.set_alpha(self.alpha)
		if self.hoverColor != None : self.hoverImage = pygame.Surface((self.w,self.h)) ; self.hoverImage.fill(self.hoverColor)
	
	def Display(self,window,mouse):
		
		# Surface #
		i = self.image
		if self.hoverImage != None and self in mouse.hoverObjects : i = self.hoverImage
		window.blit(i,(self.x,self.y))
		if self.outline != None : Outline(window,self.outline,(self.x,self.y),(self.w,self.h))
		
		# Text #
		if len(self.input) <= self.length-1 : inputString = self.input
		else : inputString = self.input[len(self.input)-(self.length-1):]
		
		x = self.x + self.xOffset
		y = self.y + self.yOffset
		if 'center input x' in self.flags:
			inputLen = len(inputString) * (self.font.size - self.font.offset)
			x = (self.x + (self.image.get_width()/2)) - (inputLen/2)
		if 'center input y' in self.flags:
			y = (self.y + (self.h/2)) - (self.font.size/2)
	
		stringColor = 'dw'
		if 'string color' in self.flags : stringColor = self.flags['string color']
		Write(inputString,str(len(inputString))+stringColor,(x,y),self.font,window)
		
		if self.selected:
			self.blinkerNum += 1
			if self.blinkerNum < 60:
				blinkerX = (self.x + self.xOffset) + (len(inputString) * (self.font.size + self.font.offset))
				Write('_','1'+stringColor,(blinkerX,y),self.font,window)
			if self.blinkerNum >= 120 : self.blinkerNum = 0
		
	def Input(self):
	
		if len(self.history) == 0 or (len(self.history) > 0 and self.input != self.history[0]):
			self.history.insert(0,self.input)
			if len(self.history) > 50:
				del self.history[-1]
		self.displayPage = None
		self.input = ''
		
	def Scroll(self,dir):
	
		if dir == K_UP:
		
			if self.displayPage != None and len(self.history) > self.displayPage+1:
				self.displayPage += 1
				self.input = self.history[self.displayPage]
			
			elif self.displayPage == None and len(self.history) > 0:
				self.displayPage = 0
				self.tempInput = self.input
				self.input = self.history[self.displayPage]
			
		elif dir == K_DOWN:
			
			if self.displayPage != None and self.displayPage > 0:
				self.displayPage -= 1
				self.input = self.history[self.displayPage]
			
			elif self.displayPage == 0:
				self.displayPage = None
				self.input = self.tempInput
				self.tempInput = ''
				
			elif self.displayPage == None:
				self.input = ''
		
	def Reload(self,reloadFlags):
	
		if 'x' in reloadFlags : self.x = reloadFlags['x']
		if 'y' in reloadFlags : self.y = reloadFlags['y']
		if 'w' in reloadFlags : self.w = reloadFlags['w']
		if 'h' in reloadFlags : self.h = reloadFlags['h']
		if 'color' in reloadFlags : self.color = reloadFlags['color']
		if 'alpha' in reloadFlags : self.alpha = reloadFlags['alpha']
		
		self.image = pygame.Surface((self.w,self.h))
		self.image.fill((self.color))
		if self.alpha != None : self.image.set_alpha(self.alpha)
		
		self.length = self.w / self.font.size
		
class Console:
	
	def __init__(self,id,length,lines,loc,fontPath,fontSize,flags):
	
		self.id = id
		self.flags = flags
		self.lines = lines
		self.length = length
		
		fontOffset = 0
		if 'font offset' in flags : fontOffset = flags['font offset']
		self.font = Font(fontPath,fontSize,fontOffset)
		
		self.w = length * (fontSize + fontOffset)
		h = fontSize
		if lines == 1 : self.h = h
		else : self.h = (self.lines * h)
		if 'image border' in flags:
			self.w += flags['image border'][0]
			self.h += flags['image border'][1]
		self.x = loc[0]
		self.y = loc[1]
		
		self.buffer = []
		self.page = 1
		
		self.color = [0,0,0]
		self.alpha = None
		if 'color' in flags : self.color = flags['color']
		self.image = pygame.Surface((self.w,self.h))
		if 'alpha' in self.flags:
			self.alpha = self.flags['alpha']
			self.image.set_alpha(self.alpha)
		self.image.fill(self.color)
		
	def Display(self,window):
	
		image = self.image
		window.blit(image,(self.x,self.y))
		
		if len(self.buffer) > 0:
			
			# Create Display List #
			listCopy = copy.deepcopy(self.buffer) ; listCopy.reverse()
			list = [] ; lineNum = 0
			
			for line in listCopy:
				lineNum += 1
				if lineNum in range(1+((self.lines)*(self.page-1)), 1+((self.lines)*self.page)):
					list.append(line)
				if lineNum >= (self.lines) * self.page : break
	
			# Display List To Screen #
			xLevel = self.x
			yLevel = self.y + self.h - self.font.size
			if 'image border' in self.flags:
				xLevel -= self.flags['image border'][0]/2
				yLevel -= self.flags['image border'][1]/2
			for line in list:
				if line == "break" : pass
				else:
					if len(line['string']) > self.length : line['string'] = line['string'][:self.length-1]
					Write(line["string"],line["code"],(xLevel,yLevel),self.font,window)
				yLevel -= self.font.size
				if "y offset" in self.flags : yLevel -= self.flags["y buffer"]*2
				
		if "outline" in self.flags:
			Outline(window,self.flags["outline"],(self.x,self.y),(self.w,self.h))
	
	def Scroll(self,dir):
	
		if dir in ['up',4] : self.page += 1
		elif dir in ['down',5] and self.page > 1 : self.page -= 1
		
	def Append(self,lines):
	
		#self.buffer.append('break')
		#self.buffer.append('break')
		
		for line in lines:
			line['string'] = ' ' + line['string']
			line['code'] = '1w' + line['code']
			self.buffer.append(line)
			
		if self.page != 1:
			self.page = 1
		
	def Reload(self,reloadFlags):
	
		if 'x' in reloadFlags : self.x = reloadFlags['x']
		if 'y' in reloadFlags : self.y = reloadFlags['y']
		if 'w' in reloadFlags : self.w = reloadFlags['w']
		if 'h' in reloadFlags : self.h = reloadFlags['h']
		if 'color' in reloadFlags : self.color = reloadFlags['color']
		if 'alpha' in reloadFlags : self.alpha = reloadFlags['alpha']
		
		self.image = pygame.Surface((self.w,self.h))
		self.image.fill((self.color))
		if self.alpha != None : self.image.set_alpha(self.alpha)
		
		self.lines = (self.h / self.font.size)
	
def Write(string,code,loc,font,window):
	
	colorCode = [] ; tempCode1 = [] ; tempCode2 = [[]] ; codePos = 0
	
	# Compose Color Code Into List #
	for x in range(1,len(code) + 1):
		try : tempCode1.append(int(code[x-1:x]))
		except TypeError : pass
		except : tempCode1.append(code[x-1:x])
		else : pass
		
	# Compose Into Sorted List #
	for x in tempCode1:
		if isinstance(x,int) == True:
			if len(tempCode2[codePos]) == 0 : tempCode2[codePos].append(x)
			elif len(tempCode2[codePos]) > 0 : tempCode2[codePos][0] = int(str(tempCode2[codePos][0]) + str(x))
		elif isinstance(x,str) == True:
			if x in ['r','o','y','g','c','b','v','m','w','a','x','l','d']:
				if len(tempCode2[codePos]) == 1 : tempCode2[codePos].append(x)
				elif len(tempCode2[codePos]) > 1 : tempCode2[codePos][1] = tempCode2[codePos][1] + x
				if x in ['r','o','y','g','c','b','v','m','w','a','x']:
					tempCode2.append([]) ; codePos += 1
				
	# Format List #
	for x in tempCode2:
		try:
			if isinstance(x[0],int) == True and isinstance(x[1],str) == True : colorCode.append(x)
		except TypeError : pass
		except : pass
		else : pass

	# Print String #
	totalprinted = 0 ; printed = 0
	
	xLoc = loc[0]
	yLoc = loc[1]
	if loc[0] == 'center window' : xLoc = (window.get_width()/2) - ((len(string)*(font.size+font.offset))/2)
	if loc[1] == 'center window' : yLoc = (window.get_height()/2) - (font.size/2)
	
	while totalprinted < len(string):

		if printed == colorCode[0][0] : del colorCode[0] ; printed = 0
		
		if len(colorCode) > 0:
			color = GetColor(colorCode[0][1])
			letter = font.font.render(string[totalprinted:totalprinted+1],False,color)
			window.blit(letter,(xLoc,yLoc))
			totalprinted += 1 ; printed += 1
			xLoc += font.size + font.offset
			
		elif len(colorCode) == 0 : break
		
def GetColor(colorCode):

	if colorCode == 'lr'  : return (255,80,80)     # LIGHT RED
	elif colorCode == 'r'   : return (255,0,0)     # RED
	elif colorCode == 'dr'  : return (125,0,0)     # DARK RED
	elif colorCode == 'ddr' : return (80,0,0)      # DARKER RED
	elif colorCode == 'lo'  : return (255,150,75)  # LIGHT ORANGE
	elif colorCode == 'o'   : return (255,100,0)   # ORANGE
	elif colorCode == 'do'  : return (150,75,0)    # DARK ORANGE
	elif colorCode == 'ddo' : return (80,40,0)     # DARKER ORANGE
	elif colorCode == 'ly'  : return (255,255,80)  # LIGHT YELLOW
	elif colorCode == 'y'   : return (255,255,0)   # YELLOW
	elif colorCode == 'dy'  : return (125,125,0)   # DARK YELLOW
	elif colorCode == 'ddy' : return (80,80,0)     # DARKER YELLOW
	elif colorCode == 'lg'  : return (80,255,80)   # LIGHT GREEN
	elif colorCode == 'g'   : return (0,255,0)     # GREEN
	elif colorCode == 'dg'  : return (0,125,0)     # DARK GREEN
	elif colorCode == 'ddg' : return (0,80,0)      # DARKER GREEN
	elif colorCode == 'lc'  : return (80,255,255)  # LIGHT CYAN
	elif colorCode == 'c'   : return (0,255,255)   # CYAN
	elif colorCode == 'dc'  : return (0,125,125)   # DARK CYAN
	elif colorCode == 'ddc' : return (0,80,80)     # DARKER CYAN
	elif colorCode == 'lb'  : return (80,80,255)   # LIGHT BLUE
	elif colorCode == 'b'   : return (0,0,255)     # BLUE
	elif colorCode == 'db'  : return (0,0,125)     # DARK BLUE
	elif colorCode == 'ddb' : return (0,0,80)      # DARKER BLUE
	elif colorCode == 'lv'  : return (255,80,255)  # LIGHT VIOLET
	elif colorCode == 'v'   : return (255,0,255)   # VIOLET
	elif colorCode == 'dv'  : return (125,0,125)   # DARK VIOLET
	elif colorCode == 'ddv' : return (80,0,80)     # DARKER VIOLET
	elif colorCode == 'lm'  : return (175,80,255)  # LIGHT MAGENTA
	elif colorCode == 'm'   : return (175,0,255)   # MAGENTA
	elif colorCode == 'dm'  : return (75,0,125)    # DARK MAGENTA
	elif colorCode == 'ddm' : return (75,0,80)     # DARKER MAGENTA
	elif colorCode == 'lw'  : return (255,255,255) # WHITE
	elif colorCode == 'w'   : return (255,255,255) # WHITE
	elif colorCode == 'dw'  : return (200,200,200) # DARK WHITE
	elif colorCode == 'ddw' : return (150,150,150) # DARKER WHITE/LIGHT GREY
	elif colorCode == 'la'  : return (150,150,150) # LIGHT GREY
	elif colorCode == 'a'   : return (150,150,150) # GREY
	elif colorCode == 'da'  : return (100,100,100) # DARK GREY
	elif colorCode == 'dda' : return (70,70,70)    # DARKER GREY
	elif colorCode == 'x'   : return (0,0,0)       # BLACK
	
	else : return (255,255,255)

def Outline(window,color,loc,size):

	pygame.draw.line(window,color,loc,[loc[0]+size[0],loc[1]])
	pygame.draw.line(window,color,loc,[loc[0],loc[1]+size[1]])
	pygame.draw.line(window,color,[loc[0]+size[0],loc[1]],[loc[0]+size[0],loc[1]+size[1]])
	pygame.draw.line(window,color,[loc[0],loc[1]+size[1]],[loc[0]+size[0],loc[1]+size[1]])
	
def CircleCircleCollide(loc1,loc2,size1,size2):

	dx = loc1[0] - loc2[0]
	dy = loc1[1] - loc2[1]
	dr = math.sqrt((dx**2)+(dy**2))
	if dr <= size1 + size2 : return True
	
	return False
	
def SquareSquareCollide(loc1,loc2,size):

	if loc1[0] in range(loc2[0],loc2[0]+size[0]):
		if loc1[1] in range(loc2[1],loc2[1]+size[1]):
			return True

	return False
	
def RectCircleCollide(r,c):

	xx = r.rect.left + r.rect.width/2
	yy = r.rect.top + r.rect.height/2
	w  = r.rect.width/2
	h  = r.rect.height/2
	dx = abs(c.rect.left+(c.rect.width/2) - xx)
	dy = abs(c.rect.top+(c.rect.width/2) - yy)
	
	if dx > (c.rect.width/2+w) or dy > (c.rect.height/2+h) : return False
	
	circledistance = {'x':abs(c.rect.left+(c.rect.width/2)-r.rect.left-w), 'y':abs(c.rect.top+(c.rect.width/2)-r.rect.top-h)}
	
	if circledistance['x'] <= w : return True
	if circledistance['y'] <= h : return True
	
	cornerdistance = ((circledistance['x']-w)**2) + ((circledistance['y']-h)**2)
	
	return cornerdistance <= (c.rect.width/2)**2
	
def RectTriangleCollide(r,t):

	rx1 = r.rect.left
	ry1 = r.rect.top
	rx2 = r.rect.right
	ry2 = r.rect.bottom
	tx1 = t.points[0][0]
	ty1 = t.points[0][1]
	tx2 = t.points[1][0]
	ty2 = t.points[1][1]
	tx3 = t.points[2][0]
	ty3 = t.points[2][1]
	
	if min(tx1,tx2,tx3) <= rx2 and min(ty1,ty2,ty3) <= ry2 and max(tx1,tx2,tx3) >= rx1 and max(ty1,ty2,ty3) >= ry1:
		
		hW = (rx2-rx1) * 0.5
		hH = (ry2-ry1) * 0.5
		if abs(tx1-rx1-hW) <= hW and abs(ty1-ry1-hH) <= hH : return True
		if abs(tx2-rx1-hW) <= hW and abs(ty2-ry1-hH) <= hH : return True
		if abs(tx3-rx1-hW) <= hW and abs(ty3-ry1-hH) <= hH : return True
		
		if InTriangle(tx1,ty1,tx2,ty2,tx3,ty3,rx1,ry1) : return True
		if InTriangle(tx1,ty1,tx2,ty2,tx3,ty3,rx2,ry1) : return True
		if InTriangle(tx1,ty1,tx2,ty2,tx3,ty3,rx2,ry2) : return True
		if InTriangle(tx1,ty1,tx2,ty2,tx3,ty3,rx1,ry2) : return True
		
		if ty1 >= ry1 != ty2 >= ry1:
			if LinesIntersect(rx1,ry1,rx2,ry1,tx1,ty1,tx2,ty2,1) : return True
		if tx1 <= rx2 != tx2 <= rx2:
			if LinesIntersect(rx2,ry1,rx2,ry2,tx1,ty1,tx2,ty2,1) : return True
		if ty1 <= ry2 != ty2 <= ry2:
			if LinesIntersect(rx2,ry2,rx1,ry2,tx1,ty1,tx2,ty2,1) : return True
		if tx1 >= rx1 != tx2 >= rx1:
			if LinesIntersect(rx1,ry2,rx1,ry1,tx1,ty1,tx2,ty2,1) : return True
		if ty2 >= ry1 != ty3 >= ry1:
			if LinesIntersect(rx1,ry1,rx2,ry1,tx2,ty2,tx3,ty3,1) : return True
		if tx2 <= rx2 != tx3 <= rx2:
			if LinesIntersect(rx2,ry1,rx2,ry2,tx2,ty2,tx3,ty3,1) : return True
		if ty2 <= ry2 != ty3 <= ry2:
			if LinesIntersect(rx2,ry2,rx1,ry2,tx2,ty2,tx3,ty3,1) : return True
		if tx2 >= rx1 != tx3 >= rx1:
			if LinesIntersect(rx1,ry1,rx2,ry1,tx2,ty2,tx3,ty3,1) : return True
		if ty3 >= ry1 != ty1 >= ry1:
			if LinesIntersect(rx1,ry1,rx2,ry1,tx3,ty3,tx1,ty1,1) : return True
		if tx3 <= rx2 != tx1 <= rx2:
			if LinesIntersect(rx2,ry1,rx2,ry2,tx3,ty3,tx1,ty1,1) : return True
		if ty3 <= ry2 != ty1 <= ry2:
			if LinesIntersect(rx2,ry2,rx1,ry2,tx3,ty3,tx1,ty1,1) : return True
		if tx3 >= rx1 != tx1 >= rx1:
			if LinesIntersect(rx1,ry1,rx2,ry1,tx3,ty3,tx1,ty1,1) : return True
			
	return False
	
def InTriangle(x1,y1,x2,y2,x3,y3,xx,yy):
	
	a0 = abs((x2-x1) * (y3-y1) - (x3-x1) * (y2-y1))
	a1 = abs((x1-xx) * (y2-yy) - (x2-xx) * (y1-yy))
	a2 = abs((x2-xx) * (y3-yy) - (x3-xx) * (y2-yy))
	a3 = abs((x3-xx) * (y1-yy) - (x1-xx) * (y3-yy))
	return abs(a1+a2+a3-a0) <= 1/256.
	
def LinesIntersect(x1,y1,x2,y2,x3,y3,x4,y4,segment):

	ua = 0
	ud = (y4-y3) * (x2-x1) - (x4-x3) * (y2-y1)
	if (ud != 0):
		ua = ((x4-x3) * (y1-y3) - (y4-y3) * (x1-x3)) / (ud+0.)
		if segment:
			ub = ((x2-x1) * (y1-y3) - (y2-y1) * (x1-x3)) / (ud+0.)
			if ua < 0 or ua > 1 or ub < 0 or ub > 1:
				ua = 0
	
	if ua != 0 : return True
	return ua
	
def LoadImageFolder(folderPath):

	images = {}
	
	for imagePath in glob.glob(folderPath+"/*.png"):
		imageName = imagePath[len(folderPath)+1:-4].lower()
		images[imageName] = pygame.image.load(imagePath).convert_alpha()
		
	return images
	